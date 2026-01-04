"""Tests for WorktreeCreator class."""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from config import WorktreeSettings
from models import CommentData, FileChange, IssueData, PRData
from worktree_creator import WorktreeCreator


@pytest.fixture
def temp_test_dir(tmp_path: Path) -> Path:
    """Temporary directory for dry-run tests."""
    return tmp_path / "dry-run-test"


@pytest.fixture
def sample_issue_data() -> IssueData:
    """Sample issue data."""
    return IssueData(
        title="Fix database connection error",
        body="Database fails when connecting...",
        number=42,
        author="testuser",
        labels=["bug", "high"],
        state="open",
        url="https://github.com/repo/issues/42",
        comments=[
            CommentData(author="user2", body="I can reproduce", created_at="2024-01-01T10:00:00Z"),
        ],
    )


@pytest.fixture
def sample_pr_data() -> PRData:
    """Sample PR data."""
    return PRData(
        title="Add OAuth authentication",
        body="Implements OAuth flow...",
        number=123,
        author="contributor",
        labels=["enhancement", "backend"],
        state="open",
        url="https://github.com/repo/pull/123",
        comments=[],
        head_branch="feature/oauth",
        base_branch="dev",
        mergeable=True,
        additions=150,
        deletions=50,
        files_changed=[
            FileChange(path="backend/api/auth.py"),
            FileChange(path="frontend/auth.vue"),
        ],
    )


