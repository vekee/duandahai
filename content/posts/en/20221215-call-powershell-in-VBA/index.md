+++
author = "DUAN DAHAI"
title = "Use VBA to run a Powershell"
date = "2022-12-15"
description = "Use VBA to run a Powershell"
tags = [
    "VBA",
    "Powershell"
]
categories = [
    "solutions"
]
+++
 
In an auto task VBA tool, I find that instead of VBA scripts,  
call a powershell file can use some more effective solutions.

So I share an example that call a Powershell file in VBA.
```VB
Dim command As String
Dim wsh As Object
Dim result As Long

command = "powershell -NoProfile -ExecutionPolicy Unrestricted "
command = command & "C:¥yourPowershellFile.ps1"

Set wsh = CreateObject("WScript.Shell")

result = wsh.Run(Command:=command, WindowStyle:=0, WaitOnReturn:=False)

If (result = 0) Then
    MsgBox ("command execute success!")
Else
    MsgBox ("command execute failed!")
End If

Set wsh = Nothing
```


#### Options
+ WindowStyle:=0  
    `not show execute window`
+ WaitOnReturn:=True  
    `wait for the script finish`


#### Other
You can also execute DOS command in VBA, like this sort a csv file command:
```
command = "sort /o  C:¥example.csv"
```