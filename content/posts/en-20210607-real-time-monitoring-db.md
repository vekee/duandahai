+++
author = "DUAN DAHAI"
title = "The solutions for real time monitoring abnormal data in database"
date = "2021-06-07"
description = "The solutions for real time monitoring abnormal data in database"
tags = [
    "database"
]
categories = [
    "solutions",
    "MonitoringTable"
]
+++

#### The design of monitoring system

In some case we need monitor application's latest data in database on time.
We could built a monitoring system out of the application.

In this case, to handle a large of new data per second with high-performance,
we can build the monitoring system like this:

- Output new inserted data into monitoring system database by trigger 
- Output new inserted data into Queque(like AWS SQS) by trigger 
- Get new data from Queque and execute your monitoring app in dynamic multiple process 

![design](/media/en/20210607-real-time-monitoring-db-1.png)

