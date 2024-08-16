from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from tool_evaluator_agent.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

@CrewBase
class ToolEvaluatorAgentCrew():
	"""ToolEvaluatorAgent crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[search_tool], 
			verbose=True
		)

	@agent
	def report_producer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_producer'],
			verbose=True
		)
  
	@task
	def criteria_clarification_task(self) -> Task:
		return Task(
			config=self.tasks_config['criteria_clarification_task'],
			agent=self.researcher()
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.report_producer(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ToolEvaluatorAgent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)