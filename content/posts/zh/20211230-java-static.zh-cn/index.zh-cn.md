+++
author = "DUAN DAHAI"
title = "Java中static关键字"
date = "2021-12-30"
description = "static关键字的加载内存"
tags = [
    "Java",
    "static"
]
categories = [
    "Java"
]
+++

本文介绍关于Java中static对象(static修饰的变量或者方法)的一些特点

#### 内存加载
static对象和需要初期化对象的保存内存领域是不同的。

class类文件加载后，static和static以外的对象，分别保存在不同的内存空间中。static对象保存在称为[static领域]的内存中，static以外的对象保存在[heap领域]中，heap领域的class会被初期化生成。因为static对象，在class文件加载后立马进行内存分配，所以static对象被访问时，可以直接调用(Class名.static对象名)，当然也可以被生成的初期化对象调用(instanceOBJ.static对象名)。

由同一个Class生成的不同初期化对象中，所持有以及操作的同一个static对象是完全相同的,不会因调用对象而不同。

由于static对象是无需初期化生成即可使用的，因此在static方法中可以调用static对象，却不能调用还需要初期化生成的对象。相反，在初期化生成的对象中，可以随意调用static对象。

如下图：

![static内存领域](20211230-java-static.png)

