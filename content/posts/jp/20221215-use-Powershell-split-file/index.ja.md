+++
author = "DUAN DAHAI"
title = "Powershellを利用して、改行なし固定長ファイルを分割する"
date = "2022-12-15"
description = "Powershellを利用して、改行なし固定長ファイルを分割する"
tags = [
    "Powershell",
    "ファイル分割"
]
categories = [
    "技術文章"
]
+++

改行なし固定長ファイルについて、Powershellより分割する方法をご紹介します。

#### ファイル特徴
+ ファイルに改行なし、全てレコードを一行にあつめている。  
+ 各レコード長は固定のバイト数。  
+ ファイルの文字コードが統一ではない、SJIS、UTF-8の可能性がある。  

#### 分割方法（性能弱）
ネットで以下の分割スクリプトを見つかって、問題なく分割できるが、件数が10万件以上の場合、すごく時間がかかります。

```shell
$WindowSize = 400
$File = [System.IO.File]::OpenRead("C:¥test.csv")
$Stream = New-Object System.IO.BinaryReader $File
0 .. (($File.Length - 1) / $WindowSize) |% {
    $str = [System.Text.Encoding]::Default.GetString($Stream.ReadBytes($WindowSize))
    Write-Output $str | Out-File -Append "C:¥test.csv.out"
}
$File.Close()
```

#### 分割方法（性能改善版）
上記のスクリプトを解析したら、ファイルストリムから1行づつのバイナリデータを読み込んで、1行づつを書き込み先ファイルに追加している仕様となります。  

遅い原因は以下2点であると思います。
+ 書き込み先ファイルを頻繁に使うこと
    - 改善策例：1000行づつに書き込み先ファイルに追加
+ ファイルストリムを頻繁にアクセスすること
    - 改善策例：ファイルストリムから1000行づつに読み込み

改善策を原因毎に取り込んで、以下のPowershellをご参照ください。
```shell
$LineByteLength = 400
$LineSlicesSize = 1000
$File = [System.IO.File]::OpenRead("C:¥test.csv")
$Stream = New-Object System.IO.BinaryReader $File
$LineSlicesContent = [System.Text.Encoding]::Default.GetString($Stream.ReadBytes($LineByteLength * $LineSlices))
do {
    $LineStr = ""
    $enc = [System.Text.Encoding]::Default
    $bytes = $enc.GetBytes($LineSlicesContent)
    for ($i=0; $i -lt ($bytes.Length / $LineByteLength); $i++){
        if (($i + 1) -eq ($bytes.Length / $LineByteLength)) {
            $LineStr = $LineStr + $enc.GetString($bytes, $i * $LineByteLength, $LineByteLength)
        } else {
            $StackLineStr = $StackLineStr + $enc.GetString($bytes, $i * $LineByteLength, $LineByteLength) + "`r`n"
        }
    }
    Write-Output $StackLineStr | Out-File -Append "C:¥test.csv.out"
    $LineSlicesContent = [System.Text.Encoding]::Default.GetString($Stream.ReadBytes($LineByteLength * $LineSlicesSize))
} until([string]::IsNullOrEmpty($LineSlicesContent))
$File.Close()
```

#### まとめ
Powershellの利用は私も初めてですが、VB、DOSコマンド、shellと似ているところがあります。基本的に不明な使い方がありましたら、DOCを参照しながら実装できれば結構です。