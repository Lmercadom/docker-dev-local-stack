# Docker Local Stack

A reusable deployment foundation for Python web services. The goal is to solve
the deployment problem once so every future project just plugs in.

Each project follows the same contract — a FastAPI app with `/health` and `/run`
endpoints, wrapped in a consistent Dockerfile — so the infrastructure layer never
has to change between projects.

## Repositories

| Repo | Purpose |
|------|---------|
| [server-template](https://github.com/Lmercadom/server-template) | Starting point for every new project |
| [docker-local-stack](https://github.com/Lmercadom/docker-dev-local-stack) | Local orchestration for running multiple projects side by side |

## Structure

    docker-local-stack/
    └── local-platform/         # Run multiple projects behind one entry point
        ├── docker-compose.yml
        └── nginx/
            └── nginx.conf

## Starting a new project

1. Go to [server-template](https://github.com/Lmercadom/server-template) on GitHub
2. Click **Use this template** → **Create a new repository**
3. Clone your new repo and start coding:

```bash
git clone https://github.com/Lmercadom/my-new-project.git
cd my-new-project
docker compose up --build
```

Then:
1. Replace the `/run` logic in `app/main.py` with your actual code
2. Add your dependencies to `requirements.txt`
3. Rename the `title=` in `FastAPI(...)` to your project name

## Running multiple projects locally

When you have more than one project running at the same time, use the local
platform to route them through a single nginx entry point instead of juggling ports.

Add a service block in `local-platform/docker-compose.yml` and a matching
`location` block in `local-platform/nginx/nginx.conf`, then:

```bash
cd local-platform
docker compose up --build
```

- http://localhost/project-a/health
- http://localhost/project-b/health

## Dev container (VS Code)

Open any project cloned from `server-template` in VS Code and run
**Dev Containers: Reopen in Container**. VS Code will attach inside the running
container with hot-reload already active.

## Stack

- Python 3.11
- FastAPI + Uvicorn
- Docker + Docker Compose
- Nginx

## Roadmap

- [ ] AWS deployment via CDK (ECR + App Runner)
- [ ] GitHub Actions CI/CD pipeline