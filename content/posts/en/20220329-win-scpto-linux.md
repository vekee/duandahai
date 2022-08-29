+++
author = "DUAN DAHAI"
title = "Scp files from windowsOS to linuxOS"
date = "2022-03-29"
description = "Scp files from windowsOS to linuxOS"
tags = [
    "SCP",
    "WinSCP"
]
categories = [
    "Windows",
    "Linux"
]
+++

When we want to scp files from Windows to linux in our application,and there is a limit to install a software,we can use the WinSCP Command-line in Windows command prompt.


WinSCP Command-line have two modes (Console/scripting mode),

I listed the console mode basic sample below.

```
C:¥winscp¥winscp.com /command "option batch on" "option confirm off" "open sftp://[scp user]:[scp password]@[scp to ipaddress]" "put C:¥test¥test01.txt" "/temp/" "option transfer binary" "close" "exit"

```


#### Reference
We can also use any other options in <a href="https://winscp.net/eng/docs/commandline" >WinSCP Command-line Options.</a>
