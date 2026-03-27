---
description: "Create a new Agno team composed of multiple agents. Use when asked to add, create, or scaffold a new team."
---

# New Team

Create a new Agno team for the Local Agent Stack.

## Steps

1. **Define member agents** in `agentos.py` (or reference existing ones):
   ```python
   agent_a = Agent(
       name="{{agent_a_name}}",
       role="{{agent_a_role}}",
   )
   agent_b = Agent(
       name="{{agent_b_name}}",
       role="{{agent_b_role}}",
   )
   ```

2. **Create the team** in `agentos.py`:
   ```python
   {{name}}_team = Team(
       model=Ollama(id=model_id),
       name="{{display_name}}",
       members=[agent_a, agent_b],
       instructions="{{delegation_instructions}}",
       tool_call_limit=5,
   )
   ```

3. **Register in AgentOS** — add to the `teams=[...]` list in the `AgentOS()` constructor.

4. **Verify** the backend starts: `python main.py`.
