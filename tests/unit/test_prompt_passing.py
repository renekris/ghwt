"""Tests for prompt passing to shuvcode."""

from pathlib import Path

import pytest
from config import WorktreeSettings, PromptPreset
from models import IssueData
from worktree_creator import WorktreeCreator
from unittest.mock import Mock, patch


@pytest.fixture
def temp_worktree_root(tmp_path: Path) -> Path:
    """Temporary directory for worktree operations."""
    worktree_dir = tmp_path / ".worktrees"
    worktree_dir.mkdir()
    yield worktree_dir


@pytest.fixture
def sample_issue_data() -> IssueData:
    """Sample issue data."""
    from models import CommentData

    return IssueData(
        title="Fix database connection error",
        body="Database fails when connecting...",
        number=42,
        author="testuser",
        labels=["bug", "high"],
        state="open",
        url="https://github.com/repo/issues/42",
        comments=[
            CommentData(
                author="user2",
                body="I can reproduce",
                created_at="2024-01-01T10:00:00Z",
            ),
        ],
    )


class TestPromptResolution:
    """Test prompt resolution logic."""

    def test_resolve_custom_prompt(self, temp_worktree_root: Path) -> None:
        """Test custom prompt takes priority over all sources."""
        settings = WorktreeSettings(
            worktree_root=temp_worktree_root,
            agent_prompt="Custom agent instruction",
        )
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        prompt = creator._resolve_shuvcode_prompt(worktree_path)

        assert prompt == "Custom agent instruction"

    def test_resolve_preset_prompt(self, temp_worktree_root: Path) -> None:
        """Test preset prompt takes priority over WT-TASK.md."""
        settings = WorktreeSettings(
            worktree_root=temp_worktree_root,
            agent_prompt_preset=PromptPreset.RALPH_LOOP,
        )
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        prompt = creator._resolve_shuvcode_prompt(worktree_path)

        assert "Follow Ralph's autonomous development loop" in prompt

    def test_resolve_wt_task_prompt(
        self, temp_worktree_root: Path, sample_issue_data: IssueData
    ) -> None:
        """Test WT-TASK.md content is used when no custom prompt or preset."""
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Create WT-TASK.md
        task_file = worktree_path / "WT-TASK.md"
        task_file.write_text("Test WT-TASK content")

        prompt = creator._resolve_shuvcode_prompt(worktree_path)

        assert prompt == "Test WT-TASK content"

    def test_resolve_none_when_no_prompt_available(
        self, temp_worktree_root: Path
    ) -> None:
        """Test None is returned when no prompt source available."""
        settings = WorktreeSettings(worktree_root=temp_worktree_root, no_prompt=True)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Don't create WT-TASK.md
        prompt = creator._resolve_shuvcode_prompt(worktree_path)

        assert prompt is None


