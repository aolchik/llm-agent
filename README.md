# ToolEvaluatorAgent Crew

Welcome to the ToolEvaluatorAgent Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```

### Composio.dev

To be able to run agents that write to Google Docs, the composio.dev scopes need to be augmented with the following list:
```
https://www.googleapis.com/auth/documents,
https://www.googleapis.com/auth/userinfo.email,
https://www.googleapis.com/auth/drive
```

This correction should be performed before to connection your Google account, in Integrations > Settings.

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/tool_evaluator_agent/config/agents.yaml` to define your agents
- Modify `src/tool_evaluator_agent/config/tasks.yaml` to define your tasks
- Modify `src/tool_evaluator_agent/crew.py` to add your own logic, tools and specific args
- Modify `src/tool_evaluator_agent/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run tool_evaluator
```

This command initializes the tool-evaluator-agent Crew, assembling the agents and assigning them tasks as defined in your configuration.


## Replaying Tasks

Too check tasks IDs, run this from src folder of your project:

```bash
crewai log-tasks-outputs
```

To replay a task, run this from src folder of your project:

```bash
crewai replay -t <task_id>
```

## Testing your Agent


## Checking your Source Code

To test your source code, run this from the root folder of your project:

```bash
poetry run pytest
```

To lint your source code, run this from the root folder of your project:

```bash
poetry run flake8
```

## Understanding Your Crew

The tool-evaluator-agent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the ToolEvaluatorAgent Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

