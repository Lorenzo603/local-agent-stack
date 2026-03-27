---
description: "Create a new Agno agent. Use when asked to add, create, or scaffold a new AI agent."
---

# New Agent

Create a new agent for the Local Agent Stack.

## Steps

1. **Create the instructions file** at `agents/{{name}}/instructions.md`:
   - Write a system prompt that clearly defines the agent's role, capabilities, and output format.
   - Use Markdown with clear section headers.

2. **Register the agent** in `agentos.py`:
   ```python
   {{name}}_agent = Agent(
       model=Ollama(id=model_id),
       db=db,
       name="{{display_name}}",
       description="{{description}}",
       instructions=Path("agents/{{name}}/instructions.md").read_text(encoding="utf-8"),
       markdown=True,
   )
   ```

3. **Add to AgentOS** — append the new agent variable to the `agents=[...]` list in the `AgentOS()` constructor at the bottom of `agentos.py`.

4. **Verify** the backend starts without errors: `python main.py`.
