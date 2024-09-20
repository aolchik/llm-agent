from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from helpers.llm_wrapper import get_llm, get_model_name, ModelParams
from helpers.tracer import Tracer
from crewai_tools import SerperDevTool
from agents.tool_evaluator.tools import ScrapingFishTool
from datetime import datetime

# Check our tools documentations for more information on how to use them
search_tool = SerperDevTool()

scraping_fish_tool = ScrapingFishTool()

current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

DEFAULT_LLM_PROVIDER = 'openai'
DEFAULT_LLM_MODEL = 'gpt-3.5-turbo-1106'
params: ModelParams = ModelParams(use_cache=False)


@CrewBase
class ToolEvalCrewFactory():
    """ToolEvalCrewFactory crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    output_file_prefix = f'{current_datetime}_'
    # SPIKE: output dir needs /?
    output_dir = '/output'
    log_dir = 'logs'
    tracer: Tracer

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[search_tool, scraping_fish_tool],
            llm=get_llm(DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL, params),
            verbose=True,
            max_iter=25
        )

    @agent
    def report_producer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_producer'],
            llm=get_llm(DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL, params),
            verbose=True,
            max_iter=25
        )

    @task
    def criteria_clarification_task(self) -> Task:
        agent = self.researcher()
        output_file = f'{self.output_dir}'\
                      f'/{self.output_file_prefix}'\
                      f'{get_model_name(agent.llm)}_criteria.md'
        return Task(
            config=self.tasks_config['criteria_clarification_task'],
            agent=agent,
            output_file=output_file
        )

    @task
    def research_task(self) -> Task:
        agent = self.researcher()
        output_file = f'{self.output_dir}'\
                      f'{self.output_file_prefix}'\
                      f'{get_model_name(agent.llm)}_research.md'
        return Task(
            config=self.tasks_config['research_task'],
            agent=agent,
            output_file=output_file
        )

    @task
    def reporting_task(self) -> Task:
        agent = self.report_producer()
        output_file = f'{self.output_dir}'\
                      f'/{self.output_file_prefix}'\
                      f'{get_model_name(agent.llm)}_report.md'
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.report_producer(),
            output_file=output_file
        )

    @crew
    def crew(self, agents=None, tasks=None) -> Crew:
        """Creates the ToolEvaluatorAgent crew"""
        agents = agents if agents else self.agents
        tasks = tasks if tasks else self.tasks
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            # process=Process.hierarchical,
            # manager_llm=get_llm("openai", "gpt-4o"),
            verbose=True,
            memory=True,
            output_log_file=f'{self.log_dir}/'\
                            f'{self.output_file_prefix}'\
                            'tool_evaluator_agent_log.txt'
        )
