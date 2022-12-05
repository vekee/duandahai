+++
author = "DUAN DAHAI"
title = "使用AWS的SES作为Mastodon的邮件送信服务"
date = "2022-11-30"
description = "使用AWS的SES作为Mastodon的邮件送信服务"
tags = [
    "AWS",
    "SES"
]
categories = [
    "Mastodon"
]
+++

#### 概要

本文为[基于云服务的Mastodon站点搭建](https://duandahai.com/zh-cn/posts/zh/20221125-mastodon-site-create.zh-cn/)的关于使用AWS的SES来发送邮件的扩展介绍。

#### IAM User

- 创建User，并为User增加SES的送信权限。  
    我的AWS账户中只有一个SES服务，下面的权限设置中没有区分Resource。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ses:SendRawEmail",
            "Resource": "*"
        }
    ]
}
```

#### 创建SES的Identity

- 创建identity，设置Domain为你的域名  
![identity details](1_identity_details.PNG)

- 设置你送信用的邮箱地址   
![Github](2_mail_from_domain.PNG)

- 设置identity的类型  
![Github](3_identity_type.PNG)

- 将生成的CNAME记录，追加到你域名的DNS记录中  
![Github](4_CANME_DNS_records.PNG)

- 将生成的MX和TXT记录，追加到你域名的DNS记录中  
![Github](5_MX_TXT_DNS_records.PNG)

- 追加后的DNS记录里面，CNAME,MX和TXT记录如下  
![Github](6_add_DNS.png)


#### 申请接触SES的送信限制
在上面的Identity验证成功的基础上，向AWS support发送增加送信次数的申请[申请](https://docs.aws.amazon.com/ses/latest/dg/manage-sending-quotas-request-increase.html)。

#### 其他
Identity验证最多会花费72小时，建议仔细检查CNAME，MX,TXT的DNS记录是否设置正确，以免耽误等待时间。

