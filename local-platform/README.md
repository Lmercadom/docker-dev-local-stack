# Local platform

This is the piece that lets you run several projects at once on your machine,
each reachable through one entry point instead of juggling ports.

This demo wires up two copies of `service-template` (`project-a` and
`project-b`) behind an nginx reverse proxy, just to prove the pattern out.
Once you have real projects, replace the `build:` paths with the real project
folders and rename the services to match.

## Running it

\`\`\`bash
docker compose up --build
\`\`\`

Then:
- http://localhost/project-a/health
- http://localhost/project-b/health
- http://localhost/project-a/docs

nginx strips the `/project-a/` prefix before forwarding, so each container
still just sees requests at `/health`, `/run`, etc. — it has no idea it's
sitting behind a proxy.

## Adding a new project

1. Add a service block in `docker-compose.yml` pointing `build:` at the
   project's folder (it needs to follow the same `service-template` shape).
2. Add a matching `location` block in `nginx/nginx.conf`.
3. `docker compose up --build` again.