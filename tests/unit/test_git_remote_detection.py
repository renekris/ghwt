"""Test git remote detection for WorktreeCreator."""

import subprocess
from unittest.mock import Mock, patch

import pytest
from config import WorktreeSettings
from worktree_creator import WorktreeCreator


class TestGitRemoteDetection:
    """Test _detect_git_remote() method."""

    def test_detects_github_https_url(self):
        """Detects owner/repo from HTTPS GitHub remote."""
        mock_result = Mock()
        mock_result.stdout = "origin\thttps://github.com/testowner/testrepo.git (fetch)\norigin\thttps://github.com/testowner/testrepo.git (push)"
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            owner, repo = creator._detect_git_remote()

        assert owner == "testowner"
        assert repo == "testrepo"

    def test_detects_github_ssh_url(self):
        """Detects owner/repo from SSH GitHub remote."""
        mock_result = Mock()
        mock_result.stdout = "origin\tgit@github.com:testowner/testrepo.git (fetch)\norigin\tgit@github.com:testowner/testrepo.git (push)"
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            owner, repo = creator._detect_git_remote()

        assert owner == "testowner"
        assert repo == "testrepo"

    def test_detects_ssh_protocol_url(self):
        """Detects owner/repo from ssh:// protocol GitHub remote."""
        mock_result = Mock()
        mock_result.stdout = "origin\tssh://git@github.com/testowner/testrepo.git (fetch)"
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            owner, repo = creator._detect_git_remote()

        assert owner == "testowner"
        assert repo == "testrepo"

    def test_strips_git_suffix(self):
        """Removes .git suffix from remote URL."""
        mock_result = Mock()
        mock_result.stdout = "origin\thttps://github.com/testowner/testrepo.git (fetch)"
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            owner, repo = creator._detect_git_remote()

        assert repo == "testrepo"
        assert not repo.endswith(".git")

    def test_returns_first_github_remote(self):
        """Returns first GitHub remote when multiple remotes exist."""
        mock_result = Mock()
        mock_result.stdout = (
            "upstream\thttps://github.com/upstream/testrepo.git (fetch)\n"
            "origin\thttps://github.com/testowner/testrepo.git (fetch)\n"
        )
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            owner, repo = creator._detect_git_remote()

        assert owner == "upstream"
        assert repo == "testrepo"

    def test_raises_error_no_github_remote(self):
        """Raises RuntimeError when no GitHub remote found."""
        mock_result = Mock()
        mock_result.stdout = "origin\thttps://gitlab.com/testowner/testrepo.git (fetch)"
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            with pytest.raises(RuntimeError, match="No GitHub remote found"):
                creator._detect_git_remote()

    def test_raises_error_git_not_installed(self):
        """Raises RuntimeError when git is not installed."""

        def side_effect(args: list[str], **kwargs: object) -> object:
            if "rev-parse" in args:
                mock_result = Mock()
                mock_result.stdout = "/tmp/test-worktrees"
                mock_result.returncode = 0
                return mock_result
            raise FileNotFoundError("git not found")

        with patch("subprocess.run", side_effect=side_effect), patch("pathlib.Path.mkdir"):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            with pytest.raises(RuntimeError, match="Git is not installed"):
                creator._detect_git_remote()

    def test_raises_error_git_timeout(self):
        """Raises RuntimeError when git remote command times out."""

        def side_effect(args: list[str], **kwargs: object) -> object:
            if "rev-parse" in args:
                mock_result = Mock()
                mock_result.stdout = "/tmp/test-worktrees"
                mock_result.returncode = 0
                return mock_result
            raise subprocess.TimeoutExpired("git", 60)

        with patch("subprocess.run", side_effect=side_effect), patch("pathlib.Path.mkdir"):
            settings = WorktreeSettings(worktree_root=None)
            creator = WorktreeCreator(
                issue_fetcher=Mock(),
                template_renderer=Mock(),
                settings=settings,
            )
            with pytest.raises(RuntimeError, match="Timeout detecting git remote"):
                creator._detect_git_remote()
