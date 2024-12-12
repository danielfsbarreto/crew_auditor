import os
from typing import Type

from crewai.tools import BaseTool
from github import Auth, Github
from pydantic import BaseModel, Field


class GithubCrewCodeFetcherToolInput(BaseModel):
    """Input schema for GithubCrewCodeFetcherToolInput.

    Attributes:
        github_repo: Repository identifier in the format 'user/repo'
    """

    github_repo: str = Field(..., description="The GitHub repository (user/repo).")


class GithubCrewCodeFetcherTool(BaseTool):
    name: str = "GithubCrewCodeFetcherTool"
    description: str = (
        "A tool that scans a Github repository and returns the content of all text files, "
        "handling binary files and access errors gracefully."
    )
    args_schema: Type[BaseModel] = GithubCrewCodeFetcherToolInput

    def _run(self, github_repo: str) -> str:
        access_token = os.getenv("GITHUB_CREDENTIALS")
        if not access_token:
            raise ValueError("GITHUB_CREDENTIALS environment variable is not set")

        auth = Auth.Token(access_token)
        g = Github(auth=auth)
        repo = g.get_repo(github_repo)
        contents = repo.get_contents("")

        repo_content = []
        while contents:
            file_content = contents.pop(0)  # type: ignore
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))  # type: ignore
            else:
                if file_content.path == "uv.lock":
                    continue

                try:
                    content = file_content.decoded_content.decode("utf-8")
                    repo_content.extend(
                        [
                            f"\nFile: {file_content.path}",
                            "Content:",
                            f"{content}",
                            "-" * 80,
                        ]
                    )
                except UnicodeDecodeError:
                    repo_content.append(f"\nSkipped binary file: {file_content.path}")
                except Exception as e:
                    repo_content.append(
                        f"\nError reading {file_content.path}: {str(e)}"
                    )

        return "\n".join(repo_content)


class CrewAiDocsFetcherTool(BaseTool):
    name: str = "CrewAiDocsFetcherTool"
    description: str = "A tool that fetches the CrewAI docs content."

    def _run(self) -> str:
        access_token = os.getenv("GITHUB_CREDENTIALS")
        if not access_token:
            raise ValueError("GITHUB_CREDENTIALS environment variable is not set")

        auth = Auth.Token(access_token)
        g = Github(auth=auth)
        repo = g.get_repo("crewAIInc/crewAI")
        contents = repo.get_contents("")

        repo_content = []
        while contents:
            file_content = contents.pop(0)  # type: ignore
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))  # type: ignore
            else:
                if "docs" not in file_content.path:
                    continue

                try:
                    content = file_content.decoded_content.decode("utf-8")
                    repo_content.extend(
                        [
                            f"\nFile: {file_content.path}",
                            "Content:",
                            f"{content}",
                            "-" * 80,
                        ]
                    )
                except UnicodeDecodeError:
                    repo_content.append(f"\nSkipped binary file: {file_content.path}")
                except Exception as e:
                    repo_content.append(
                        f"\nError reading {file_content.path}: {str(e)}"
                    )

        return "\n".join(repo_content)
