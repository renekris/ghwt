"""Shared fixtures for worktree automation tests."""

from pathlib import Path

import pytest
from github_fetcher import GitHubIssueFetcher
from template_renderer import TemplateRenderer
from worktree_creator import WorktreeCreator


@pytest.fixture(scope="session")
def template_path() -> Path:
    """Path to WT_TASK_TEMPLATE.md."""
    return Path(__file__).parent.parent / "WT_TASK_TEMPLATE.md"


@pytest.fixture
def temp_worktree_root(tmp_path: Path) -> Path:
    """Temporary directory for worktree operations."""
    worktree_dir = tmp_path / ".worktrees"
    worktree_dir.mkdir()
    yield worktree_dir


@pytest.fixture(scope="session")
def sample_issue_data() -> dict:
    """Sample issue data for testing."""
    return {
        "title": "Fix database connection error",
        "body": "Database fails when connecting to PostgreSQL",
        "number": 42,
        "author": {"login": "testuser"},
        "labels": [{"name": "bug"}, {"name": "priority:high"}],
        "state": "open",
        "url": "https://github.com/test/repo/issues/42",
        "comments": [
            {
                "author": {"login": "contributor1"},
                "body": "I can reproduce this issue",
                "created_at": "2026-01-03T10:00:00Z",
            }
        ],
    }


@pytest.fixture(scope="session")
def sample_pr_data() -> dict:
    """Sample PR data for testing."""
    return {
        "title": "Add user authentication",
        "body": "Implements OAuth login with GitHub",
        "number": 123,
        "author": {"login": "contributor"},
        "labels": [{"name": "enhancement"}, {"name": "feature"}],
        "state": "open",
        "url": "https://github.com/test/repo/pull/123",
        "head_branch": "feature/auth",
        "base_branch": "dev",
        "mergeable": True,
        "additions": 250,
        "deletions": 50,
        "changed_files": 15,
        "comments": [
            {
                "author": {"login": "reviewer"},
                "body": "Looks good, just one minor comment",
                "created_at": "2026-01-03T11:00:00Z",
            }
        ],
    }


@pytest.fixture
def issue_fetcher(template_path: Path) -> GitHubIssueFetcher:
    """GitHub issue fetcher instance."""
    return GitHubIssueFetcher()


@pytest.fixture
def template_renderer(template_path: Path) -> TemplateRenderer:
    """Template renderer instance."""
    return TemplateRenderer(template_path)


@pytest.fixture
def worktree_creator(
    issue_fetcher: GitHubIssueFetcher, template_renderer: TemplateRenderer, temp_worktree_root: Path
) -> WorktreeCreator:
    """Worktree creator instance with test configuration."""
    return WorktreeCreator(
        issue_fetcher=issue_fetcher, template_renderer=template_renderer, worktree_root=str(temp_worktree_root)
    )


@pytest.fixture
def mock_github_cli():
    """Mock GitHub CLI responses for issue fetching."""
    from unittest.mock import MagicMock, patch

    mock_result = MagicMock()
    mock_result.stdout = '{"title":"Test Issue","body":"Test issue body","number":42,"author":{"login":"testuser"},"labels":[{"name":"bug"}],"state":"open","url":"https://github.com/test/repo/issues/42","comments":[]}'
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_github_cli_with_comments():
    """Mock GitHub CLI responses for issue with comments."""
    from unittest.mock import MagicMock, patch

    mock_result = MagicMock()
    mock_result.stdout = '{"title":"Test Issue","body":"Test issue body","number":42,"author":{"login":"testuser"},"labels":[{"name":"bug"}],"state":"open","url":"https://github.com/test/repo/issues/42","comments":[{"author":{"login":"commenter"},"body":"Test comment","created_at":"2026-01-03T10:00:00Z"}]}'
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_github_cli_pr():
    """Mock GitHub CLI responses for PR fetching."""
    from unittest.mock import MagicMock, patch

    mock_result = MagicMock()
    mock_result.stdout = '{"title":"Test PR","body":"Test PR body","number":123,"author":{"login":"testuser"},"labels":[{"name":"enhancement"}],"state":"open","url":"https://github.com/test/repo/pull/123","comments":[],"headRefName":"feature/test","baseRefName":"dev","mergeable":true,"additions":10,"deletions":5,"changedFiles":2}'
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_github_cli_pr_with_files():
    """Mock GitHub CLI responses for PR with file changes."""
    from unittest.mock import MagicMock, patch

    mock_result = MagicMock()
    mock_result.stdout = '{"title":"Test PR","body":"Test PR body","number":123,"author":{"login":"testuser"},"labels":[{"name":"enhancement"}],"state":"open","url":"https://github.com/test/repo/pull/123","comments":[],"headRefName":"feature/test","baseRefName":"dev","mergeable":true,"additions":100,"deletions":50,"changedFiles":3}'
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_github_cli_not_installed():
    """Mock GitHub CLI not installed error."""
    from unittest.mock import patch

    with patch("subprocess.run", side_effect=FileNotFoundError("gh not found")):
        yield


