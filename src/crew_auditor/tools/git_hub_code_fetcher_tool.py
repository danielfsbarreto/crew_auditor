import os
from typing import Type

from crewai.tools import BaseTool
from github import Auth, Github
from pydantic import BaseModel, Field


class GitHubCodeFetcherToolInput(BaseModel):
    """Input schema for GitHubCodeFetcherTool.

    Attributes:
        github_repo: Repository identifier in the format 'user/repo'
    """

    github_repo: str = Field(..., description="The GitHub repository (user/repo).")


class GitHubCodeFetcherTool(BaseTool):
    name: str = "GitHubCodeFetcherTool"
    description: str = (
        "A tool that scans a Github repository and returns the content of all text files, "
        "handling binary files and access errors gracefully."
    )
    args_schema: Type[BaseModel] = GitHubCodeFetcherToolInput

    def _run(self, github_repo: str) -> str:
        access_token = str(os.getenv("GITHUB_ACCESS_TOKEN", ""))
        if not access_token:
            raise ValueError("GITHUB_ACCESS_TOKEN environment variable is not set")

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
