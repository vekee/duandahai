+++
author = "DUAN DAHAI"
title = "Nginxで複数ドメインサービスを一つサーバーに運用する"
date = "2023-08-03"
description = "Nginxで複数ドメインサービスを一つサーバーに運用する"
tags = [
    "Nginx",
    "REST API SERVICE",
    "VPS"
    ]
categories = [
    "ソリューション"
]
+++

VPS上で既に稼働しているアプリケーションの利用率が低いため、コスト削減を目的に他のサービスも同一のVPSにデプロイしたいと考えました。本記事では、Nginxを利用してアクセス先のドメインごとに各サービスへリクエストをディスパッチする方法を共有します。


##### 前提条件
- NginxがインストールされているVPSを所有していること
- 複数のサービスとそれぞれに対応するドメインを所有していること

##### Nginxの設定
以下の設定をNginxの設定ファイル（通常は/etc/nginx/nginx.confまたは/etc/nginx/sites-available/default）に追加します。


##### HTTPサーバーブロックの設定
```
# サイト1のHTTPサーバーブロック
server {
    listen 80;  # ポート80でのHTTPリクエストを待ち受ける
    server_name site1.com www.site1.com;  # site1.comおよびwww.site1.comのドメインからのリクエスト

    location / {
        proxy_pass http://localhost:8081;  # リクエストをlocalhostのポート8081にプロキシする
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# サイト2のHTTPサーバーブロック
server {
    listen 80;  # ポート80でのHTTPリクエストを待ち受ける
    server_name site2.com www.site2.com;  # site2.comおよびwww.site2.comのドメインからのリクエスト

    location / {
        proxy_pass http://localhost:8082;  # リクエストをlocalhostのポート8082にプロキシする
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

##### HTTPSサーバーブロックの設定
```
# サイト1のHTTPSサーバーブロック
server {
    listen 443 ssl;  # ポート443でのHTTPSリクエストを待ち受ける
    server_name site1.com www.site1.com;  # site1.comおよびwww.site1.comのドメインからのリクエスト

    location / {
        proxy_pass https://localhost:8441;  # リクエストをlocalhostのポート8441にHTTPS経由でプロキシする
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    ssl_certificate      /etc/letsencrypt/live/site1.com/fullchain.pem;  # SSL証明書のパス
    ssl_certificate_key  /etc/letsencrypt/live/site1.com/privkey.pem;  # SSL証明書の秘密鍵のパス
    ssl_protocols        TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;  # サポートするSSLプロトコルのバージョン
    ssl_ciphers          HIGH:!aNULL:!MD5;  # 使用するSSL暗号スイート
}

# サイト2のHTTPSサーバーブロック
server {
    listen 443 ssl;  # ポート443でのHTTPSリクエストを待ち受ける
    server_name site2.com www.site2.com;  # site2.comおよびwww.site2.comのドメインからのリクエスト

    location / {
        proxy_pass https://localhost:8442;  # リクエストをlocalhostのポート8442にHTTPS経由でプロキシする
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    ssl_certificate      /etc/letsencrypt/live/site2.com/fullchain.pem;  # SSL証明書のパス
    ssl_certificate_key  /etc/letsencrypt/live/site2.com/privkey.pem;  # SSL証明書の秘密鍵のパス
    ssl_protocols        TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;  # サポートするSSLプロトコルのバージョン
    ssl_ciphers          HIGH:!aNULL:!MD5;  # 使用するSSL暗号スイート
}
```

#### 設定の適用
設定ファイルの編集が完了したら、以下のコマンドを実行してNginxの設定をテストし、問題がなければ再起動します。
```
sudo nginx -t  # 設定ファイルのテスト
sudo systemctl reload nginx  # Nginxの再読み込み
```


#### 結論
Nginxを利用することで、一つのVPS上で複数のドメインサービスを効率的に運用することができます。この設定により、VPSのリソースを最大限に活用し、運用コストを削減することができます。