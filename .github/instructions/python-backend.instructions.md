---
applyTo: "**/*.py"
description: "Python backend conventions for the Agno agent framework. Use when editing Python files."
---

# Python Backend Conventions

- Python 3.12 with type hints.
- Agents are defined in `agentos.py` and use `agno.agent.Agent`.
- Models: `Ollama(id=model_id)` where `model_id` comes from `os.getenv("MODEL_ID", "gemma3:4b")`.
- Database: `SqliteDb(db_file="storage/agno.db")`.
- Agent instructions are stored as Markdown in `agents/<agent_name>/instructions.md` and read via `Path(...).read_text(encoding="utf-8")`.
- Environment loading: use `env_loader.load_env()` which calls `os.environ.setdefault` (never overwrites).
- Tracing: `agno.tracing.setup_tracing(db=db)` is called once at startup.
- New agents must be registered in the `AgentOS(agents=[...])` list in `agentos.py`.
