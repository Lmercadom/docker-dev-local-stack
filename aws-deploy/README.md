# AWS Deploy

CDK app that deploys any project built from `service-template` to AWS App
Runner. Builds the Docker image locally, pushes it to ECR, and stands up a
public HTTPS endpoint — all from one command.

This is the AWS counterpart to `docker-local-stack`: same project shape,
different destination.

## Prerequisites

- Docker running locally (images are built on your machine before pushing)
- AWS CLI configured via IAM Identity Center (`aws sso login --profile personal`)
- CDK bootstrapped once per account/region:

```bash
export AWS_PROFILE=personal
cdk bootstrap aws://ACCOUNT_ID/us-west-2
```

## Structure

    aws-deploy/
    ├── app.py                    # Entry point -- picks which project to deploy
    ├── cdk.json                  # Tells CDK how to run app.py
    ├── requirements.txt
    └── stacks/
        ├── __init__.py
        └── apprunner_stack.py    # The actual infrastructure definition

## Setup

```bash
cd aws-deploy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Deploying a project

By default, `app.py` deploys `../service-template`. To deploy a different
project, pass its path at deploy time:

```bash
cdk deploy --context project_path=../my-other-project
```

The project folder just needs a Dockerfile and a `/health` endpoint on port
8000 — the same contract every `service-template`-based project already
follows.

First deploy takes a few minutes. CDK prints the public `ServiceUrl` when
it's done.

## Redeploying after a code change

```bash
cdk deploy
```

CDK fingerprints the project folder — if nothing changed, it skips the
rebuild. If something did, it rebuilds, re-pushes, and updates the running
service.

## Tearing down

App Runner isn't free to leave running. Tear down services you're not
actively demoing:

```bash
cdk destroy
```

This removes the App Runner service, the ECR repo it used, and the IAM role
-- nothing is left running or billing after this completes.

## What's actually deployed

- **ECR repository** — holds the built Docker image
- **IAM role** — scoped narrowly to let App Runner pull from that one ECR repo
- **App Runner service** — runs the container, checks `/health` every 10s,
  sized at the smallest available tier (0.25 vCPU / 0.5 GB) to keep cost down

## Stack

- Python 3.11
- AWS CDK v2
- App Runner, ECR, IAM

## Roadmap

- [ ] GitHub Actions workflow to deploy on push to main
- [ ] Parameterize instance size per project
- [ ] Custom domain support