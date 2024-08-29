#!/usr/bin/env python
import sys

from tool_evaluator_agent.crew import ToolEvaluatorAgentCrew
from helpers.tracer import TracerFactory, TracerAnnotation

from dotenv import load_dotenv
load_dotenv()

tracer = TracerFactory.get_tracer()
tracer.provider = 'helicone'
tracer.annotation = TracerAnnotation(app='tool_evaluator_agent')

crew_inputs = {
    'topic': 'plaforms for development of applications that use LLM',
    'criteria': '''
        - Comprehensive support for the development of multi-step AI agents
        - Low vendor lock-in
        - Support for higher end LLM models (e.g. GPT-4, Gemini, ...)
        - Support for zero cost LLM models (e.g. Open Hermes, ...)
        - Good documentation
        - Strong community support
        - RAG (Retrieval-Augmented Generation) support
        - Rich ecosystem of integrations and toolkits
        ''',
    'tools': '''
        - Amazon Bedrock
        - CrewAI
        - LangChain
        - LangGraph
        - phidata
        ''',
}


def run():
    """
    Run the crew.
    """
    inputs = crew_inputs

    tracer.init()

    ToolEvaluatorAgentCrew().crew().kickoff(inputs=inputs)

    tracer.end()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = crew_inputs
    try:
        ToolEvaluatorAgentCrew().crew().train(n_iterations=int(sys.argv[1]),
                                              inputs=inputs)

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
