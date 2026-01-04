"""Test suite for worktree automation tool."""

import json
import subprocess
from unittest.mock import patch

import pytest
from github_fetcher import GitHubIssueFetcher


@pytest.fixture
def sample_issue_data() -> dict[str, object]:
    """Sample issue data from GitHub API."""
    return {
        "title": "Fix database connection error",
        "body": "Database fails when connecting...",
        "number": 42,
        "author": {"login": "testuser"},
        "labels": [{"name": "bug"}, {"name": "high"}],
        "state": "open",
        "url": "https://github.com/repo/issues/42",
        "comments": [
            {
                "author": {"login": "user2"},
                "body": "I can reproduce",
                "createdAt": "2024-01-01T10:00:00Z",
            }
        ],
    }


@pytest.fixture
def sample_pr_data() -> dict[str, object]:
    """Sample PR data from GitHub API."""
    return {
        "title": "Add OAuth authentication",
        "body": "Implements OAuth flow...",
        "number": 123,
        "author": {"login": "contributor"},
        "labels": [{"name": "enhancement"}, {"name": "backend"}],
        "state": "open",
        "url": "https://github.com/repo/pull/123",
        "comments": [],
        "headRefName": "feature/oauth",
        "baseRefName": "dev",
        "mergeable": True,
        "additions": 150,
        "deletions": 50,
        "files": [
            {"path": "backend/api/auth.py"},
            {"path": "frontend/auth.vue"},
        ],
    }


class TestGitHubIssueFetcher:
    """Test GitHub CLI wrapper functionality."""

    def test_fetch_issue_success(self, sample_issue_data: dict[str, object]) -> None:
        """Test successful issue fetch."""
        fetcher = GitHubIssueFetcher()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = json.dumps(sample_issue_data)
            mock_run.return_value.returncode = 0

            result = fetcher.fetch_issue(owner="testuser", repo="testrepo", issue_number=42)

            assert result.title == "Fix database connection error"
            assert result.number == 42
            assert result.author == "testuser"
            assert len(result.comments) == 1

    def test_fetch_issue_not_found(self):
        """Test issue not found error."""
        fetcher = GitHubIssueFetcher()
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "gh", stderr=b"Not Found")

            with pytest.raises(RuntimeError, match="GitHub CLI failed"):
                fetcher.fetch_issue(owner="testuser", repo="testrepo", issue_number=999)

    def test_fetch_pr_success(self, sample_pr_data: dict[str, object]) -> None:
        """Test successful PR fetch."""
        fetcher = GitHubIssueFetcher()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = json.dumps(sample_pr_data)
            mock_run.return_value.returncode = 0

            result = fetcher.fetch_pr(owner="testuser", repo="testrepo", pr_number=123)

            assert result.title == "Add OAuth authentication"
            assert result.number == 123
            assert result.head_branch == "feature/oauth"
            assert result.base_branch == "dev"
            assert result.mergeable is True
            assert len(result.files_changed) == 2

    def test_fetch_pr_timeout(self):
        """Test PR fetch timeout."""
        fetcher = GitHubIssueFetcher()
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("gh pr view", 60)

            with pytest.raises(RuntimeError, match="GitHub CLI timeout"):
                fetcher.fetch_pr(owner="testuser", repo="testrepo", pr_number=123)

    def test_fetch_gh_not_installed(self):
        """Test GitHub CLI not installed."""
        fetcher = GitHubIssueFetcher()
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("gh")

            with pytest.raises(RuntimeError, match="GitHub CLI .* not installed"):
                fetcher.fetch_issue(owner="testuser", repo="testrepo", issue_number=42)
