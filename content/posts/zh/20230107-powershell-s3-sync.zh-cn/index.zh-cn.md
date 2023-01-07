+++
author = "DUAN DAHAI"
title = "Windows下使用Powershell同步S3上的存储文件"
date = "2023-01-07"
description = "Windows下使用Powershell同步S3上的存储文件"
tags = [
    "AWS",
    "S3",
    "powershell"
]
categories = [
    "解决方案"
]
+++

#### 概要

一直想利用AWS S3作为文件服务器，并可以和本地文件自动保持同步，主要考虑Windows下（没错，就是像Onedrive那样的）。   
稍微考虑一下后，试着做了一个粗劣版本出来，感觉不是很满意，又搜索一下相关解决方案，结果发现已经有[老美公司](https://www.gladinet.com/cn/amazon-s3/amazon-s3-file-server/)把它作为成熟产品推广了，真是感慨为啥想做个什么都是慢别人几年呢。

虽然找到了其他可行的替代方案，就是直接用[winscp](https://winscp.net/eng/download.php)连接到AWS S3，可以更方便的上传下载，但还是将这次的想法记录下来吧。

#### Windows下将S3作为文件服务器的实现构想

最容易想到的便是，针对每次文件的变更操作创建一个S3的同期请求。  
但Windows下如何获取文件的变更操作，是否有一些文件操作的触发器之类的东西?  
一头雾水的我埋入搜索的海洋，发现了还真有针对文件的监听接口，为了方便同时使用AWS CLI，我选择了powershell进行实现这次的构想。

#### 详细实现介绍

Powershell中可以使用FileSystemWatcher对文件夹进行动作监听，动作分类为
`Created`，`Changed`，`Deleted`，`Renamed`，所以我在各个动作中进行各自的S3文件同期操作。

由于担心不小心删除本地同期文件夹，S3上的所有文件也被删除了的情况，所以在`Deleted`动作中，会先把要删除的文件备份到其他bucket中。

代码中将下面必要的项目作为参数传入了，当然你也可以直接写进代码中。  
watchPath： 同期的文件夹  
watchBucket： 同期S3的bucket名  
backupBucket： 备份S3的bucket名  

下面代码可以直接使用，建议在必要处用`Write-Host`加入调试输出。

#### Powershell文件启动
```
PowerShell -ExecutionPolicy RemoteSigned D:\watch.ps1 "D:\s3-sync-test" "s3-sync-test" "s3-sync-test-backup"
```

#### Powershell实现代码
```powershell
Param(
    [String]$watchPath,
    [String]$watchBucket,
    [String]$backupBucket
)

try {
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $watchPath
    $watcher.Filter = "*"
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents   = $true

    $action = {
        $path = $Event.SourceEventArgs.FullPath
        $changeType = $Event.SourceEventArgs.ChangeType
        $oldPath = $Event.SourceEventArgs.OldFullPath
        
        $s3key = $path.Substring($watchPath.Length, $path.Length - $watchPath.Length)
        $s3key = $s3key.Replace("\","/")
        
        if ($changeType -eq "Created") {
            $cpCommand = 'aws s3 cp "' + $path + '" "s3://' + $watchBucket + $s3key + '"'
            cmd.exe /c $cpCommand
        }
        
        if ($changeType -eq "Changed") {
            $cpCommand = 'aws s3 cp "' + $path + '" "s3://' + $watchBucket + $s3key + '"'
            cmd.exe /c $cpCommand
        }
        
        if ($changeType -eq "Deleted") {
            $systemYmd = Get-Date -Format "yyyyMMdd"
            $cpCommand = 'aws s3 cp "s3://' + $watchBucket + $s3key + '" ' + '"s3://' + $backupBucket + '/' + $systemYmd + '/' + $watchBucket + $s3key + '"'
            cmd.exe /c $cpCommand
             
            $cpCommand = 'aws s3 rm "s3://' + $watchBucket + $s3key + '"'
            cmd.exe /c $cpCommand
        }
        
        if ($changeType -eq "Renamed") {
            $s3oldkey = $oldPath.Substring($watchPath.Length, $oldPath.Length - $watchPath.Length)
            $s3oldkey = $s3oldkey.Replace("\","/")
            
            $cpCommand = 'aws s3 rm "s3://' + $watchBucket + $s3oldkey + '"'
            cmd.exe /c $cpCommand
            
            $cpCommand = 'aws s3 cp "' + $path + '" "s3://' + $watchBucket + $s3key + '"'
            cmd.exe /c $cpCommand
        }   
    }

    $handlers = . {
       Register-ObjectEvent -InputObject $watcher -EventName Created -SourceIdentifier ("_FileWatcher_Created_") -Action $action
       Register-ObjectEvent -InputObject $watcher -EventName Changed -SourceIdentifier ("_FileWatcher_Changed_") -Action $action
       Register-ObjectEvent -InputObject $watcher -EventName Deleted -SourceIdentifier ("_FileWatcher_Deleted_") -Action $action
       Register-ObjectEvent -InputObject $watcher -EventName Renamed -SourceIdentifier ("_FileWatcher_Renamed_") -Action $action
    }

    $watcher.EnableRaisingEvents = $true

    do {
        Wait-Event -Timeout 1
        Write-Host "." -NoNewline
    } while ($true)
} finally {
    $watcher.EnableRaisingEvents = $false
    
    $handlers | ForEach-Object {
      Unregister-Event -SourceIdentifier $_.Name
    }
    
    $handlers | Remove-Job
    
    $watcher.Dispose()
    
    Write-Warning "Event Handler disabled, monitoring ends."
}
```

#### 本文未言及事项
+ AWS S3创建、AWS IAM设置
+ Windows下AWS CLI安装设置、S3同期command介绍
+ Powershell中的函数说明，ps1文件运行，调试

#### 上述代码未实现事项
+ 多个客户端对同一个文件变更时的Lock处理
+ S3文件对本地的反向同期
+ Powershell如何作为一个服务使用等问题

#### 参考資料
* https://powershell.one/tricks/filesystem/filesystemwatcher
* https://junjun777.hatenablog.com/entry/20141203/powershell_filesystem_watcher
* https://tex2e.github.io/blog/powershell/Register-ObjectEvent