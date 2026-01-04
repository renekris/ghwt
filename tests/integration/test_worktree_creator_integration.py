"""Integration tests for WorktreeCreator with mocked external binaries."""

from pathlib import Path

import pytest
from config import WorktreeSettings
from github_fetcher import GitHubIssueFetcher
from template_renderer import TemplateRenderer
from worktree_creator import WorktreeCreator


@pytest.mark.integration
class TestWorktreeCreatorIntegration:
    """Integration tests for worktree creation with external binary mocks."""

    def test_create_worktree_from_issue_url(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path, mock_user_input_yes
    ) -> None:
        """Test creating worktree from GitHub issue URL."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        assert worktree_path.exists()
        assert worktree_path.name == "issue-42-test-issue"
        assert (worktree_path / "WT-TASK.md").exists()

    def test_create_worktree_from_pr_url(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path
    ) -> None:
        """Test creating worktree from GitHub PR URL."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/pull/123", "pr")

        assert worktree_path.exists()
        assert worktree_path.name == "pr-123-test-pr"
        assert (worktree_path / "WT-TASK.md").exists()

    def test_dry_run_mode_integration(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path
    ) -> None:
        """Test dry-run mode creates directory and task file without workmux."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings, dry_run=True)

        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        # Verify directory and task file created
        assert worktree_path.exists()
        assert worktree_path.name == "issue-42-test-issue"
        assert (worktree_path / "WT-TASK.md").exists()

        # Verify no workmux calls made (pytest-subprocess handles this)

    def test_branch_conflict_handling_user_cancels(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path
    ) -> None:
        """Test branch conflict handling when user cancels."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        from unittest.mock import patch

        with pytest.raises(RuntimeError, match="User cancelled"), patch("builtins.input", return_value="n"):
            creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

    def test_branch_conflict_handling_user_accepts(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path, mock_user_input_yes
    ) -> None:
        """Test branch conflict handling when user accepts removal."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        # Verify worktree created after conflict resolution
        assert worktree_path.exists()
        assert (worktree_path / "WT-TASK.md").exists()

    def test_task_file_content_with_issue_data(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path, mock_user_input_yes
    ) -> None:
        """Test task file contains correct issue data."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        task_file = worktree_path / "WT-TASK.md"
        content = task_file.read_text()

        # Verify issue data is present
        assert "Test Issue" in content
        assert "Test issue body" in content
        assert "#42" in content
        assert "testuser" in content
        assert "https://github.com/test/repo/issues/42" in content
        assert "bug" in content

    def test_task_file_all_placeholders_replaced(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path, mock_user_input_yes
    ) -> None:
        """Test all core placeholders are replaced in task file."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        task_file = worktree_path / "WT-TASK.md"
        content = task_file.read_text()

        # Verify core placeholders are replaced (not all placeholders - some are for runtime)
        assert "{{ISSUE_NUMBER}}" not in content
        assert "{{TITLE}}" not in content
        assert "{{AUTHOR}}" not in content
        assert "{{GITHUB_URL}}" not in content
        assert "{{WORKTREE_NAME}}" not in content
        assert "{{BRANCH_NAME}}" not in content
        assert "{{PARENT_PATH}}" not in content

        # Verify context placeholders
        assert str(temp_worktree_root) in content or temp_worktree_root.name in content
        assert "issue-42-test-issue" in content

    def test_task_file_has_all_sections(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path, mock_user_input_yes
    ) -> None:
        """Test task file contains all sections."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)

        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        task_file = worktree_path / "WT-TASK.md"
        content = task_file.read_text()

        # Verify all sections are present
        required_sections = [
            "SECTION 1: WORKTREE CONTEXT & RULES",
            "SECTION 2: HOTL (Human on the Loop) PROTOCOL",
            "SECTION 3: SELF-VERIFICATION CONDITIONS",
            "SECTION 4: EARLY PR CREATION GUIDANCE",
            "SECTION 5: ESCALATION CONDITIONS",
            "SECTION 6: STATUS TRACKING",
            "SECTION 7: GITHUB ISSUE/PR DATA",
            "SECTION 8: IMPLEMENTATION PLAN",
            "SECTION 9: NOTES & ARTIFACTS",
        ]

        for section in required_sections:
            assert section in content, f"Missing section: {section}"

    def test_dry_run_task_file_content_validation(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path
    ) -> None:
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)
        creator = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings, dry_run=True)

        worktree_path = creator.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        task_file = worktree_path / "WT-TASK.md"
        content = task_file.read_text()

        # Verify content is not empty
        assert len(content) > 100

        # Verify issue data is present
        assert "Test Issue" in content

        # Verify core placeholders are replaced (not all placeholders - some are for runtime)
        assert "{{ISSUE_NUMBER}}" not in content
        assert "{{TITLE}}" not in content
        assert "{{AUTHOR}}" not in content
        assert "{{GITHUB_URL}}" not in content
        assert "{{WORKTREE_NAME}}" not in content
        assert "{{BRANCH_NAME}}" not in content
        assert "{{PARENT_PATH}}" not in content

    def test_multiple_worktrees_with_same_issue(
        self, mock_subprocess_command_aware, temp_worktree_root: Path, template_path: Path, mock_user_input_yes
    ) -> None:
        """Test creating multiple worktrees from same issue URL."""
        fetcher = GitHubIssueFetcher()
        renderer = TemplateRenderer(template_path)
        settings = WorktreeSettings(worktree_root=temp_worktree_root)

        # First worktree
        creator1 = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)
        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree1 = creator1.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        # Second worktree (should handle conflict)
        creator2 = WorktreeCreator(issue_fetcher=fetcher, template_renderer=renderer, settings=settings)
        mock_subprocess_command_aware.set_worktree_root(temp_worktree_root)
        worktree2 = creator2.create_from_github_url("https://github.com/testuser/testrepo/issues/42", "issue")

        # Both should have task files
        assert (worktree1 / "WT-TASK.md").exists()
        assert (worktree2 / "WT-TASK.md").exists()