class TestWorktreeCreator:
    """Test WorktreeCreator functionality."""

    def test_generate_branch_name_issue(self, sample_issue_data: IssueData) -> None:
        """Test branch name generation for issue."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        branch_name = creator._generate_branch_name(sample_issue_data)

        assert branch_name.startswith("issue-42-")
        assert "fix-database-connection-error" in branch_name

    def test_generate_branch_name_pr(self, sample_pr_data: PRData) -> None:
        """Test branch name generation for PR."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        branch_name = creator._generate_branch_name(sample_pr_data)

        assert branch_name.startswith("pr-123-")
        assert "add-oauth-authentication" in branch_name

    def test_parse_issue_url(self) -> None:
        """Test parsing GitHub issue URL."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        item_type, owner, repo, number = creator._parse_github_url("https://github.com/testuser/testrepo/issues/42")

        assert item_type == "issue"
        assert owner == "testuser"
        assert repo == "testrepo"
        assert number == 42

    def test_parse_pr_url(self) -> None:
        """Test parsing GitHub PR URL."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        item_type, owner, repo, number = creator._parse_github_url("https://github.com/testuser/testrepo/pull/123")

        assert item_type == "pr"
        assert owner == "testuser"
        assert repo == "testrepo"
        assert number == 123

    def test_parse_invalid_url(self) -> None:
        """Test parsing invalid GitHub URL."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            _ = creator._parse_github_url("https://example.com/not-github")

    @patch("builtins.input", return_value="y")
    @patch("subprocess.run")
    @patch("pathlib.Path.write_text")
    def test_create_worktree_success(
        self, mock_write_text: Mock, mock_run: Mock, mock_input: Mock, sample_issue_data: IssueData
    ) -> None:
        """Test successful worktree creation."""
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["git", "rev-parse", "--show-toplevel"],
                returncode=0,
                stdout="/tmp/test-git-repo",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["workmux", "list"],
                returncode=0,
                stdout="",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["workmux", "add", "issue-42-fix-database-connection-error"],
                returncode=0,
                stdout="Created worktree at /tmp/test-git-repo/.worktrees/issue-42-fix-database-connection-error",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["shuvcode", "/tmp/test-git-repo/.worktrees/issue-42-fix-database-connection-error"],
                returncode=0,
                stdout="",
                stderr="",
            ),
        ]

        mock_renderer = Mock()
        mock_renderer.render_for_issue.return_value = "Generated prompt content"

        mock_fetcher = Mock()
        mock_fetcher.fetch_issue.return_value = sample_issue_data

        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=mock_fetcher,
            template_renderer=mock_renderer,
            settings=settings,
        )
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        assert worktree_path == Path("/tmp/test-git-repo/.worktrees/issue-42-fix-database-connection-error")
        mock_renderer.render_for_issue.assert_called_once()
        mock_fetcher.fetch_issue.assert_called_once_with("testuser", "testrepo", 42)

    @patch("subprocess.run")
    def test_create_worktree_conflict(self, mock_run: Mock, sample_issue_data: IssueData) -> None:
        """Test branch conflict handling."""

        def run_side_effect(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            if "rev-parse" in args:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout="/tmp/test-git-repo",
                    stderr="",
                )
            elif "list" in args:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout="issue-42-fix-database-connection-error  /tmp/test-git-repo/.worktrees/issue-42-fix-database-connection-error",
                    stderr="",
                )
            elif "remove" in args:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")
            raise RuntimeError("Unexpected subprocess call")

        mock_run.side_effect = run_side_effect

        mock_renderer = Mock()
        mock_renderer.render_for_issue.return_value = "Generated prompt content"

        mock_fetcher = Mock()
        mock_fetcher.fetch_issue.return_value = sample_issue_data

        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=mock_fetcher,
            template_renderer=mock_renderer,
            settings=settings,
        )

        with patch("builtins.input", return_value="n"), pytest.raises(RuntimeError, match="User cancelled"):
            _ = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

    @patch("builtins.input", return_value="y")
    @patch("subprocess.run")
    def test_open_shuvcode(self, mock_run: Mock, mock_input: Mock, sample_issue_data: IssueData) -> None:
        """Test auto-opening shuvcode."""
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["git", "rev-parse", "--show-toplevel"],
                returncode=0,
                stdout="/tmp/test-git-repo",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["workmux", "list"],
                returncode=0,
                stdout="",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["workmux", "add", "issue-42-fix-database-connection-error"],
                returncode=0,
                stdout="Created worktree at /tmp/test-git-repo/.worktrees/issue-42-fix-database-connection-error",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["shuvcode", "/path/to/.worktrees/issue-42-fix-database-connection-error"],
                returncode=0,
                stdout="",
                stderr="",
            ),
        ]

        mock_renderer = Mock()
        mock_renderer.render_for_issue.return_value = "Generated prompt content"

        mock_fetcher = Mock()
        mock_fetcher.fetch_issue.return_value = sample_issue_data

        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=mock_fetcher,
            template_renderer=mock_renderer,
            settings=settings,
        )
        with patch.object(creator, "_write_task_file"):
            _ = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        # Check if shuvcode was called
        shuvcode_calls = [call for call in mock_run.call_args_list if "shuvcode" in str(call)]
        assert len(shuvcode_calls) == 1

    @patch("subprocess.run")
    def test_dry_run_skips_workmux(self, mock_run: Mock, sample_issue_data: IssueData, temp_test_dir: Path) -> None:
        """Dry-run mode does not call workmux subprocess."""
        mock_renderer = Mock()
        mock_renderer.render_for_issue.return_value = "Generated prompt content"

        mock_fetcher = Mock()
        mock_fetcher.fetch_issue.return_value = sample_issue_data

        settings = WorktreeSettings(worktree_root=temp_test_dir)
        creator = WorktreeCreator(
            issue_fetcher=mock_fetcher,
            template_renderer=mock_renderer,
            settings=settings,
            dry_run=True,
        )

        _ = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_task_file_all_placeholders_replaced(
        self, mock_run: Mock, sample_issue_data: IssueData, temp_test_dir: Path
    ) -> None:
        """Generated WT-TASK.md has all placeholders replaced."""
        mock_renderer = Mock()
        mock_renderer.render_for_issue.return_value = (
            "SECTION 1: WORKTREE CONTEXT\n"
            "Title: Fix database connection error\n"
            f"Parent: {temp_test_dir}\n"
            "Worktree: issue-42-fix-database-connection-error\n"
        )

        mock_fetcher = Mock()
        mock_fetcher.fetch_issue.return_value = sample_issue_data

        settings = WorktreeSettings(worktree_root=temp_test_dir)
        creator = WorktreeCreator(
            issue_fetcher=mock_fetcher,
            template_renderer=mock_renderer,
            settings=settings,
            dry_run=True,
        )

        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        content = (worktree_path / "WT-TASK.md").read_text()
        assert "{{" not in content
        assert "Fix database connection error" in content
        assert str(temp_test_dir) in content
        assert "issue-42-fix-database-connection-error" in content
