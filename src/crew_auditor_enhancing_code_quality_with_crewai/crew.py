from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import GithubSearchTool
from crewai_tools import CodeDocsSearchTool

@CrewBase
class CrewAuditorEnhancingCodeQualityWithCrewaiCrew():
    """CrewAuditorEnhancingCodeQualityWithCrewai crew"""

    @agent
    def repo_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['repo_analyzer'],
            
        )

    @agent
    def best_practices_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['best_practices_checker'],
            
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'],
            
        )


    @task
    def fetch_repository_content(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_repository_content'],
            tools=[GithubSearchTool()],
        )

    @task
    def evaluate_code_structure(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_code_structure'],
            
        )

    @task
    def check_against_best_practices(self) -> Task:
        return Task(
            config=self.tasks_config['check_against_best_practices'],
            tools=[CodeDocsSearchTool()],
        )

    @task
    def calculate_quality_score(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_quality_score'],
            
        )

    @task
    def generate_detailed_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_detailed_report'],
            
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewAuditorEnhancingCodeQualityWithCrewai crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
