import os
from pathlib import Path

from agno.agent import Agent
from agno.team import Team
from agno.workflow import Step, Workflow, StepOutput
from agno.os import AgentOS
from agno.models.ollama import Ollama
from agno.models.llama_cpp import LlamaCpp
from agno.db.sqlite import SqliteDb
from agno.tracing import setup_tracing

from env_loader import load_env
from webapp_generator import webapp_generator_workflow

load_env()

db = SqliteDb(db_file=os.getenv("AGNO_DB_PATH", "storage/agno.db"))

setup_tracing(db=db) # Call this once at startup

model_id = os.getenv("MODEL_ID", "gemma3:4b")

jira_ticket_enhancer_agent = Agent(
    model=Ollama(id=model_id),
    # model=LlamaCpp(id="cyankiwi/Minimax-REAP", base_url="http://127.0.0.1:8001/v1"), # unsloth/MiniMax-M2.5, cyankiwi/Minimax-REAP
    db=db,
    name="Jira Ticket Enhancer",
    description="Analyze and review the input in order to translate it into a Jira task with a title and description.",
    instructions="instructions template",
)

# jira_ticket_enhancer_agent.print_response("can i use node running in docker to compile an app leaving on my os?", stream=True)


news_agent = Agent(
    name="News Agent",
    role="Analyzes tech news",
)

finance_agent = Agent(
    name="Finance Agent",
    role="Analyzes financial data",
)

research_team = Team(
    model=Ollama(id=model_id),
    name="Research Team",
    members=[news_agent, finance_agent],
    instructions="Delegate to the appropriate agent based on the request. Always start your response back to the question with the name of the agent you have delegated to, followed by a colon",
    tool_call_limit=5,
)

def data_preprocessor(step_input):
    # Custom preprocessing logic

    # Or you can also run any agent/team over here itself
    # response = some_agent.run(...)
    return StepOutput(content=f"Processed: {step_input.previous_step_content}") # <-- Now pass the agent/team response in content here

workflow = Workflow(
    name="Mixed Execution Pipeline",
    steps=[
        research_team,          # Team
        data_preprocessor,      # Function
        jira_ticket_enhancer_agent,  # Agent
    ]
)

agent_os = AgentOS(
    db=db,
    agents=[
        jira_ticket_enhancer_agent, 
    ],
    teams=[research_team],
    workflows=[workflow, webapp_generator_workflow],
)
app = agent_os.get_app()

