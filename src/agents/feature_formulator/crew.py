from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from helpers.llm_wrapper import get_llm, get_model_name, ModelParams
from helpers.tracer import Tracer
from datetime import datetime
from composio_crewai import ComposioToolSet, Action
from composio.utils import logging

current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

DEFAULT_LLM_PROVIDER = 'openai'
DEFAULT_LLM_MODEL = 'gpt-4o'
params: ModelParams = ModelParams(use_cache=False)

logging.setup(logging.LogLevel.DEBUG)
tool_set = ComposioToolSet()
gdocs_update_tools = tool_set.get_tools(actions=[
    Action.GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT,
    Action.GOOGLEDOCS_GET_DOCUMENT_BY_ID])


@CrewBase
class FeatureFormulatorCrewFactory():
    """FeatureFormulatorCrewFactory crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    output_file_prefix = f'{current_datetime}_feature_formulator_'
    # SPIKE: output dir needs /?
    output_dir = '/output'
    log_dir = 'logs'
    tracer: Tracer

    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'],
            tools=[],
            llm=get_llm(DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL, params),
            verbose=True,
            max_iter=25
        )

    @task
    def feature_specification_task(self) -> Task:
        agent = self.product_owner()
        output_file = f'{self.output_dir}'\
                      f'/{self.output_file_prefix}'\
                      f'{get_model_name(agent.llm)}_spec.md'
        return Task(
            config=self.tasks_config['feature_specification_task'],
            agent=agent,
            output_file=output_file
        )

    @task
    def previous_spec_review_task(self) -> Task:
        agent = self.product_owner()
        output_file = f'{self.output_dir}'\
                      f'/{self.output_file_prefix}'\
                      f'{get_model_name(agent.llm)}_spec_review.md'
        return Task(
            config=self.tasks_config['previous_spec_review_task'],
            agent=agent,
            tools=gdocs_update_tools,
            output_file=output_file
        )

    @crew
    def crew(self, agents=None, tasks=None) -> Crew:
        """Creates the FeatureFormulatorAgent crew"""
        agents = agents if agents else self.agents
        tasks = tasks if tasks else self.tasks
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            output_log_file=f'{self.log_dir}/'
                            f'{self.output_file_prefix}'
                            'feature_formulator_log.txt'
        )
