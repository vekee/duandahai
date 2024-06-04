+++
author = "DUAN DAHAI"
title = "Use CI/CD Pipeline for aws lambda and stepfunctions"
date = "2023-12-30"
description = "Use CI/CD Pipeline for aws lambda and stepfunctions"
tags = [
    "AWS",
    "CI/CD",
    "Lambda",
    "stepfunctions"
]
categories = [
    "solutions"
]
+++
 
In this case, I will share some points about use AWS SAM to deploy serverless applications on AWS.   
If you want to know the details or the base knowledge about CI/CD/SAM, you can ask ChatGPT or Google to get more professional answers.   

When you want to start with this blog, you need to prepared for this:   
* IAM role
* codecommit repository
* code build
* pipeline with only source and build is ok.

#### project structure
Create your project straucture like this.   
You can find all the config file example at below.   
```
├── src
│   ├── lambda
│   │   ├── hello-world-1
│   │   │   ├── lambda_function.py
│   │   │   └── config.json
│   │   └── hello-world-2
│   │       └── lambda_function.py
│   ├── statemachine
│   │   └── your-statemachine-config.json
├── templates
│   └── template.yml
├── buildspec.yml
├── samconfig.toml
└── template_statemachine_cf.py
```

#### samconfig.toml
Set the SAM config like this.
```
version = 0.1

[default]
  [default.build]
    [default.build.parameters]
      template = "templates/template.yml"
      base_dir = "src"
      s3_bucket = "deploy-1234567890"
      s3_prefix = "build"

  [default.deploy]
    [default.deploy.parameters]
      stack_name = "cfn-your-repository-name"
      region = "ap-northeast-1"
      capabilities = "CAPABILITY_NAMED_IAM"
      fail_on_empty_changeset = false
```

#### buildspec.yml
Set the build config like this.   
The importpant point is I use the `python template_statemachine_cf.py` for inject the statemachine json into template config before sam build.   
```
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9

  pre_build:
    commands:
      - echo "update statemachine json in samconfig.toml"
      - python template_statemachine_cf.py

  build:
    commands:
      - echo "Build started on $(date)"
      - sam build
      - echo "Deploying SAM application"
      - sam deploy

  post_build:
    commands:
      - echo Build completed on `date`
```

#### template.yml
Set the template like this.   
I use `Definition` to set the StateMachine json, before the sam build,    
Prebuild `python template_statemachine_cf.py` will replace the `statemachine/your-statemachine-config.json` as its json content.   
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  SAM Template

Globals:
  Function:
    Runtime: python3.9
    Timeout: 3
    MemorySize: 128
  
Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: hello-world-1
      CodeUri: lambda/hello-world-1/
      Description: 'hello-world-1 lambda'
      MemorySize: 128
      Timeout: 600
      Handler: lambda_function.lambda_handler
      Runtime: python3.9
      Architectures:
        - x86_64
      EventInvokeConfig:
        MaximumEventAgeInSeconds: 21600
        MaximumRetryAttempts: 2
      EphemeralStorage:
        Size: 512
      Environment:
        Variables:
          test: 'test'
      Layers:
        - arn:aws:lambda:ap-northeast-1:1234567890:layer:python39_layers:1
      RuntimeManagementConfig:
        UpdateRuntimeOn: Auto
      SnapStart:
        ApplyOn: None
      PackageType: Zip
      Role: 'arn:aws:iam::1234567890:role/your_role'
  TestStateMachine:
    Type: AWS::StepFunctions::StateMachine
    Properties: 
      StateMachineName: 'your-stepfunction-name'
      Definition: statemachine/your-statemachine-config.json
      RoleArn: 'arn:aws:iam::1234567890:role/your_role'
```

#### template_statemachine_cf.py
This is what the Prebuild doing.    
You can also add other action in this script like run unit test.
```
import sys
import glob
import os
import json


def read_sm_def (sm_def_json_file: str) -> dict:
    try:
        with open(f"{sm_def_json_file}", "r") as file:
            return json.load(file)
    except IOError as e:
        sys.exit(1)


def list_json_files(directory):
    json_files = glob.glob(os.path.join(directory, '*.json'))
    return json_files


template_yml_file = './templates/template.yml'
for json_file in list_json_files('./src/statemachine/'):
    json_file_name_with_extension = os.path.basename(json_file)
    sm_def_dict = read_sm_def(json_file)

    with open(template_yml_file, 'r') as file:
        yaml_data = file.read()
        updated_yaml_data = yaml_data.replace('statemachine/' + json_file_name_with_extension, json.dumps(sm_def_dict))

    with open(template_yml_file, 'w') as file:
        file.write(updated_yaml_data)
```

#### Reference
[Introducing AWS SAM Pipelines](https://aws.amazon.com/jp/blogs/compute/introducing-aws-sam-pipelines-automatically-generate-deployment-pipelines-for-serverless-applications/).   
[AWS::Serverless::StateMachine](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/sam-resource-statemachine.html).