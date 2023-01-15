+++
author = "DUAN DAHAI"
title = "バイナリコードの文字列変数をデコードする"
date = "2023-01-15"
description = "バイナリコードの文字列変数をデコードする"
tags = [
    "Python",
    "Binary decode"
    ]
categories = [
    "技術文章"
]
+++

Pythonでバイナリデータをデコードする方法は、以下のものがあるが、
今回の課題はバイナリデータではなく、バイナリデータの文字列をデコードすることです。
```python
# エンコード（文字列の"日本"をbytesに変換）
print("日本".encode("utf-8"))

# デコード（bytesを文字列の"日本"に変換）
print(b'\xe6\x97\xa5\xe6\x9c\xac'.decode("utf-8"))
```

なぜこの変な課題があるかは、AWS S3 Triggerで起きたイベントに、日本語名KeyがUTF-8でエンコードされて、以下のように出ています。
```
# S3 Trigger設定された元のS3 Key名
"日本/test.pdf"

# S3 Triggerで起きたイベントに出ているKey名
"%e6%97%a5%e6%9c%ac/test.pdf"
```

#### デコード方法
バイナリデータの文字列は、文字列型の変数のため、直接bytes関数よりデコードができません。  
また、この変数をさらにエンコードしてから、デコードしてもできません。
以下の結果になります。
```
bstr = "\xe6\x97\xa5\xe6\x9c\xac"
print(bstr.encode("utf-8").decode("utf-8"))
# output：\\xe6\\x97\\xa5\\xe6\\x9c\\xac
```

Pythonの`bytes`仕様を調べたら、`fromhex`関数があるため、
16進数の文字を以下のようにデコードができます。
```
bstr = " e6 97 a5 e6 9c ac"
print(bytes.fromhex(bstr))
# output："日本"
```

上記の方法を従って、S3 Triggerで起きたイベントに出ているKey名に、
16進数の文字を判別して、`fromhex`でデコードできる発想がありました。

デコード例：
"%e6%97%a5%e6%9c%ac/test.pdf"から、"%e6%97%a5%e6%9c%ac"を16進数として判別し、" e6 97 a5 e6 9c ac"に変換してから`fromhex`でデコードします。  
デコード後の文字と16進数ではない文字を結合して、元のKeyになります。
"日本" + "/test.pdf"　→ "日本/test.pdf"

実現コードを以下の実装をご参照ください。

#### `fromhex`を利用して、デコード実装
```python
def isHex(str):
    try:
        int(str, 16)
        return True
    except:
        return False

def convertBstrToStr(binary_str):
    decoded_str = ""
    
    tmp_hex_str = ""
    index = 0
    while index < len(binary_str):
    
        c = binary_str[index : index + 1]
    
        if c == "%":
            hex_str = binary_str[index + 1 : index + 3]
            if isHex(hex_str):
                tmp_hex_str = tmp_hex_str + " " + hex_str
                index = index + 2
            else:
                decoded_str = decoded_str + c
        else:
            if tmp_hex_str != "":
                binary_str_bytes = bytes.fromhex(tmp_hex_str)
                decoded_str = decoded_str + binary_str_bytes.decode("utf-8")
                tmp_hex_str = ""
            
            decoded_str = decoded_str + c
    
        index = index + 1
    return decoded_str
```