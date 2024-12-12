from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CodeDocsSearchTool

from crew_auditor.tools.github_tools import GithubCrewCodeFetcherTool
from crew_auditor.tools.report_writing_tool import ReportWritingTool


@CrewBase
class CrewAuditorEnhancingCodeQualityWithCrewaiCrew:
    """CrewAuditorEnhancingCodeQualityWithCrewai crew"""

    docs_search_tool = CodeDocsSearchTool(docs_url="https://docs.crewai.com/")

    @agent
    def information_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["information_collector"],  # type: ignore
            tools=[
                GithubCrewCodeFetcherTool(),
                self.docs_search_tool,
            ],
        )

    @agent
    def crewai_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["crewai_expert"],  # type: ignore
            tools=[
                self.docs_search_tool,
                ReportWritingTool(),
            ],
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
