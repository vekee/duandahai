+++
author = "DUAN DAHAI"
title = "How to send html form via email"
date = "2022-06-16"
description = "How to send html form via email"
tags = [
    "send email",
    "html form"
]
categories = [
    "html",
    "solution"
]
+++


### Use API for send html form via email.

For an online html site, in some case ,it has no hosted server or just want to get the information submitted in the form via email without backend program.

This post introduce one API that can help you make it simple and easily.

You can just set your form action like this:

```
<form action="https://formsendbox.com/sendto/[set your receive email at here]" method="post">
some input contents
</from>
```

When one submit this form, the API will send the input form to your email.


#### This API can also be used in Ajax.

+ Send text email API URL

    `https://formsendbox.com/sendSimpleMail`

+ Send text email with a attach file API URL

    `https://formsendbox.com/sendSimpleMailWithAttachment`


You need to set the necessary JSON Arguments that to send your email by javascript or other program.

+ toList
    - a list of email addresses that will be send to.
    - like [aa@gmail.com, bb@gmail.com].

+ ccList

    - a list of email addresses that will be send by carbon copy.
    - like [aa@gmail.com, bb@gmail.com].

+ bccList
    - a list of email addresses that will be send by blind carbon copy.
    - like [aa@gmail.com, bb@gmail.com].

+ title
    - the email title

+ content
    - the email content

+ fileName
    - the file name of attachment .
    - if an attach file will be send ,this parameter must be set.

+ fileBytes
    - the bytes of attachment file.
    - if an attach file will be send ,this parameter must be set.

+ formsendbox_id
    - certification id.
    - a free public formsendbox_id `b309590d3bb80e140873d729be7c8d6d`.

+ formsendbox_key
    - certification key.
    - a free public formsendbox_key `2b2731af96cc3d862395993a7ba1188d`.

#### Reference
You can find more information on <a href="https://formsendbox.com" >their site.</a>
