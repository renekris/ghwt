"""Integration tests for GitHub CLI wrapper."""

import subprocess

import pytest
from github_fetcher import GitHubIssueFetcher
from models import IssueData, PRData


@pytest.mark.integration
class TestGitHubIntegration:
    """Integration tests for GitHub issue/PR fetching."""

    def test_fetch_issue_success(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test successful issue fetch with mocked GitHub CLI."""
        from unittest.mock import MagicMock, patch

        mock_result = MagicMock()
        mock_result.stdout = '{"title":"Test Issue","body":"Test issue body","number":42,"author":{"login":"testuser"},"labels":[{"name":"bug"}],"state":"open","url":"https://github.com/test/repo/issues/42","comments":[]}'
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = issue_fetcher.fetch_issue("testuser", "testrepo", 42)

        assert isinstance(result, IssueData)
        assert result.title == "Test Issue"
        assert result.number == 42
        assert result.author == "testuser"
        assert result.state == "open"
        assert len(result.labels) == 1
        assert result.labels[0] == "bug"
        assert len(result.comments) == 0

    def test_fetch_issue_with_comments(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test issue fetch with comments."""
        from unittest.mock import MagicMock, patch

        mock_result = MagicMock()
        mock_result.stdout = '{"title":"Test Issue","body":"Test issue body","number":42,"author":{"login":"testuser"},"labels":[{"name":"bug"}],"state":"open","url":"https://github.com/test/repo/issues/42","comments":[{"author":{"login":"commenter"},"body":"Test comment","createdAt":"2026-01-03T10:00:00Z"}]}'
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = issue_fetcher.fetch_issue("testuser", "testrepo", 42)

        assert result.title == "Test Issue"
        assert result.body == "Test issue body"
        assert len(result.comments) == 1

    def test_fetch_pr_success(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test successful PR fetch with mocked GitHub CLI."""
        from unittest.mock import MagicMock, patch

        mock_result = MagicMock()
        mock_result.stdout = '{"title":"Test PR","body":"Test PR body","number":123,"author":{"login":"testuser"},"labels":[{"name":"enhancement"}],"state":"open","url":"https://github.com/test/repo/pull/123","comments":[],"headRefName":"feature/test","baseRefName":"dev","mergeable":true,"additions":10,"deletions":5,"files":[{"path":"src/main.py"},{"path":"README.md"}]}'
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = issue_fetcher.fetch_pr("testuser", "testrepo", 123)

        assert isinstance(result, PRData)
        assert result.title == "Test PR"
        assert result.number == 123
        assert result.author == "testuser"
        assert result.state == "open"
        assert result.head_branch == "feature/test"
        assert result.base_branch == "dev"
        assert result.mergeable is True
        assert result.additions == 10
        assert result.deletions == 5
        assert len(result.files_changed) == 2
        assert len(result.labels) == 1
        assert result.labels[0] == "enhancement"

    def test_fetch_pr_with_files(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test PR fetch with file changes."""
        from unittest.mock import MagicMock, patch

        mock_result = MagicMock()
        mock_result.stdout = '{"title":"Test PR","body":"Test PR body","number":123,"author":{"login":"testuser"},"labels":[{"name":"enhancement"}],"state":"open","url":"https://github.com/test/repo/pull/123","comments":[],"headRefName":"feature/test","baseRefName":"dev","mergeable":true,"additions":100,"deletions":50,"files":[{"path":"src/main.py"},{"path":"README.md"},{"path":"test.py"}]}'
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = issue_fetcher.fetch_pr("testuser", "testrepo", 123)

        assert result.title == "Test PR"
        assert result.body == "Test PR body"
        assert result.head_branch == "feature/test"
        assert result.base_branch == "dev"
        assert result.mergeable is True
        assert result.additions == 100
        assert result.deletions == 50
        assert len(result.files_changed) == 3

    def test_fetch_issue_cli_not_installed(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test error when GitHub CLI is not installed."""
        from unittest.mock import patch

        with (
            pytest.raises(RuntimeError, match="GitHub CLI .* not installed"),
            patch("subprocess.run", side_effect=FileNotFoundError("gh")),
        ):
            issue_fetcher.fetch_issue("testuser", "testrepo", 42)

    def test_fetch_issue_timeout(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test error when GitHub CLI times out."""
        from unittest.mock import patch

        with (
            pytest.raises(RuntimeError, match="GitHub CLI timeout"),
            patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 30)),
        ):
            issue_fetcher.fetch_issue("testuser", "testrepo", 42)

    def test_fetch_issue_cli_error(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test error when GitHub CLI returns non-zero exit code."""
        from unittest.mock import patch

        with pytest.raises(RuntimeError, match="GitHub CLI failed"):
            error = subprocess.CalledProcessError(1, ["gh", "issue", "view", "42"])
            error.stderr = b"Error: Not found"
            with patch("subprocess.run", side_effect=error):
                issue_fetcher.fetch_issue("testuser", "testrepo", 42)

    def test_fetch_pr_timeout(self, issue_fetcher: GitHubIssueFetcher) -> None:
        """Test error when GitHub CLI times out for PR fetch."""
        from unittest.mock import patch

        with (
            pytest.raises(RuntimeError, match="GitHub CLI timeout"),
            patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 30)),
        ):
            issue_fetcher.fetch_pr("testuser", "testrepo", 123)
