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
    "AWS",
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
全件105のデータを多重で処理する、1ジョブに最大10件処理をする場合、
以下の制御情報リストを作成します。
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

**注** 下記は制御情報を返却する実装例です。

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
    
    return {
        'statusCode': 200,
        'body': json.dumps(controlInfoList)
    }
```

#### 業務処理
更新中.

**Note** that you can use *Markdown syntax* within a blockquote.
{{< highlight html >}}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Example HTML5 Document</title>
</head>
<body>
  <p>Test</p>
</body>
</html>
{{< /highlight >}}

#### ステートマシン
更新中.

**Note** that you can use *Markdown syntax* within a blockquote.
{{< highlight html >}}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Example HTML5 Document</title>
</head>
<body>
  <p>Test</p>
</body>
</html>
{{< /highlight >}}

#### 参考資料
* https://aws.amazon.com/jp/blogs/news/new-step-functions-support-for-dynamic-parallelism/
* https://docs.aws.amazon.com/ja_jp/step-functions/latest/dg/amazon-states-language-map-state.html
