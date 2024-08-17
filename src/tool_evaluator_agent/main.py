#!/usr/bin/env python
import sys
from tool_evaluator_agent.crew import ToolEvaluatorAgentCrew
from helpers.tracer import Tracer

from dotenv import load_dotenv


# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

load_dotenv()
        
tracer = Tracer()

crew_inputs = {
    'topic': 'plaforms for developmet of applications that use LLM',
    'criteria': '''
        - Support for agents
        - Low vendor lock-in
        - Support for higher end LLM models (e.g. GPT-4, Gemini, ...)
        - Support for zero cost models (e.g. Open Hermes, ...)
        - Good documentation
        - Strong community support
        - RAG support
        - Rich ecosystem of integrations and toolkits
        ''',
    'tools': '''
        - LangChain
        - phidata
        - CrewAI
        - Amazon Bedrock
        '''
}

def run():
    """
    Run the crew.
    """
    inputs = crew_inputs
    
    tracer.init(default_tags=['tool_evaluator_agent'])
    
    ToolEvaluatorAgentCrew().crew().kickoff(inputs=inputs)
    
    tracer.end()


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
