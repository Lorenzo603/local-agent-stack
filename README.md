# Local Agent Stack

Bootstrap guide (Agno): https://docs.agno.com/first-agent

## Install

Create and activate a Python 3.12 venv:

```bash
uv venv --python 3.12
.venv\Scripts\activate
```

Install dependencies:

```bash
uv pip install -U agno openai sqlalchemy "fastapi[standard]"
```

Telemetry dependencies

```bash
uv pip install -U opentelemetry-api opentelemetry-sdk openinference-instrumentation-agno
```

Custom models

```bash
uv pip install -U ollama
```

Other dependencies:

```bash
uv pip install -U jwt PyJWT
```

## Run

Start the agent:

```bash
python agentos.py
```

## UI

Agent UI docs: https://docs.agno.com/other/agent-ui

Install:

```bash
npx create-agent-ui@latest
```

Run:

```bash
cd agent-ui && npm run dev
```