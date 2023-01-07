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







