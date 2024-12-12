from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ReportWritingToolInput(BaseModel):
    """Input schema for ReportWritingTool.

    Attributes:
        crew_name: The name of the crew.
        introduction_section_content: The content of the introduction section of the report.
        quality_score_section_content: The content of the quality score section of the report. The score must be between 0 and 100.
        crew_architecture_section_content: The content of the crew architecture section of the report.
        agents_section_content: The content of the agents section of the report.
        tasks_section_content: The content of the tasks section of the report.
        tools_section_content: The content of the tools section of the report.
        recommendations_section_content: The content of the recommendations section of the report.
    """

    crew_name: str = Field(
        ...,
        description="The name of the crew.",
    )
    introduction_section_content: str = Field(
        ..., description="The content of the introduction section of the report."
    )
    quality_score_section_content: str = Field(
        ..., description="The content of the quality score section of the report."
    )
    crew_architecture_section_content: str = Field(
        ..., description="The content of the crew architecture section of the report."
    )
    agents_section_content: str = Field(
        ..., description="The content of the agents section of the report."
    )
    tasks_section_content: str = Field(
        ..., description="The content of the tasks section of the report."
    )
    tools_section_content: str = Field(
        ..., description="The content of the tools section of the report."
    )
    recommendations_section_content: str = Field(
        ..., description="The content of the recommendations section of the report."
    )


class ReportWritingTool(BaseTool):
    name: str = "ReportWritingTool"
    description: str = "A tool that writes a report with the analysis of the crew's code, highlighting strengths and areas for improvement."
    args_schema: Type[BaseModel] = ReportWritingToolInput

    def _run(
        self,
        crew_name: str,
        introduction_section_content: str,
        quality_score_section_content: str,
        crew_architecture_section_content: str,
        agents_section_content: str,
        tasks_section_content: str,
        tools_section_content: str,
        recommendations_section_content: str,
    ) -> str:
        report = f"""
# CrewAI Code Analysis Report for `{crew_name}`

## Introduction
{introduction_section_content}

## Quality Score
{quality_score_section_content}

## Crew Architecture
{crew_architecture_section_content}

## Agents
{agents_section_content}

## Tasks
{tasks_section_content}

## Tools
{tools_section_content}

## Recommendations
{recommendations_section_content}
"""

        return report
