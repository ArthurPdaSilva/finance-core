# Finance Core Development Guide

## Project Layout

- `backend/`: FastAPI, SQLAlchemy, LangGraph, RAG and database seed.
- `frontend/`: Next.js application and server actions.
- `docker-compose.yml`: local PostgreSQL, backend, frontend and self-hosted Langfuse orchestration.

## Local Conventions

- Keep secrets in ignored `.env` files or environment variables.
- Keep the frontend API URL configurable through `API_URL`.
- Use `http://backend:8000` for frontend-to-backend calls inside Docker Compose.
- Use `http://127.0.0.1:8000` when running the frontend outside Docker.
- Use `http://langfuse-web:3000` for backend-to-Langfuse calls inside Docker Compose.
- Open the Langfuse dashboard at `http://localhost:3001` from the host.
- Do not commit generated databases, vector stores, build output or dependencies.

## Validation

Run the Docker stack before changing integration behavior:

```bash
docker compose config
docker compose up --build
docker compose logs -f langfuse-web langfuse-worker
```

For backend changes:

```bash
cd backend
uv lock --check
uv run ruff check src
```

For frontend changes:

```bash
cd frontend
pnpm typecheck
pnpm build
```

## Safety

- Never print or commit the contents of `.env` files.
- Do not replace local user changes while fixing the project.
- Keep database initialization explicit through `/init-db`; it resets seeded financial and chat tables.
