from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

import os

from helpers.llm_wrapper import get_llm, get_model_name

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

from tool_evaluator_agent.tools.scraping_fish_tool import ScrapingFishTool
scraping_fish_tool = ScrapingFishTool()

from datetime import datetime
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

llm=get_llm('gpt-4o')

@CrewBase
class ToolEvaluatorAgentCrew():
  """ToolEvaluatorAgent crew"""
  agents_config = 'config/agents.yaml'
  tasks_config = 'config/tasks.yaml'
  output_file_prefix = f'{current_datetime}_'
  # SPIKE: output dir needs /?
  output_dir = '/output'
  log_dir = 'logs'

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'],
      tools=[search_tool, scraping_fish_tool], 
      llm=llm,
      verbose=True,
      max_iter=25
    )

  @agent
  def report_producer(self) -> Agent:
    return Agent(
      config=self.agents_config['report_producer'],
      llm=llm,
      verbose=True,
      max_iter=25
    )
  
  @task
  def criteria_clarification_task(self) -> Task:
    agent = self.researcher()
    output_file = f'{self.output_dir}/{self.output_file_prefix}{get_model_name(agent.llm)}_criteria.md'
    print(f'>>> Criteria clarification task output file: {output_file}')
    return Task(
      config=self.tasks_config['criteria_clarification_task'],
      agent=agent,
      output_file=output_file
    )

  @task
  def research_task(self) -> Task:
    agent = self.researcher()
    output_file = f'{self.output_dir}/{self.output_file_prefix}{get_model_name(agent.llm)}_research.md'
    print(f'>>> Research task output file: {output_file}')
    return Task(
      config=self.tasks_config['research_task'],
      agent=agent,
      output_file=output_file
    )

  @task
  def reporting_task(self) -> Task:
    agent = self.report_producer()
    output_file = f'{self.output_dir}/{self.output_file_prefix}{get_model_name(agent.llm)}_report.md'
    print(f'>>> Reporting task output file: {output_file}')
    return Task(
      config=self.tasks_config['reporting_task'],
      agent=self.report_producer(),
      output_file=output_file
    )

  @crew
  def crew(self) -> Crew:
    """Creates the ToolEvaluatorAgent crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
      # manager_llm=ChatOpenAI(model="gpt-4"),
      verbose=True,
      output_log_file=f'{self.log_dir}/{self.output_file_prefix}tool_evaluator_agent_log.txt'
    )