+++
author = "DUAN DAHAI"
title = "Workflow服务在Cloud中的应用场景小结"
date = "2021-11-06"
description = "Workflow服务的应用场景小结"
tags = [
    "Workflow",
    "Actions"
]
categories = [
    "Cloud",
    "KnowHow"
]
+++

本文介绍关于Workflow在Cloud服务中的一些应用场景。

#### Workflow服务的概念
英文：Workflow as a service。直接翻译为中文：工作流服务

* 工作流可以简单理解为企业或者个人处理业务的一个流程。简单的工作流举例如下图：

![工作流](/media/20211106-workflow-actions.zh-cn-1.png)

* 在Cloud中，即是将工作流转化为一种可提供的Cloud服务。该服务可能是固定形式的，也可能是根据具体业务场景自定义开发，后者支持范围广，服务场景多，在Cloud服务中比较常见。


#### AWS中的Workflow服务-Amazon Simple Workflow Service (SWF)
AWS官网称SWF是一种低代码可视化工作流服务，用于编排AWS服务、自动化业务流程或构建无服务器应用程序。具有以下特点：

* 逻辑分隔

  流程控制、底层的状态结构和任务分派分开管理，降低耦合性，方便修改维护。

* 可靠

  SWF在Amazon 的高可用性数据中心中运行，因此状态追踪和任务处理引擎可以在应用程序需要时随时可用。SWF还具有冗余存储任务，可将它们指派到应用程序组件，追踪进度并使其保持最新状态。

* 简单

  SWF用全托管的云工作流Web服务替代复杂的定制代码，属于工作流解决方案和流程自动化软件。开发人员不再需要管理流程自动化的基础设施，可以将精力集中在应用程序的独特功能上。

* 可扩展

  SWF可以随着应用程序的使用进行无缝调节。无需对工作流服务进行人工管理，即可在应用程序中添加更多云工作流或增加工作流复杂性。

* 灵活

  SWF中可以使用多种编程语言进行应用程序组件和协作逻辑编写，并在云中或本地运行。

#### Salesforce中的Workflow服务-workflow
Salesforce对workflow解释为将企业标准的业务、程序进行自动化，以提高业务流程效率。

#### Google中的Workflow服务
Google中的Workflow是一种对给定任务进行可编排的的服务平台。主要的应用场景：

* 各种服务的编排

* Batch Job处理

* 业务流程处理

* 业务自动化


#### Github中的Workflow服务


#### 其他企业提供的Workflow服务


#### Workflow服务的需要的底层技术支持


#### 为什么会用到Workflow服务，Workflow服务的优点缺点


#### 参考資料
* https://www.sciencedirect.com/science/article/pii/S1877050914002269