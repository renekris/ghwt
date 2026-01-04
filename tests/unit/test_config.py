"""Test WorktreeSettings configuration."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
from config import WorktreeSettings


class TestWorktreeSettings:
    """Test WorktreeSettings configuration."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        settings = WorktreeSettings()
        assert settings.gh_cli_timeout == 30
        assert settings.workmux_timeout == 60
        assert settings.file_write_timeout == 5
        assert settings.verbose is False
        assert settings.quiet is False
        assert settings.worktree_root is None

    def test_path_resolution_with_tilde(self) -> None:
        """Test that ~ is expanded in paths."""
        settings = WorktreeSettings(worktree_root=Path("~/worktrees"))
        assert settings.worktree_root == Path.home() / "worktrees"

    def test_env_var_prefix(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test WORKTREE_ROOT environment variable (no prefix)."""
        monkeypatch.setenv("WORKTREE_ROOT", "/custom/path")
        settings = WorktreeSettings()
        assert settings.worktree_root == Path("/custom/path")

    def test_template_path_validation(self) -> None:
        """Test that non-existent template raises error."""
        with pytest.raises(ValueError, match="Template file not found"):
            WorktreeSettings(template_path=Path("/nonexistent/template.md"))

    def test_timeout_validation(self) -> None:
        """Test that timeout validation works."""
        with pytest.raises(ValueError):
            WorktreeSettings(gh_cli_timeout=0)

        with pytest.raises(ValueError):
            WorktreeSettings(gh_cli_timeout=301)

    def test_get_default_worktree_root_success(self, tmp_path: Path) -> None:
        """Test default worktree root detection."""
        git_dir = tmp_path / "test-repo"
        git_dir.mkdir()
        (git_dir / ".git").mkdir()

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["git", "rev-parse", "--show-toplevel"],
                returncode=0,
                stdout=str(git_dir),
                stderr="",
            )

            default_root = WorktreeSettings.get_default_worktree_root()
            assert default_root == git_dir / ".worktrees"

    def test_get_default_worktree_root_not_in_git_repo(self) -> None:
        """Test error when not in a git repository."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(returncode=128, cmd="git rev-parse --show-toplevel")

            with pytest.raises(RuntimeError, match="Not in a git repository"):
                WorktreeSettings.get_default_worktree_root()

    def test_get_default_worktree_root_git_not_found(self) -> None:
        """Test error when git is not installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            with pytest.raises(RuntimeError, match="Git is not installed"):
                WorktreeSettings.get_default_worktree_root()

    def test_get_default_worktree_root_git_timeout(self) -> None:
        """Test error when git command times out."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="git rev-parse --show-toplevel", timeout=5)

            with pytest.raises(RuntimeError, match="Git command timed out"):
                WorktreeSettings.get_default_worktree_root()

    def test_get_effective_worktree_root_uses_custom(self, tmp_path: Path) -> None:
        """Test that custom worktree_root is used when specified."""
        custom_root = tmp_path / "custom-worktrees"
        settings = WorktreeSettings(worktree_root=custom_root)

        effective_root = settings.get_effective_worktree_root()
        assert effective_root == custom_root
        assert effective_root.exists()

    def test_get_effective_worktree_root_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test fallback to git repo default when worktree_root is None."""
        monkeypatch.delenv("GHWT_WORKTREE_ROOT", raising=False)

        git_dir = tmp_path / "test-repo"
        git_dir.mkdir()
        (git_dir / ".git").mkdir()

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["git", "rev-parse", "--show-toplevel"],
                returncode=0,
                stdout=str(git_dir),
                stderr="",
            )

            settings = WorktreeSettings()
            effective_root = settings.get_effective_worktree_root()
            assert effective_root == git_dir / ".worktrees"

    def test_verbose_quiet_flags(self) -> None:
        """Test verbose and quiet flags."""
        settings = WorktreeSettings(verbose=True, quiet=False)
        assert settings.verbose is True
        assert settings.quiet is False

        settings = WorktreeSettings(verbose=False, quiet=True)
        assert settings.verbose is False
        assert settings.quiet is True

    def test_env_var_worktree_root(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test WORKTREE_ROOT environment variable."""
        monkeypatch.setenv("WORKTREE_ROOT", "/custom/root")
        settings = WorktreeSettings()
        assert settings.worktree_root == Path("/custom/root")

    def test_env_var_gh_cli_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test GH_CLI_TIMEOUT environment variable."""
        monkeypatch.setenv("GH_CLI_TIMEOUT", "60")
        settings = WorktreeSettings()
        assert settings.gh_cli_timeout == 60

    def test_cli_flag_overrides_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that CLI flag overrides environment variable."""
        monkeypatch.setenv("GHWT_WORKTREE_ROOT", "/env/root")
        settings = WorktreeSettings(worktree_root=Path("/cli/root"))
        assert settings.worktree_root == Path("/cli/root")

    def test_default_template_path_resolution(self) -> None:
        """Test that default template path resolves to package directory."""
        from config import __file__ as config_file

        settings = WorktreeSettings()
        expected_path = Path(config_file).parent / "WT_TASK_TEMPLATE.md"
        assert settings.template_path == expected_path
        assert settings.template_path.exists()
