"""Tests for URL parsing and conflict handling."""

import subprocess
from unittest.mock import Mock, patch

import pytest
from config import WorktreeSettings
from worktree_creator import WorktreeCreator


class TestURLParsing:
    """Test URL parsing logic."""

    def test_parse_issue_url(self):
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

    def test_parse_pr_url(self):
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

    def test_parse_invalid_url(self):
        """Test parsing invalid GitHub URL."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            creator._parse_github_url("https://example.com/not-github")

    def test_parse_bare_number_issue(self):
        """Test parsing bare number with --issue flag."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        item_type, owner, repo, number = creator._parse_github_url("42", item_type="issue")

        assert item_type == "issue"
        assert number == 42

    def test_parse_bare_number_pr(self):
        """Test parsing bare number with --pr flag."""
        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        item_type, owner, repo, number = creator._parse_github_url("123", item_type="pr")

        assert item_type == "pr"
        assert number == 123

    def test_parse_github_urls_dot_com(self):
        """Test parsing github.com URL (not github.com)."""
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


class TestConflictHandling:
    """Test branch conflict handling."""

    @patch("subprocess.run")
    def test_branch_exists_prompt_remove(self, mock_run):
        """Test branch exists prompts for removal."""
        # Simulate existing branch in worktrees
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
                stdout="issue-42-fix-db  /tmp/test-git-repo/.worktrees/issue-42-fix-db",
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=["workmux", "remove", "issue-42-fix-db"], returncode=0, stdout="", stderr=""
            ),
        ]

        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        with patch("builtins.input") as mock_input:
            mock_input.return_value = "y"
            # Should NOT raise - user confirms removal
            creator._check_branch_conflict("issue-42-fix-db")

    @patch("subprocess.run")
    def test_branch_exists_user_declines_remove(self, mock_run):
        """Test user declines branch removal."""
        # Simulate existing branch
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
                stdout="issue-42-fix-db  /tmp/test-git-repo/.worktrees/issue-42-fix-db",
                stderr="",
            ),
        ]

        settings = WorktreeSettings(worktree_root=None)
        creator = WorktreeCreator(
            issue_fetcher=Mock(),
            template_renderer=Mock(),
            settings=settings,
        )
        with patch("builtins.input") as mock_input:
            mock_input.return_value = "n"
            # Should raise but with different message
            with pytest.raises(RuntimeError, match="User cancelled"):
                creator._check_branch_conflict("issue-42-fix-db")
