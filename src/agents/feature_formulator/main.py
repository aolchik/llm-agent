#!/usr/bin/env python
import os
import sys

from agents.feature_formulator.crew import FeatureFormulatorCrewFactory
from helpers import read_yaml, TracerFactory, TracerAnnotation

from dotenv import load_dotenv
load_dotenv()

tracer = TracerFactory.get_tracer()
tracer.provider = 'helicone'
tracer.annotation = TracerAnnotation(app='tool_evaluator_agent')


crew_inputs = read_yaml(
    f"input/{os.getenv('LLMAGENT_FEATURE_FORMULATOR_CONFIG')}")['crew_inputs']


def run():
    """
    Run the crew.
    """
    inputs = crew_inputs

    tracer.init()

    FeatureFormulatorCrewFactory().crew().kickoff(inputs=inputs)

    tracer.end()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = crew_inputs
    try:
        FeatureFormulatorCrewFactory().crew()\
            .train(n_iterations=int(sys.argv[1]),
                   inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FeatureFormulatorCrewFactory().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew.
    """
    inputs = crew_inputs
    try:
        tracer.init()
        FeatureFormulatorCrewFactory().crew().test(n_iterations=2,
                                                   openai_model_name='gpt-4o',
                                                   inputs=inputs)
        tracer.end()

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
