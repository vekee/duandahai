+++
author = "DUAN DAHAI"
title = "Use AWS lambda as api endpoint"
date = "2023-02-07"
description = "Use AWS lambda as api endpoint"
tags = [
    "AWS",
    "Lambda",
    "API"
]
categories = [
    "solutions"
]
+++

[AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) + [API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) can easily and quickly build your api servcie.   
You can find the the introduce and Benefits on aws documents.   
I will just show you how eazy to build a api in this article.


### Create a python lambda by your fastest way
![1-lamda](1-lamda.png)

### Create a HTTP API by AWS API Gateway
![2-API](2-API.png)

### when creating the HTTP API, use the default stage and default settings
![3-stage](3-stage.png)

### add a test rout linked to python lambda as the endpoint
![4-rout](4-rout.png)

### then test your api in browser, connected backend lambda successfully!
![5-test](5-test.png)