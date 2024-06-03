+++
author = "DUAN DAHAI"
title = "APIアプリケーションをLinuxサービスとして設定する方法"
date = "2023-09-30"
description = "APIアプリケーションをLinuxサービスとして設定し、システム起動時に自動的に起動するように設定する方法"
tags = [
    "Linux",
    "API",
    "Systemd"
]
categories = [
    "ソリューション"
]
+++

Linux環境でAPIアプリケーションを運用する際、システムの起動と共に自動的にアプリケーションを起動させたいことがあります。systemdを使用してAPIアプリケーションをLinuxサービスとして設定することで、安定した運用が可能となります。本記事では、JavaベースのAPIアプリケーションを例に、その手順を紹介します。

##### 前提条件
- Linux環境（本記事ではUbuntuを利用している） 
- Javaがインストールされていること
- APIアプリケーションのJARファイルが存在すること

##### サービスファイルの作成
まず、サービスファイルを作成します。このファイルには、サービスの起動方法や動作設定を記述します。
```
sudo nano /etc/systemd/system/yourapp.service
```

以下の内容をサービスファイルに記述します：
```
[Unit]
# サービスの説明と起動の順序を指定します
Description=APP Service
After=network.target

[Service]
# サービスの実行に関する設定を行います
User=sme
ExecStart=/usr/bin/java -jar /home/sme/live/public/yourapp.jar
SuccessExitStatus=143
Restart=on-failure
RestartSec=10
WorkingDirectory=/home/yourappuser/live/public

[Install]
# サービスのインストールに関する設定を行います
WantedBy=multi-user.target
```

##### サービスのリロードと起動
サービスファイルを作成したら、systemdに新しいサービスを認識させ、サービスを起動します。
```
sudo systemctl daemon-reload  # systemdの設定をリロード
sudo systemctl start yourapp.service  # サービスを起動
sudo systemctl enable yourapp.service  # サービスを自動起動に設定
```

##### サービスの状態確認
サービスの状態を確認して、正常に動作しているかどうかを確認します。
```
sudo systemctl status yourapp.service
```

##### 最後
APIアプリケーションをLinuxサービスとして設定することで、システム起動時に自動的にアプリケーションが起動し、安定した運用が可能になります。この手順を参考に、自身の環境でも試してみてください。