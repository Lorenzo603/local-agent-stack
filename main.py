from agentos import agent_os, app

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)
