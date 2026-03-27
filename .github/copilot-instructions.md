# Copilot Workspace Instructions

## Project Overview

This is the **Local Agent Stack**, a Python + Next.js monorepo for AI agents using the Agno framework.

- **Backend**: Python 3.12, FastAPI via Agno AgentOS, Ollama local models, SQLite storage.
- **Frontend** (`agent-ui/`): Next.js 15, React 18, TypeScript, Tailwind CSS, pnpm.

## Repository Layout

- `main.py` — Entrypoint, starts AgentOS (FastAPI/uvicorn)
- `agentos.py` — Agent/Team/Workflow definitions and AgentOS config
- `env_loader.py` — Minimal .env loader
- `agents/<name>/instructions.md` — Agent system prompts
- `storage/` — SQLite DB
- `scripts/start.sh` — Concurrent backend + frontend launcher
- `agent-ui/` — Next.js frontend sub-project

## Code Conventions

### Python
- Python 3.12, use type hints where appropriate.
- Agent instructions are Markdown files in `agents/<agent_name>/instructions.md`.
- Read files with `Path().read_text(encoding="utf-8")`.
- Register agents/teams/workflows in `agentos.py` via `AgentOS()`.
- Environment: custom `env_loader.py` using `os.environ.setdefault`.
- Default model via `MODEL_ID` env var; model instantiation: `Ollama(id=model_id)`.
- Database: `SqliteDb(db_file="storage/agno.db")`.

### TypeScript / React
- Next.js 15 App Router with `'use client'` for client components.
- Components: `components/chat/` (domain), `components/ui/` (primitives).
- Barrel exports via `index.ts`.
- Styling: Tailwind CSS with `cn()` from `lib/utils.ts`.
- State: Zustand (`store.ts`).
- Package manager: pnpm.

## Development Commands

### Backend
```bash
source .venv/bin/activate
python main.py
```

### Frontend
```bash
cd agent-ui && pnpm run dev
```

### Validation
```bash
cd agent-ui && pnpm run validate  # lint + format + typecheck
```

## Adding a New Agent
1. Create `agents/<name>/instructions.md`.
2. In `agentos.py`, add `Agent(model=Ollama(id=model_id), db=db, name="...", description="...", instructions=Path("agents/<name>/instructions.md").read_text(encoding="utf-8"))`.
3. Register in the `AgentOS(agents=[...])` list.
