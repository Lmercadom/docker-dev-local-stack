#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks.apprunner_stack import AppRunnerStack

app = cdk.App()

# Path to the project folder to deploy -- must contain a Dockerfile.
# Change this per project, or override with -c project_path=../my-other-project
project_path = app.node.try_get_context("project_path") or "../service-template"

AppRunnerStack(
    app, "ServiceTemplateAppRunnerStack",
    project_path=project_path,
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

app.synth()