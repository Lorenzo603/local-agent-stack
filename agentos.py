import os
from pathlib import Path

from agno.agent import Agent
from agno.os import AgentOS
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.tracing import setup_tracing

from env_loader import load_env

load_env()

db = SqliteDb(db_file="storage/agno.db")

setup_tracing(db=db) # Call this once at startup

model_id = os.getenv("MODEL_ID", "gemma3:4b")

jira_ticket_enhancer_agent = Agent(
    model=Ollama(id=model_id),
    db=db,
    name="Jira Ticket Enhancer",
    description="Analyze and review the input in order to translate it into a Jira task with a title and description.",
    instructions="Take the following input and create the title and description for a Jira task:  ",
    markdown=True
)

# jira_ticket_enhancer_agent.print_response("can i use node running in docker to compile an app leaving on my os?", stream=True)

prompt_enhancer_agent = Agent(
    model=Ollama(id=model_id),
    db=db,
    name="Prompt Enhancer",
    description="Improve the prompts received as input to optimize them for use with an LLM.",
    instructions=Path("agents/prompt_enhancer/instructions.md").read_text(encoding="utf-8"),
)

email_enhancer_agent = Agent(
    model=Ollama(id=model_id),
    db=db,
    name="Email Enhancer",
    description="Improve and refine email text to be friendly, pleasant, and straight to the point.",
    instructions=Path("agents/email_enhancer/instructions.md").read_text(encoding="utf-8"),
)

agent_os = AgentOS(agents=[jira_ticket_enhancer_agent, prompt_enhancer_agent, email_enhancer_agent])

