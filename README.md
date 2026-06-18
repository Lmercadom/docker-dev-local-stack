# Docker Local Stack

A reusable deployment foundation for Python web services. The goal is to solve
the deployment problem once so every future project just plugs in.

Each project follows the same contract — a FastAPI app with `/health` and `/run`
endpoints, wrapped in a consistent Dockerfile — so the infrastructure layer never
has to change between projects.

## Structure

    docker-local-stack/
    ├── service-template/       # Clone this for every new project
    │   ├── app/
    │   │   ├── __init__.py
    │   │   └── main.py
    │   ├── .devcontainer/
    │   │   └── devcontainer.json
    │   ├── Dockerfile
    │   ├── .dockerignore
    │   ├── docker-compose.yml
    └── local-platform/         # Run multiple projects behind one entry point
        ├── docker-compose.yml
        └── nginx/
            └── nginx.conf


## Quickstart

### Single project

```bash
cd service-template
docker compose up --build
```

- http://localhost:8000/health
- http://localhost:8000/docs

### Multiple projects via nginx

```bash
cd local-platform
docker compose up --build
```

- http://localhost/project-a/health
- http://localhost/project-b/health

## Starting a new project

```bash
cp -r service-template my-new-project
cd my-new-project
```

Then:
1. Replace the `/run` logic in `app/main.py` with your actual code
2. Add your dependencies to `requirements.txt`
3. Rename the `title=` in `FastAPI(...)` to your project name
4. `docker compose up --build`

To add it to the local platform, add a service block in
`local-platform/docker-compose.yml` and a matching `location` block in
`local-platform/nginx/nginx.conf`.

## Dev container (VS Code)

Open `service-template/` in VS Code and run
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