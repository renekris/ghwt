"""GitHub CLI wrapper for fetching issue and PR data."""

import json
import re
import subprocess
from typing import Any

import structlog
from models import CommentData, FileChange, IssueData, PRData


class GitHubIssueFetcher:
    """Fetch GitHub issue and PR data using gh CLI."""

    def __init__(self, gh_timeout: int = 30) -> None:
        """Initialize GitHub issue fetcher.

        Args:
            gh_timeout: GitHub CLI timeout in seconds
        """
        self.logger = structlog.get_logger(__name__)
        self.gh_timeout = gh_timeout

    def _strip_ansi_codes(self, text: str) -> str:
        """Remove ANSI escape sequences from text.

        Defensive helper to handle edge cases where gh CLI might output ANSI codes
        in JSON responses. Most of the time this will be a no-op since --json
        output is already clean.

        Args:
            text: Text that may contain ANSI escape sequences

        Returns:
            Text with ANSI codes removed
        """
        # ANSI escape pattern: \x1b followed by bracket sequence
        ansi_escape = re.compile(r"\x1b\[[0-9;]*[mGKH]")

        stripped = ansi_escape.sub("", text)

        if stripped != text:
            self.logger.warning(
                "ANSI codes detected and stripped from gh CLI output",
                original_length=len(text),
                stripped_length=len(stripped),
            )

        return stripped

    def fetch_issue(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ) -> IssueData:
        """Fetch issue data from GitHub.

        Args:
            owner: Repository owner (e.g., "testuser")
            repo: Repository name (e.g., "testrepo")
            issue_number: Issue number

        Returns:
            IssueData object with issue information

        Raises:
            RuntimeError: If gh CLI fails, times out, or is not installed
        """
        self.logger.info(
            "Fetching GitHub issue",
            owner=owner,
            repo=repo,
            issue_number=issue_number,
        )

        cmd = [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            f"{owner}/{repo}",
            "--json",
            "title,body,number,author,labels,state,url,comments",
        ]

        self.logger.debug("Executing gh CLI command", command=" ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=self.gh_timeout,
            )
        except subprocess.CalledProcessError as e:
            stderr_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode("utf-8", errors="replace")
            self.logger.error(
                "GitHub CLI failed to fetch issue",
                owner=owner,
                repo=repo,
                issue_number=issue_number,
                stderr=stderr_msg[:500] if stderr_msg else None,
            )
            raise RuntimeError(f"GitHub CLI failed to fetch issue {owner}/{repo}#{issue_number}: {stderr_msg}") from e
        except subprocess.TimeoutExpired as e:
            self.logger.error(
                "GitHub CLI timeout",
                owner=owner,
                repo=repo,
                issue_number=issue_number,
                timeout=self.gh_timeout,
            )
            raise RuntimeError(f"GitHub CLI timeout fetching issue {owner}/{repo}#{issue_number}") from e
        except FileNotFoundError as e:
            self.logger.error("GitHub CLI not found")
            raise RuntimeError("GitHub CLI (gh) is not installed. Install from https://cli.github.com/") from e

        self.logger.debug("gh CLI response received", stdout_length=len(result.stdout))

        try:
            cleaned_stdout = self._strip_ansi_codes(result.stdout)
            data: dict[str, Any] = json.loads(cleaned_stdout)
        except json.JSONDecodeError as e:
            self.logger.debug(
                "JSON parsing failed",
                stdout_length=len(result.stdout),
                stdout_first_100=result.stdout[:100] if result.stdout else None,
                error=str(e),
            )
            raise RuntimeError("Failed to parse GitHub CLI response as JSON") from e

        # Parse comments
        comments = [
            CommentData(
                author=comment["author"]["login"],
                body=comment["body"],
                created_at=comment["createdAt"],
            )
            for comment in data.get("comments", [])
        ]

        # Parse labels
        labels = [label["name"] for label in data.get("labels", [])]

        issue_data = IssueData(
            title=data["title"],
            body=data.get("body", ""),
            number=data["number"],
            author=data["author"]["login"],
            labels=labels,
            state=data["state"],
            url=data["url"],
            comments=comments,
        )

        self.logger.info(
            "Issue data fetched successfully",
            title=issue_data.title,
            number=issue_data.number,
            state=issue_data.state,
            labels_count=len(labels),
            comments_count=len(comments),
        )

        return issue_data

    def fetch_pr(
        self,
        owner: str,
        repo: str,
        pr_number: int,
    ) -> PRData:
        """Fetch PR data from GitHub.

        Args:
            owner: Repository owner (e.g., "testuser")
            repo: Repository name (e.g., "testrepo")
            pr_number: Pull request number

        Returns:
            PRData object with PR information

        Raises:
            RuntimeError: If gh CLI fails, times out, or is not installed
        """
        self.logger.info(
            "Fetching GitHub PR",
            owner=owner,
            repo=repo,
            pr_number=pr_number,
        )

        cmd = [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--repo",
            f"{owner}/{repo}",
            "--json",
            "title,body,number,author,labels,state,url,comments,headRefName,baseRefName,mergeable,additions,deletions,files",
        ]

        self.logger.debug("Executing gh CLI command", command=" ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=self.gh_timeout,
            )
        except subprocess.CalledProcessError as e:
            stderr_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode("utf-8", errors="replace")
            self.logger.error(
                "GitHub CLI failed to fetch PR",
                owner=owner,
                repo=repo,
                pr_number=pr_number,
                stderr=stderr_msg[:500] if stderr_msg else None,
            )
            raise RuntimeError(f"GitHub CLI failed to fetch PR {owner}/{repo}#{pr_number}: {stderr_msg}") from e
        except subprocess.TimeoutExpired as e:
            self.logger.error(
                "GitHub CLI timeout",
                owner=owner,
                repo=repo,
                pr_number=pr_number,
                timeout=self.gh_timeout,
            )
            raise RuntimeError(f"GitHub CLI timeout fetching PR {owner}/{repo}#{pr_number}") from e
        except FileNotFoundError as e:
            self.logger.error("GitHub CLI not found")
            raise RuntimeError("GitHub CLI (gh) is not installed. Install from https://cli.github.com/") from e

        self.logger.debug("gh CLI response received", stdout_length=len(result.stdout))

        try:
            data: dict[str, Any] = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            self.logger.debug(
                "JSON parsing failed",
                stdout_length=len(result.stdout),
                stdout_first_100=result.stdout[:100] if result.stdout else None,
                error=str(e),
            )
            raise RuntimeError("Failed to parse GitHub CLI response as JSON") from e

        # Parse comments
        comments = [
            CommentData(
                author=comment["author"]["login"],
                body=comment["body"],
                created_at=comment["createdAt"],
            )
            for comment in data.get("comments", [])
        ]

        # Parse labels
        labels = [label["name"] for label in data.get("labels", [])]

        # Parse file changes
        files_changed = [FileChange(path=file_data["path"]) for file_data in data.get("files", [])]

        pr_data = PRData(
            title=data["title"],
            body=data.get("body", ""),
            number=data["number"],
            author=data["author"]["login"],
            labels=labels,
            state=data["state"],
            url=data["url"],
            comments=comments,
            head_branch=data["headRefName"],
            base_branch=data["baseRefName"],
            mergeable=data.get("mergeable"),
            additions=data.get("additions", 0),
            deletions=data.get("deletions", 0),
            files_changed=files_changed,
        )

        self.logger.info(
            "PR data fetched successfully",
            title=pr_data.title,
            number=pr_data.number,
            state=pr_data.state,
            labels_count=len(labels),
            comments_count=len(comments),
            files_changed_count=len(files_changed),
            additions=pr_data.additions,
            deletions=pr_data.deletions,
            mergeable=pr_data.mergeable,
        )

        return pr_data
