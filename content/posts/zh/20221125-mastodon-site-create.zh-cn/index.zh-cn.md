+++
author = "DUAN DAHAI"
title = "基于云服务的Mastodon站点搭建"
date = "2022-11-25"
description = "基于云服务的Mastodon站点搭建"
tags = [
    "AWS",
    "Mastodon"
]
categories = [
    "Mastodon"
]
+++

#### Mastodon简介

一言蔽之就是一个去中心化的开源社交媒体。
详细内容请参看<a href="https://github.com/mastodon/mastodon" >mastodon</a>官方介绍。


能够看到这篇文章的人，我相信已经对Mastodon有了一定的了解，我就直入主题，讲讲我是如何搭建Mastodon站点的，过程中遇到的那些坑以及我会给打算尝试朋友的一些建议。

#### Mastodon的搭建教程

Mastodon的instance搭建教程都是放在官方的<a href="https://docs.joinmastodon.org" >documentation</a>里面，搭建教程主要是以下章节。

+ <a href="https://docs.joinmastodon.org/user/run-your-own/" >Running your own server</a>
+ <a href="https://docs.joinmastodon.org/admin/prerequisites/" >Preparing your machine</a>
+ <a href="https://docs.joinmastodon.org/admin/install/" >Installing from source</a>

注意：由于所有的文档都是Mastodon社区维护的，虽然有中文的版本，但可能不是最新的。建议中文和英文的都先浏览一遍，最后按照英文的文档实施。

#### <a href="https://docs.joinmastodon.org/user/run-your-own/" >Running your own server</a>
这个章节是告诉你，要搭建Mastodon站点需要准备的内容。
它列出了可以提供一条龙托管服务的网站，以及一键安装的镜像文件，  
当然，既然你来到这里，肯定是希望自己动手从头尝试的，那么请继续看下面。

+ 域名(A domain name) 

    我选择的是<a href="https://www.onamae.com/" >onamae</a>，当然你也可以选择像<a href="https://www.godaddy.com/" >godaddy</a>等其他的域名服务商。  
    不过既然是基于云服务的，我建议你选择你所用云服务商的域名服务，因为在随后的一些设置中会方便很多，管理上也会很方便。  
    当然，如果你像我一样，已经有很多域名托管在某个服务商那里的话，不妨集中在那里管理也可以。

+ 主机(A VPS)

    我选择使用AWS的EC2, 主机大小是双核4G，100G存储，目标支撑2000日活用户。  
    不建议选择很便宜的VPS，因为一份价钱一分货，从我使用VPS的经验来看，共用的主机的VPS被攻击，中毒，宕机，访问慢等各种问题太多了，使用感很差，但就是便宜。

+ 邮件服务(An e-mail provider)

    我用的是AWS的云服务，当然选择AWS里面的邮件服务SES。  
    你可以选择其他的专门邮件服务商，因为管理各种账号太麻烦，而且云服务的邮件服务免费额度也很大，扩展性更不用说，所以我首先使用云服务商的邮件服务。  
    但是，AWS的SES默认是有送信限制，以及需要事前登录被送信者邮箱地址的，这根本不符合需求啊，但是请记住，AWS的SES是可以申请解除该限制的。  
    关于如何解除该限制，我会在下面的一篇文章中介绍。  
    [《使用AWS的SES作为Mastodon的邮件送信服务》](https://duandahai.com/zh-cn/posts/zh/20221130-mastodon-ses-dns.zh-cn/)


+ 存储服务(Object storage provider)

    我这边就直接使用AWS S3的存储服务了。  
    不建议将文件的存储放在主机上。  
    在设定AWS S3时，会出现访问S3被拒的问题，解决方法我放在下面一篇文章中介绍了。  
    [《使用AWS的S3服务来保存Mastodon的媒体文件》](https://duandahai.com/zh-cn/posts/zh/20221205-mastodon-s3.zh-cn/)


#### [Preparing your machine](https://docs.joinmastodon.org/admin/prerequisites/)

这个章节中主要是准备你的主机，建议准备官方教程指定的OS版本（2022年12月为Ubuntu 20.04），这个章节基本上没有问题。

因为我使用的是AWS的EC2, 所以我可以在AWS上对主机额外再设置一份访问限制。
你如果也要这样做的话，注意不要把应该要有的访问给限制了。


#### [Installing from source](https://docs.joinmastodon.org/admin/install/)

经验总结  
1. 这个章节中会出现一些问题，一定要通篇浏览教程后，严格按照教程走，不然出现问题不太好分析原因。
2. 设置过程中，出现的各类问题最好都能随时保存下来，为随后自己学习也为Mastodon社区的发展更新贡献一份力。
3. 各种密码以及账号，一定要随时设置随时记录保存下来。
4. 一些source的版本随后可能需要随着Mastodon的版本更新而再更新，但是不用担心，现在只需要按照官方教程的版本走就没有问题。
5. 官方教程的数据库是没有和主机分离的，对于最初的你来说，不是什么大问题而且会节省不少费用，如果你的主机人数达到很多的时候，再考虑将数据库单独移出来也并不麻烦。

可能发生的问题汇总
1. 获取SSL certificate失败，或者因为定义的ssl_certificate不存在导致Nginx启动失败  
    - 解决方法请参照我在Github上关于该Issue的[回答](https://github.com/mastodon/documentation/issues/857#issuecomment-1315281894)

2. 首页的CSS以及Javascript不起作用  
    - 确认WebLog命令：journalctl -eu mastodon-web
    - 原因推测：应该是一些CSS文件或者JS文件执行权限受限制了
    - 解决方法请参照我在Github上的回答[All CSS / JS Not Being Passed Client Side](https://github.com/mastodon/mastodon/discussions/17221#discussioncomment-4151966)


3. 邮件无法送信
    - 可以在你站点的以下管理页面中确认发送失败的log  
    https://example.com/sidekiq/retries
    - 原因推测：各人利用的服务不同，原因太多，不好推测

4. 即使设置了可www访问的DNS设置，也无法访问www站点
    - 原因推测：Nginx未对应www访问
    - 可增加www访问的www重定向，还没有尝试。如果有尝试成功的朋友请分享以下。


#### Mastodon的版本升级
网上有各种关于Mastodon的版本升级介绍，我要告诉你的是一定✖️3要去官方Github上查看各个版本[Release记录](https://github.com/mastodon/mastodon/tags)，里面会有关于版本升级的详细内容。  
如果要跨多个版本升级的话，你最好逐个确认各个版本间有没有需要特别处理的地方，是否可以跨版本直接升级到最新版本。

#### 其他
1. 将你的SSL证书更新设置为自动更新
2. 将你的数据库和source，定期打包备份到S3