+++
author = "DUAN DAHAI"
title = "マップ状態を利用して、動的並列にLambdaを多重で実行する"
date = "2021-10-27"
description = "Lambda実行時間の最大15分制限より、15分以内に処理完了するために、同一Lambdaを並行で処理する対策方法を説明しました。"
tags = [
    "AWS",
    "Lambda",
    "Stepfunctions",
    "Map"
]
categories = [
    "技術文章",
    "AWS"
]
+++

Lambda実行時間の最大15分制限より、15分以内に処理完了するために、同一Lambdaを並行で処理する対策を説明します。

#### 対策概要
1. AWS Lambda 関数：動的並列数制御処理
2. AWS Lambda 関数：業務処理
3. AWS Step Functions ステートマシン

動的並列数制御処理に処理する全体のデータ量より、並列数、各並列起動で処理するデータを決めて、Step Functions の OutputPathに並列数と同じなサイズのJsonリストで返却します。
Map stateがJsonリストの要素ごとに、各並列起動情報を引数として、業務処理を起動します。
業務処理に振り分けされたそれぞれの処理対象を処理して、15分以内に完了するように実現できます。


#### 動的並列数制御処理
全件105のデータを多重で処理して、一つ並行処理ジョブに最大10件を処理する場合、
以下の制御情報リストを作成とします。
```JSON
[
  {
    'oneJobProcessingCount': 10,
    'offset': 0
  },
  {
    'oneJobProcessingCount': 10,
    'offset': 10
  },
  {
    'oneJobProcessingCount': 10,
    'offset': 20
  }
  ・・・・・・
  {
    'oneJobProcessingCount': 5,
    'offset': 100
  }
]
```

下記は制御情報を返却する実装例です。

**note** 並行処理ジョブ数を指定することより、平均的に全てのデータを分割して、並行処理することも可能です。

**note** 一つ並行処理ジョブに、処理件数をできるだけ15分完了近くまでに調整すれば、Lambdaの利用料金を減らすことが可能です。


```python
import json

def lambda_handler(event, context):
    
    totalProcessRecordCount = 105
    oneJobProcessMaxCount = 10
    
    jobCount = totalProcessRecordCount // oneJobProcessMaxCount
    
    controlInfoList = []
    for jobIndex in range(jobCount):
        controlInfo = {
            'oneJobProcessingCount': oneJobProcessMaxCount,
            'offset': jobIndex * oneJobProcessMaxCount
        }
        controlInfoList.append(controlInfo)
    
    if totalProcessRecordCount % oneJobProcessMaxCount != 0:
        controlInfo = {
            'oneJobProcessingCount': totalProcessRecordCount % oneJobProcessMaxCount,
            'offset': jobCount * oneJobProcessMaxCount
        }
        controlInfoList.append(controlInfo)
    
    return controlInfoList
```

#### 業務処理

下記は業務処理の実装例です。

並列実行しているLambdaに処理される対象レコードを返却する。

```python
def lambda_handler(event, context):
    oneJobProcessingCount = int(event['oneJobProcessingCount'])
    offset = int(event['offset'])
    
    processed = []
    for i in range(oneJobProcessingCount):
        processed.append(offset + i)
        
    return processed
```


#### ステートマシン

動的並列数制御処理で、生成した並列情報リストをLoopして、非同期で業務処理を起動する。
Mapを利用して、作成したステートマシンは、以下のようなイメージです。

![ステートマシン](20211027-AWS-stepfunctions-Map-state.png)


下記はステートマシンの記述です。

```JSON
{
  "Comment": "A dynamically parallel process example of the Amazon States Language using Map",
  "StartAt": "dynamically-parallel-processing-control",
  "States": {
    "dynamically-parallel-processing-control": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:ap-northeast-1:370382556331:function:dynamically-parallel-processing-control"
      },
      "Next": "dynamically-parallel-processing-iterator"
    },
    "dynamically-parallel-processing-iterator": {
      "Type": "Map",
      "InputPath": "$",
      "ItemsPath": "$",
      "MaxConcurrency": 0,
      "Iterator": {
        "StartAt": "dynamically-parallel-processing",
        "States": {
          "dynamically-parallel-processing": {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "Parameters": {
              "FunctionName": "arn:aws:lambda:ap-northeast-1:370382556331:function:business-logic-process"
            },
            "End": true
          }
        }
      },
      "End": true
    }
  }
}
```

#### 走行結果
1. ステートマシンのログ出力より、動的並列数制御処理の並列数処理結果は、以下です。

```JSON
{
  "name": "dynamically-parallel-processing-control",
  "output": [
    {
      "oneJobProcessingCount": 10,
      "offset": 0
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 10
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 20
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 30
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 40
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 50
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 60
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 70
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 80
    },
    {
      "oneJobProcessingCount": 10,
      "offset": 90
    },
    {
      "oneJobProcessingCount": 5,
      "offset": 100
    }
  ],
  "outputDetails": {
    "truncated": false
  }
}
```

2. 並列起動される業務処理の入力パラメーター例は以下となります。

```JSON
{
  "name": "dynamically-parallel-processing",
  "input": {
    "ParallelIndex": 0,
    "ParallelControlInfo": {
      "oneJobProcessingCount": 10,
      "offset": 0
    }
  },
  "inputDetails": {
    "truncated": false
  }
}
```

3. 並列で起動された業務処理の実行結果例は以下となります。

```JSON
{
  "resourceType": "lambda",
  "resource": "invoke",
  "output": {
    "ExecutedVersion": "$LATEST",
    "Payload": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9
    ],
    ・・・
```

#### まとめ
上記の簡単なサンプルより、MAPの利用で、Lambda処理を動的並行で処理されることを確認しました。
実際の業務開発に、並行処理が複数、処理前後依存などケースがあるかもしれないので、状況よりご活用ください。

#### Mapのオプション

* ItemsPath

    並行処理を実行するベースの配列要素。配列に格納されている要素ごとに、非同期で処理を起動する。
いずれかの並行処理が失敗すると、全体の処理が失敗となり、ステートマシンが終了します。


* MaxConcurrency

    同時並行実行の最大数を定義する。
デフォルト値は0です。この場合、同時並行実行数が無制限です。
設定される場合、同時並行実行処理数がこの設定値を超える部分は、前処理が終了するまで待ちがます。


#### 参考資料
* https://aws.amazon.com/jp/blogs/news/new-step-functions-support-for-dynamic-parallelism/
* https://docs.aws.amazon.com/ja_jp/step-functions/latest/dg/amazon-states-language-map-state.html