class TestShuvcodeCommands:
    """Test shuvcode command generation."""

    @patch("subprocess.run")
    def test_shuvcode_with_wt_task_prompt(
        self, mock_run: Mock, temp_worktree_root: Path, sample_issue_data: IssueData
    ) -> None:
        """Test shuvcode receives WT-TASK.md as prompt."""

        # Track subprocess calls
        calls = []

        def track_calls(*args, **kwargs):
            calls.append(list(args[0]) if args else [])
            mock_result = Mock()
            mock_result.stdout = ""
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = track_calls

        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Create WT-TASK.md
        task_file = worktree_path / "WT-TASK.md"
        task_file.write_text("Test task content")

        # Open shuvcode
        creator._open_shuvcode(worktree_path)

        # Find shuvcode call
        shuvcode_calls = [c for c in calls if "shuvcode" in c]
        assert len(shuvcode_calls) == 1

        cmd = shuvcode_calls[0]
        assert "shuvcode" in cmd
        assert str(worktree_path) in cmd
        assert "--prompt" in cmd
        # Verify prompt content passed
        prompt_index = cmd.index("--prompt") + 1
        assert cmd[prompt_index] == "Test task content"

    @patch("subprocess.run")
    def test_ci_mode_uses_run_command(
        self, mock_run: Mock, temp_worktree_root: Path, sample_issue_data: IssueData
    ) -> None:
        """Test CI mode uses 'shuvcode run' command."""
        # Track subprocess calls
        calls = []

        def track_calls(*args, **kwargs):
            calls.append(list(args[0]) if args else [])
            mock_result = Mock()
            mock_result.stdout = ""
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = track_calls

        settings = WorktreeSettings(worktree_root=temp_worktree_root, ci_mode=True)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Create WT-TASK.md
        task_file = worktree_path / "WT-TASK.md"
        task_file.write_text("Test task content")

        # Open shuvcode in CI mode
        creator._open_shuvcode(worktree_path)

        # Find shuvcode call
        shuvcode_calls = [c for c in calls if "shuvcode" in c]
        assert len(shuvcode_calls) == 1

        cmd = shuvcode_calls[0]
        assert "shuvcode" in cmd
        assert "run" in cmd
        assert "--prompt" not in cmd  # No --prompt flag in CI mode
        # Verify prompt content passed directly to 'run' command
        run_index = cmd.index("run") + 1
        assert cmd[run_index] == "Test task content"

    @patch("subprocess.run")
    def test_no_prompt_skips_prompt_flag(
        self, mock_run: Mock, temp_worktree_root: Path, sample_issue_data: IssueData
    ) -> None:
        """Test --no-prompt flag skips prompt passing."""
        # Track subprocess calls
        calls = []

        def track_calls(*args, **kwargs):
            calls.append(
                {"cmd": list(args[0]) if args else [], "env": kwargs.get("env")}
            )
            mock_result = Mock()
            mock_result.stdout = ""
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = track_calls

        settings = WorktreeSettings(worktree_root=temp_worktree_root, no_prompt=True)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Create WT-TASK.md
        task_file = worktree_path / "WT-TASK.md"
        task_file.write_text("Test task content")

        # Open shuvcode with no-prompt
        creator._open_shuvcode(worktree_path)

        # Find shuvcode call
        shuvcode_calls = [c for c in calls if "shuvcode" in c["cmd"]]
        assert len(shuvcode_calls) == 1

        call_info = shuvcode_calls[0]
        cmd = call_info["cmd"]
        env = call_info["env"]
        assert "shuvcode" in cmd
        assert str(worktree_path) in cmd
        assert "--prompt" not in cmd  # No prompt flag
        assert "run" not in cmd  # Not in CI mode
        assert env is None or "OPENCODE_PERMISSION" not in env  # No auto-permission

    @patch("subprocess.run")
    def test_ci_mode_sets_permission_env_var(
        self, mock_run: Mock, temp_worktree_root: Path, sample_issue_data: IssueData
    ) -> None:
        """Test CI mode sets OPENCODE_PERMISSION environment variable."""
        # Track subprocess calls
        calls = []

        def track_calls(*args, **kwargs):
            calls.append(
                {"cmd": list(args[0]) if args else [], "env": kwargs.get("env")}
            )
            mock_result = Mock()
            mock_result.stdout = ""
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = track_calls

        settings = WorktreeSettings(worktree_root=temp_worktree_root, ci_mode=True)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )

        worktree_path = temp_worktree_root / "test-branch"
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Create WT-TASK.md
        task_file = worktree_path / "WT-TASK.md"
        task_file.write_text("Test task content")

        # Open shuvcode in CI mode
        creator._open_shuvcode(worktree_path)

        # Find shuvcode call
        shuvcode_calls = [c for c in calls if "shuvcode" in c["cmd"]]
        assert len(shuvcode_calls) == 1

        call_info = shuvcode_calls[0]
        cmd = call_info["cmd"]
        env = call_info["env"]

        # Verify CI mode command
        assert "shuvcode" in cmd
        assert "run" in cmd
        assert "--prompt" not in cmd  # No --prompt flag in CI mode

        # Verify OPENCODE_PERMISSION is set
        assert env is not None, "Environment should be passed to subprocess"
        assert "OPENCODE_PERMISSION" in env, (
            "OPENCODE_PERMISSION should be set in CI mode"
        )
        assert env["OPENCODE_PERMISSION"] == '{"*":"allow"}'

    @patch("subprocess.run")
    def test_dry_run_skips_shuvcode(
        self, mock_run: Mock, temp_worktree_root: Path
    ) -> None:
        """Test dry-run mode skips shuvcode entirely."""
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
            dry_run=True,
        )

        worktree_path = temp_worktree_root / "test-branch"

        # Open shuvcode in dry-run mode
        creator._open_shuvcode(worktree_path)

        # Verify subprocess not called
        mock_run.assert_not_called()
