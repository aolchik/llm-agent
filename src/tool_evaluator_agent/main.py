#!/usr/bin/env python
import sys
from tool_evaluator_agent.crew import ToolEvaluatorAgentCrew

from dotenv import load_dotenv
import os
import agentops

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

load_dotenv()
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

crew_inputs = {
    'topic': 'plaforms for developmet of applications that use LLM',
    'criteria': '''
        - Support for agents
        - Low vendor lock-in
        - Support for higher end LLM models
        ''',
    'tools': '''
        - LangChain
        - phidata
        - CrewAI
        '''
}

def run():
    """
    Run the crew.
    """
    inputs = crew_inputs
    agentops.init(AGENTOPS_API_KEY, default_tags=["tool-evaluator-agent"])
    ToolEvaluatorAgentCrew().crew().kickoff(inputs=inputs)
    agentops.end_session("Success")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = crew_inputs
    try:
        ToolEvaluatorAgentCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ToolEvaluatorAgentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