@pytest.fixture
def mock_github_cli_timeout():
    """Mock GitHub CLI timeout."""
    import subprocess
    from unittest.mock import patch

    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 30)):
        yield


@pytest.fixture
def mock_github_cli_error():
    """Mock GitHub CLI error."""
    from unittest.mock import MagicMock, patch

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Error: Invalid issue number"

    with patch("subprocess.run", return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_github_cli_pr_timeout():
    """Mock GitHub CLI timeout for PR."""
    import subprocess
    from unittest.mock import patch

    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 30)):
        yield


@pytest.fixture
def mock_workmux():
    """Mock workmux CLI."""
    from unittest.mock import MagicMock, patch

    mock_result = MagicMock()
    mock_result.stdout = "Created worktree at /tmp/test-worktree"
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_workmux_existing():
    """Mock workmux CLI with existing worktree."""
    from unittest.mock import MagicMock, patch

    mock_result_list = MagicMock()
    mock_result_list.stdout = "issue-42-test-issue /path/to/existing-worktree"
    mock_result_list.returncode = 0

    mock_result_remove = MagicMock()
    mock_result_remove.stdout = "Removed worktree"
    mock_result_remove.returncode = 0

    mock_result_add = MagicMock()
    mock_result_add.stdout = "Created worktree at /tmp/test-worktree"
    mock_result_add.returncode = 0

    call_count = [0]

    def side_effect(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return mock_result_list
        elif call_count[0] == 2:
            return mock_result_remove
        else:
            return mock_result_add

    with patch("subprocess.run", side_effect=side_effect):
        yield


@pytest.fixture
def mock_user_input_yes():
    """Mock user input accepting branch conflict."""
    from unittest.mock import patch

    with patch("builtins.input", return_value="y"):
        yield


@pytest.fixture
def mock_user_input_no():
    """Mock user input declining branch conflict."""
    from unittest.mock import patch

    with patch("builtins.input", return_value="n"):
        yield


@pytest.fixture
def mock_subprocess_command_aware():
    """Mock subprocess.run with different responses for gh vs workmux commands."""
    from pathlib import Path
    from unittest.mock import MagicMock, patch

    mock_gh_issue_result = MagicMock()
    mock_gh_issue_result.stdout = '{"title":"Test Issue","body":"Test issue body","number":42,"author":{"login":"testuser"},"labels":[{"name":"bug"}],"state":"open","url":"https://github.com/test/repo/issues/42","comments":[]}'
    mock_gh_issue_result.returncode = 0

    mock_gh_pr_result = MagicMock()
    mock_gh_pr_result.stdout = '{"title":"Test PR","body":"Test PR body","number":123,"author":{"login":"testuser"},"labels":[{"name":"enhancement"}],"state":"open","url":"https://github.com/test/repo/pull/123","comments":[],"headRefName":"feature/test","baseRefName":"dev","mergeable":true,"additions":10,"deletions":5,"files":[{"path":"src/main.py"},{"path":"README.md"}]}'
    mock_gh_pr_result.returncode = 0

    call_history = []

    class WorktreeRootHolder:
        def __init__(self):
            self.path = None

        def set_path(self, path: Path):
            self.path = path

    worktree_root_holder = WorktreeRootHolder()

    def side_effect(*args, **kwargs):
        cmd = args[0] if args else []
        call_history.append(cmd)

        if "gh" in cmd:
            if "pr" in cmd:
                return mock_gh_pr_result
            return mock_gh_issue_result
        elif "workmux" in cmd:
            if "list" in cmd:
                branch_name_to_match = kwargs.get("branch_to_create", "issue-42-test-issue")
                list_output = f"{branch_name_to_match} /path/to/existing"
                mock_result = MagicMock()
                mock_result.stdout = list_output
                mock_result.returncode = 0
                return mock_result
            elif "remove" in cmd:
                mock_result = MagicMock()
                mock_result.stdout = "Removed worktree"
                mock_result.returncode = 0
                return mock_result
            else:
                branch_name = cmd[2] if len(cmd) > 2 else "test-branch"
                if worktree_root_holder.path is None:
                    mock_result = MagicMock()
                    mock_result.stdout = "Error: Worktree root not set. Call set_worktree_root() first."
                    mock_result.returncode = 1
                    return mock_result

                worktree_path = worktree_root_holder.path / branch_name
                worktree_path.mkdir(parents=True, exist_ok=True)

                mock_result = MagicMock()
                mock_result.stdout = f"Created worktree at {worktree_path}"
                mock_result.returncode = 0
                return mock_result
        elif "shuvcode" in cmd:
            mock_result = MagicMock()
            mock_result.stdout = ""
            mock_result.returncode = 0
            return mock_result
        else:
            raise ValueError(f"Unexpected command: {cmd}")

    with patch("subprocess.run", side_effect=side_effect) as mock_run:
        mock_run.worktree_root_holder = worktree_root_holder
        mock_run.call_history = call_history
        mock_run.set_worktree_root = worktree_root_holder.set_path
        yield mock_run
