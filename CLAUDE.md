# CLAUDE.md — Project Instructions for Claude Code

## Project Overview

This is the **Local Agent Stack**, a Python + Next.js monorepo for building and running AI agents using the [Agno](https://docs.agno.com) framework. It consists of:

- **Backend** (Python 3.12): FastAPI-based AgentOS serving multiple AI agents, teams, and workflows via Ollama local models.
- **Frontend** (`agent-ui/`): Next.js 15 + React 18 + TypeScript chat UI using npm.

## Repository Layout

```
├── main.py              # Entrypoint — starts AgentOS (FastAPI via uvicorn)
├── agentos.py           # Agent/Team/Workflow definitions and AgentOS config
├── env_loader.py        # Minimal .env file loader
├── agents/              # Agent instruction files (Markdown)
│   ├── <agent_name>/
│   │   └── instructions.md
├── storage/             # SQLite DB storage (agno.db)
├── scripts/
│   └── start.sh         # Starts backend + frontend concurrently
├── agent-ui/            # Next.js frontend (separate sub-project)
│   ├── src/
│   │   ├── app/         # Next.js app router pages
│   │   ├── components/  # React components (chat, ui)
│   │   ├── hooks/       # Custom React hooks
│   │   ├── lib/         # Utilities
│   │   ├── types/       # TypeScript types
│   │   └── store.ts     # Zustand store
│   └── package.json
```

## Tech Stack & Dependencies

### Backend (Python)
- **Framework**: Agno (AgentOS, Agent, Team, Workflow)
- **Models**: Ollama (local LLMs), optional LlamaCpp
- **Database**: SQLite via `agno.db.sqlite.SqliteDb`
- **Tracing**: OpenTelemetry + OpenInference instrumentation
- **Server**: FastAPI (served by Agno's built-in uvicorn wrapper)
- **Env management**: Custom `env_loader.py` (reads `.env` with `os.environ.setdefault`)

### Frontend (TypeScript)
- **Framework**: Next.js 15 (App Router)
- **UI**: React 18, Tailwind CSS, Radix UI, Framer Motion
- **State**: Zustand
- **Markdown**: react-markdown + remark-gfm + rehype-raw/sanitize
- **Package manager**: npm

## Development Commands

### Backend
```bash
# Create and activate venv
uv venv --python 3.12
source .venv/bin/activate  # macOS/Linux

# Install dependencies
uv pip install -U agno openai sqlalchemy "fastapi[standard]"
uv pip install -U opentelemetry-api opentelemetry-sdk openinference-instrumentation-agno
uv pip install -U ollama PyJWT

# Run
python main.py
```

### Frontend
```bash
cd agent-ui
npm install
npm run dev          # Dev server on port 3000
npm run build        # Production build
npm run lint         # ESLint
npm run lint:fix     # ESLint autofix
npm run format       # Check formatting (Prettier)
npm run format:fix   # Fix formatting
npm run typecheck    # TypeScript check
npm run validate     # lint + format + typecheck
```

### Both
```bash
./scripts/start.sh    # Starts backend + frontend concurrently
```

## Code Conventions

### Python
- Use `Path().read_text(encoding="utf-8")` for reading files.
- Agent instructions live in `agents/<agent_name>/instructions.md`.
- Register agents/teams/workflows in `agentos.py` via the `AgentOS()` constructor.
- Environment variables loaded via `env_loader.load_env()` — default model is set by `MODEL_ID` env var.
- Use `os.environ.setdefault` pattern (don't overwrite existing env vars).

### TypeScript / React
- Use `'use client'` directive for client components.
- Components organized by domain: `components/chat/` for chat features, `components/ui/` for primitives.
- Barrel exports via `index.ts` in component folders.
- Tailwind for styling; use `cn()` utility from `lib/utils.ts` for class merging.
- State management via Zustand store in `store.ts`.

## Adding a New Agent

1. Create `agents/<agent_name>/instructions.md` with the agent's system prompt.
2. In `agentos.py`, instantiate a new `Agent(...)` with:
   - `model=Ollama(id=model_id)`
   - `db=db`
   - `name`, `description`, `instructions` (read from the markdown file)
3. Add the agent to the `agents=[]` list in the `AgentOS()` constructor.

## Important Notes

- The `agent-ui/` directory is gitignored from the root project — it's treated as a separate sub-project.
- SQLite database lives at `storage/agno.db`.
- The `.env` file at the project root holds secrets (API keys, `MODEL_ID`, etc.) — never commit it.
- The backend auto-reloads on file changes (`reload=True` in `agent_os.serve()`).
