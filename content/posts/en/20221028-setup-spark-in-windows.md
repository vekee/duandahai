+++
author = "DUAN DAHAI"
title = "Simple setup spark in windows OS"
date = "2022-10-28"
description = "Simple setup spark in windows OS"
tags = [
    "spark-submit",
    "PySpark",
    "BigData"
]
categories = [
    "solutions"
]
+++

When you want to start learning about spark and try to write or run some scripts,
you needn't spent time to search the integration solution about spark environment,
you needn't confuse that you don't have a linux environment or a cloud service account.
Just take the integrated spark environment into your own PC, only one step setup, then you can use it.
and even you needn't to install anything in your PC.

This solution is win-spark-env, You can find it on <a href="https://github.com/vekee/win-spark-env" >github.</a>

Under the article, I will show how I use it.

### Download from <a href="https://github.com/vekee/win-spark-env" >github.</a>

- Copy the root folder Apache under C:¥
![save](/media/en/20220928-run-spark-in-windows-1.png)


### Set Up
- Open the Command Prompt as administrator, execute the __environment_variable_setup.bat__  under C:¥Apache¥Spark3.3¥tools
![run](/media/en/20220928-run-spark-in-windows-3.png)

### Run your spark script
- Run the example pyspark script by spark-submit in Command Prompt.
```
python C:¥Apache¥Spark3.3¥tools¥spark-3.3.0-bin-hadoop3¥bin¥spark-submit.py C:\Apache\Spark3.3\source\example.py
```
- Avoid the ouput folder permission problem, Suggest you open the Command Prompt as administrator.
![run](/media/en/20220928-run-spark-in-windows-5.png)

### Develop IDE
- Start the VSCode as administrator, install Python extension for VSCode.
`
C:\Apache\Spark3.3\tools\VSCode-win32-x64-1.72.0¥Code.exe
`
- Import the source folder.
`
C:\Apache\Spark3.3\source
`
- Run the example pyspark script in DEBUG model by spark-submit.
![run](/media/en/20220928-run-spark-in-windows-6.png)

### Example script result
- When executed the example script successfully, the result file will be create under output folder.
![run](/media/en/20220928-run-spark-in-windows-7.png)

### Other
You can change the root director to avoid permission problem.
1. Change the setted environment variable path
2. Grep all the files under `C:\Apache\Spark3.3\source`, update the path as you want change.

#### Reference
You can find more information on <a href="https://github.com/vekee/win-spark-env" >github.</a> If you have any question, you can submit an Issue on it.