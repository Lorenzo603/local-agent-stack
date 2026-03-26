"""
Web Application Generator — Multi-Agent Orchestration Workflow

Accepts a JSON specification describing a web application and autonomously
produces the complete application code, file structure, and dependency list
through a pipeline of specialised agents.

Usage:
    Import ``webapp_generator_workflow`` and register it with AgentOS, or
    run the module directly for a standalone dry-run.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.team.mode import TeamMode
from agno.workflow import Step, StepOutput, Workflow

from env_loader import load_env

load_env()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL_ID: str = os.getenv("MODEL_ID", "gemma3:4b")
DB_PATH: str = os.getenv("AGNO_DB_PATH", "storage/agno.db")

_db = SqliteDb(db_file=DB_PATH)
_model = Ollama(id=MODEL_ID)


def _load_instructions(agent_dir: str) -> str:
    """Read the instruction file for an agent directory under ``agents/``."""
    path = Path("agents") / agent_dir / "instructions.md"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

project_planner_agent = Agent(
    model=_model,
    db=_db,
    name="Project Planner",
    role="Project Planner",
    description=(
        "Analyses web-app specifications and produces a structured "
        "architecture plan covering file layout, tech stack, DB schema, "
        "API endpoints, frontend components, and dependencies."
    ),
    instructions=_load_instructions("webapp_project_planner"),
    markdown=True,
)

frontend_architect_agent = Agent(
    model=_model,
    db=_db,
    name="Frontend Architect",
    role="Frontend Architect",
    description=(
        "Generates all frontend source files (pages, components, styles, "
        "routing, state management) based on the architecture plan."
    ),
    instructions=_load_instructions("webapp_frontend_architect"),
    markdown=True,
)

backend_specialist_agent = Agent(
    model=_model,
    db=_db,
    name="Backend Specialist",
    role="Backend Specialist",
    description=(
        "Generates all backend source files (server, routes, middleware, "
        "models, validation) based on the architecture plan."
    ),
    instructions=_load_instructions("webapp_backend_specialist"),
    markdown=True,
)

database_engineer_agent = Agent(
    model=_model,
    db=_db,
    name="Database Engineer",
    role="Database Engineer",
    description=(
        "Generates database migration scripts, seed data, ORM models, "
        "and connection configuration from the architecture plan."
    ),
    instructions=_load_instructions("webapp_database_engineer"),
    markdown=True,
)

devops_engineer_agent = Agent(
    model=_model,
    db=_db,
    name="DevOps Engineer",
    role="DevOps Engineer",
    description=(
        "Produces Dockerfiles, CI/CD pipelines, environment templates, "
        "proxy configs, and a setup README."
    ),
    instructions=_load_instructions("webapp_devops_engineer"),
    markdown=True,
)

security_reviewer_agent = Agent(
    model=_model,
    db=_db,
    name="Security Reviewer",
    role="Security Reviewer",
    description=(
        "Audits all generated code for OWASP Top-10 vulnerabilities and "
        "outputs issues with suggested patches."
    ),
    instructions=_load_instructions("webapp_security_reviewer"),
    markdown=True,
)

integration_reviewer_agent = Agent(
    model=_model,
    db=_db,
    name="Integration Reviewer",
    role="Integration Reviewer",
    description=(
        "Verifies API contracts, data-model consistency, and routing "
        "alignment across frontend and backend code."
    ),
    instructions=_load_instructions("webapp_integration_reviewer"),
    markdown=True,
)

# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

code_generation_team = Team(
    model=_model,
    db=_db,
    name="Code Generation Team",
    mode=TeamMode.coordinate,
    members=[
        frontend_architect_agent,
        backend_specialist_agent,
        database_engineer_agent,
        devops_engineer_agent,
    ],
    instructions=(
        "You coordinate the code-generation agents. "
        "Delegate the architecture plan to each specialist and "
        "merge all generated file maps into a single consolidated JSON object."
    ),
    delegate_to_all_members=True,
    tool_call_limit=20,
)

review_team = Team(
    model=_model,
    db=_db,
    name="Review Team",
    mode=TeamMode.coordinate,
    members=[
        security_reviewer_agent,
        integration_reviewer_agent,
    ],
    instructions=(
        "You coordinate the review agents. "
        "Send all generated code to both reviewers, then merge their findings "
        "and patched files into a single consolidated JSON response with keys "
        "'issues' and 'patched_files'."
    ),
    delegate_to_all_members=True,
    tool_call_limit=20,
)


# ---------------------------------------------------------------------------
# Custom step functions
# ---------------------------------------------------------------------------

def validate_specs(step_input) -> StepOutput:
    """Parse and validate the incoming web-app specification JSON."""
    raw_input = step_input.input
    try:
        if isinstance(raw_input, str):
            specs = json.loads(raw_input)
        elif isinstance(raw_input, dict):
            specs = raw_input
        else:
            return StepOutput(
                content=None,
                success=False,
                error=f"Unsupported input type: {type(raw_input).__name__}. Expected JSON string or dict.",
            )

        if "web_app_specs" not in specs:
            return StepOutput(
                content=None,
                success=False,
                error="Missing required key 'web_app_specs' in input.",
            )

        return StepOutput(content=json.dumps(specs["web_app_specs"], indent=2))

    except json.JSONDecodeError as exc:
        return StepOutput(
            content=None,
            success=False,
            error=f"Invalid JSON input: {exc}",
        )


def assemble_output(step_input) -> StepOutput:
    """Merge generated code with review patches into the final deliverable."""
    generated_code = step_input.get_step_content("Code Generation")
    review_results = step_input.get_step_content("Code Review")

    # Build final payload
    final_output: Dict[str, Any] = {
        "generated_files": {},
        "review_issues": [],
        "dependencies": {},
    }

    # Parse generated code
    if generated_code:
        try:
            parsed = json.loads(generated_code) if isinstance(generated_code, str) else generated_code
            if isinstance(parsed, dict):
                final_output["generated_files"] = parsed
        except (json.JSONDecodeError, TypeError):
            final_output["generated_files"] = {"raw_output": str(generated_code)}

    # Overlay review patches
    if review_results:
        try:
            review = json.loads(review_results) if isinstance(review_results, str) else review_results
            if isinstance(review, dict):
                final_output["review_issues"] = review.get("issues", [])
                for path, content in review.get("patched_files", {}).items():
                    final_output["generated_files"][path] = content
        except (json.JSONDecodeError, TypeError):
            final_output["review_issues"] = [{"raw_review": str(review_results)}]

    return StepOutput(content=json.dumps(final_output, indent=2))


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

webapp_generator_workflow = Workflow(
    name="Web App Generator",
    description=(
        "End-to-end orchestration pipeline that transforms a JSON web-app "
        "specification into complete, reviewed application source code."
    ),
    db=_db,
    steps=[
        Step(
            name="Validate Specs",
            executor=validate_specs,
            max_retries=1,
            on_error="fail",
        ),
        Step(
            name="Architecture Planning",
            agent=project_planner_agent,
            max_retries=2,
            on_error="fail",
        ),
        Step(
            name="Code Generation",
            team=code_generation_team,
            max_retries=2,
            on_error="fail",
        ),
        Step(
            name="Code Review",
            team=review_team,
            max_retries=2,
            on_error="skip",
            skip_on_failure=True,
        ),
        Step(
            name="Assemble Output",
            executor=assemble_output,
            max_retries=1,
            on_error="fail",
        ),
    ],
)
