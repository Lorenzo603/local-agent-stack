---
description: "Create a new Agno workflow with sequential steps (agents, teams, or functions). Use when asked to add, create, or scaffold a new workflow."
---

# New Workflow

Create a new Agno workflow for the Local Agent Stack.

## Steps

1. **Define or reference the steps** — each step can be an Agent, Team, or a plain function:
   ```python
   def {{step_name}}(step_input):
       # Custom logic
       return StepOutput(content=f"Result: {step_input.previous_step_content}")
   ```

2. **Create the workflow** in `agentos.py`:
   ```python
   {{name}}_workflow = Workflow(
       name="{{display_name}}",
       steps=[
           some_agent,        # Agent step
           some_team,         # Team step
           {{step_name}},     # Function step
       ],
   )
   ```

3. **Register in AgentOS** — add to the `workflows=[...]` list in the `AgentOS()` constructor.

4. **Verify** the backend starts: `python main.py`.
