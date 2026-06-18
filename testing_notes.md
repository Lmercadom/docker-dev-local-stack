# Guide to test the configuration

# Stage 1 - Test the app directly (no Docker needed)
From inside service-template/:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://localhost:8000/docs in your browser. FastAPI auto-generates an interactive UI where you can hit both endpoints without writing any curl commands — expand /health, click "Try it out", execute. Same for /run, but paste this as the request body:

{"payload": {"hello": "world"}}

This stage is worth doing first because if something breaks here, you know it's a Python problem, not a Docker problem.

## Stage 2 — Test the image build (no compose, just Docker)

docker build -t service-template .
docker run -p 8000:8000 service-template

Hit http://localhost:8000/health again. This is the closest thing to how it'll run in production — no volume mounts, no --reload, just the image as built. If it works here but fails later on AWS, the problem is in the infrastructure, not the image.

## Stage 3 — Test via compose (the actual dev workflow)
docker compose up --build

## Optionally, test from the terminal with curl
If you prefer not using the browser UI:

curl http://localhost:8000/health

curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"payload": {"hello": "world"}}'