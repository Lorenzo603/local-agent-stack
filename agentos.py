from agno.agent import Agent
from agno.os import AgentOS
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.tracing import setup_tracing

db = SqliteDb(db_file="storage/agno.db")

setup_tracing(db=db) # Call this once at startup

agent = Agent(
    model=Ollama(id="gemma3:4b"),
    db=db,
    name="Jira Agent",
    description="Analyze and review the input in order to translate it into a Jira task with a title and description.",
    instructions="Take the following input and create the title and description for a Jira task:  ",
    markdown=True
)

# agent.print_response("can i use node running in docker to compile an app leaving on my os?", stream=True)


agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)
