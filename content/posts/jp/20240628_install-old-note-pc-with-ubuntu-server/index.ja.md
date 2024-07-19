+++
author = "DUAN DAHAI"
title = "10年前のThinkPadをUbuntu ServerUbuntu 24.04に改造する記録"
date = "2024-06-28"
description = "10年前のThinkPadをUbuntu ServerUbuntu 24.04に改造する記録"
tags = [
    "Ubuntu"
    ]
categories = [
    "ソリューション"
]
+++

### Rufusを使って、UbuntuのライブブートUSBを作成する

[作成方法⇒Create a bootable USB stick with Rufus on Windows](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview)


### Ubuntu Serverをインストールする手順を以下のページを参考しました。
[古いWindowsノートPCにUbuntu Serverをインストールするまでの記録](https://www.iehohs.com/ubuntu-server-install/)

###  アップデートとアップグレード
* インストール後、まずシステムを最新の状態にする
```bash
sudo apt update
sudo apt upgrade -y
```

###  タイムゾーンの設定
* サーバーのタイムゾーンを日本東京に設定します
```bash
sudo timedatectl set-timezone Asia/Tokyo
sudo timedatectl
```

### Wifiが利用できるように設定
* WiFiインターフェースの名前（例：wlp3s0）を確認する
```bash
sudo lshw -C network
```
* Netplan設定ファイルをバックアップする
```bash
sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml.original
```
* Netplan設定ファイルを編集する
```bash
sudo vi /etc/netplan/50-cloud-init.yaml
```
* WiFiセクション内に以下のように設定する
```
network:
  ethernets:
    enp0s25:
       dhcp4: true
  version: 2
  wifis:
    wlp3s0:
      dhcp4: true
      access-points:
        "@Your_SSID":
          password: "Your_WiFi_Password"
```
* Netplanの設定を適用
```bash
sudo netplan apply
```
* IPアドレスの確認
```bash
ip a
```

### ノートPCのカバーを閉じてもシステムをオンのままにする
* 電源設定ファイルを編集する
```bash
sudo cp /etc/systemd/logind.conf /etc/systemd/logind.conf.original
```
* ファイル内に以下の行があるはずです。コメントアウトされている場合はコメントを外し、値を以下のように変更する。
```
HandleLidSwitch=ignore
HandleLidSwitchDocked=ignore
```
* ファイルを保存して閉じた後、以下のコマンドを実行して設定を反映させます
```bash
sudo systemctl restart systemd-logind
```

### ノートPCのカバーを閉じてもシステムをオンのままにする
* 電源設定ファイルを編集する
```bash
sudo cp /etc/systemd/logind.conf /etc/systemd/logind.conf.original
```
* ファイル内に以下の行があるはずです。コメントアウトされている場合はコメントを外し、値を以下のように変更する。
```
HandleLidSwitch=ignore
HandleLidSwitchDocked=ignore
```
* ファイルを保存して閉じた後、以下のコマンドを実行して設定を反映させます
```bash
sudo systemctl restart systemd-logind
```

### Tera Termマクロスクリプトを作成し、Ubuntu Serverを接続する
* 新しいテキストファイルを作成し、以下の内容を記述します。これを.ttlファイルとして保存する（例: connect_ubuntu_server.ttl）。
```
;=====================================================================
; 接続情報
;=====================================================================
HOSTADDR = '192.168.2.151'
PORT = '22'
USERNAME = 'jimiloveme'
PASSWORD = 'you guess'

;=====================================================================
; コマンドオプション組立て
;=====================================================================
COMMAND = HOSTADDR
strconcat COMMAND ' /ssh /2 /auth=password /user='
strconcat COMMAND USERNAME
strconcat COMMAND ' /passwd='
strconcat COMMAND PASSWORD
strconcat COMMAND ' /port='
strconcat COMMAND PORT

;=====================================================================
; 接続
;=====================================================================
connect COMMAND


; 接続後の操作をここに記述
; 例: ホームディレクトリの内容を表示
wait '$ '
sendln 'ls -la'

; マクロの終了
end
```

### docker composeインストール
* 必要なパッケージをインストール
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release
```

* DockerリポジトリのGPGキーを取得
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

* Dockerリポジトリをaptソースに追加
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

* dockerインストール
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

* docker確認
```bash
docker --version
sudo docker run hello-world
```

* 一般ユーザでDockerを起動する
```bash
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

* docker compose確認
```bash
docker compose version
```

### ファイルシステムの監視設定変更
* ファイルシステムの監視設定ファイルの編集
```bash
sudo vi /etc/sysctl.conf
```

* ファイルの末尾に次の行を追加します。
```
fs.inotify.max_user_watches = 524288
```

* 設定の反映
```bash
sudo sysctl -p
```

### odooインストール

[参考資料](https://github.com/minhng92/odoo-17-docker-compose/tree/master)

* ファイルとフォルダー構成
```bash
sudo mkdir -p /srv/odoo17-prod
cd /srv/odoo17-prod
sudo mkdir -p addons && sudo mkdir -p etc && sudo mkdir -p postgresql 
sudo touch etc/odoo.conf && sudo touch etc/requirements.txt
sudo chmod -R 777 addons && sudo chmod -R 777 etc && sudo chmod -R 777 postgresql
sudo touch docker-compose.yml
```

* ファイル中身略

* docker composeコマンド
```bash
# dockerサービスをバックグラウンドで起動する
docker compose up -d
# dockerサービスを再起動する
docker compose restart
# dockerサービスを停止する
docker compose down
```

* docker コマンド
```bash
# すべてのコンテナの一覧を表示
docker ps -a
# 稼働中のコンテナの一覧を表示
docker ps
# コンテナを削除
docker rm <コンテナIDまたは名前>
```

### ログ監視
* リアルタイムのアクセスログ監視
```bash
# リアルタイムのアクセスログを確認
tail -f odoo-server.log
# 最後から3行を表示する
tail odoo-server.log -n 100
```

### Nginx設定



