import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import GithubSearchTool
from crewai_tools import CodeDocsSearchTool

@CrewBase
class CrewAuditorEnhancingCodeQualityWithCrewaiCrew():
    """CrewAuditorEnhancingCodeQualityWithCrewai crew"""

    @agent
    def crewai_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['crewai_expert'],
            tools=[
                GithubSearchTool(
                    gh_token=os.environ.get('GH_TOKEN'),
                    content_types=['code'],
                ),
                CodeDocsSearchTool()
            ],
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'],
        )

    @task
    def fetch_crew_content(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_crew_content'],
        )

    @task
    def fetch_crewai_docs(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_crewai_docs'],
        )

    @task
    def fetch_crewai_source_code(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_crewai_source_code'],
        )

    @task
    def evaluate_crew(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_crew'],
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
