from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectorySearchTool

from crew_auditor.tools.git_hub_code_fetcher_tool import GitHubCodeFetcherTool
from crew_auditor.tools.report_writing_tool import ReportWritingTool


@CrewBase
class CrewAuditorEnhancingCodeQualityWithCrewaiCrew:
    """CrewAuditorEnhancingCodeQualityWithCrewai crew"""

    @agent
    def code_fetcher(self) -> Agent:
        return Agent(
            config=self.agents_config["code_fetcher"],  # type: ignore
            tools=[GitHubCodeFetcherTool()],
        )

    @agent
    def crewai_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["crewai_expert"],  # type: ignore
            tools=[DirectorySearchTool(directory="crewai-docs"), ReportWritingTool()],
        )

    # @agent
    # def report_reviewer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["report_reviewer"],  # type: ignore
    #     )

    @task
    def fetch_crew_content(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_crew_content"],  # type: ignore
        )

    @task
    def fetch_crewai_docs(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_crewai_docs"],  # type: ignore
        )

    @task
    def evaluate_crew(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_crew"],  # type: ignore
        )

    # @task
    # def review_report(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["review_report"],  # type: ignore
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewAuditorEnhancingCodeQualityWithCrewai crew"""
        return Crew(
            agents=self.agents,  # type: ignore
            tasks=self.tasks,  # type: ignore
            process=Process.sequential,
            verbose=True,
        )
