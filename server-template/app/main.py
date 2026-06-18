from fastapi import FastAPI
from pydantic import BaseModel

# Rename "service-template" below to your actual project name.
app = FastAPI(title="service-template", version="0.1.0")


class RunRequest(BaseModel):
    payload: dict


@app.get("/health")
def health() -> dict:
    """Used by Docker, AWS, and load balancers to check the service is alive."""
    return {"status": "ok"}


@app.post("/run")
def run(request: RunRequest) -> dict:
    """
    Replace this with your project's actual logic.
    Every project keeps this same /health + /run shape so the deployment
    layer (docker-compose locally, App Runner on AWS) never has to change.
    """
    return {"received": request.payload, "result": "replace with project logic when ready"}