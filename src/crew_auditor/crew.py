from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CodeDocsSearchTool

from crew_auditor.tools.github_tools import GithubCrewCodeFetcherTool
from crew_auditor.tools.report_writing_tool import ReportWritingTool


@CrewBase
class CrewAuditorEnhancingCodeQualityWithCrewaiCrew:
    """CrewAuditorEnhancingCodeQualityWithCrewai crew"""

    github_crew_code_fetcher_tool = GithubCrewCodeFetcherTool()
    docs_search_tool = CodeDocsSearchTool(docs_url="https://docs.crewai.com/")
    # report_writing_tool = ReportWritingTool()

    @agent
    def information_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["information_collector"],  # type: ignore
            tools=[
                self.github_crew_code_fetcher_tool,
            ],
        )

    @agent
    def crewai_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["crewai_expert"],  # type: ignore
            tools=[
                self.docs_search_tool,
                # self.report_writing_tool,
            ],
        )

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

    @crew
    def crew(self) -> Crew:
        """Creates the CrewAuditorEnhancingCodeQualityWithCrewai crew"""
        return Crew(
            agents=self.agents,  # type: ignore
            tasks=self.tasks,  # type: ignore
            process=Process.sequential,
            verbose=True,
        )
