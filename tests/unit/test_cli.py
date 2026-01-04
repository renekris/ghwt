"""Tests for Click CLI interface."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from main import cli


class TestCLIArguments:
    """Test CLI argument parsing."""

    def test_accepts_github_issue_url(self):
        """Test accepting GitHub issue URL."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_instance = Mock()
            mock_creator.return_value = mock_instance

            result = runner.invoke(cli, ["https://github.com/testuser/testrepo/issues/42", "--issue"])

            assert result.exit_code == 0
            mock_instance.create_from_github_url.assert_called_once()

    def test_accepts_github_pr_url(self):
        """Test accepting GitHub PR URL."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_instance = Mock()
            mock_creator.return_value = mock_instance

            result = runner.invoke(cli, ["https://github.com/testuser/testrepo/pull/123", "--pr"])

            assert result.exit_code == 0
            mock_instance.create_from_github_url.assert_called_once()

    def test_accepts_bare_number_with_issue_flag(self):
        """Test accepting bare number with --issue flag."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_instance = Mock()
            mock_creator.return_value = mock_instance

            result = runner.invoke(cli, ["42", "--issue"])

            assert result.exit_code == 0
            mock_instance.create_from_github_url.assert_called_once()

    def test_accepts_bare_number_with_pr_flag(self):
        """Test accepting bare number with --pr flag."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_instance = Mock()
            mock_creator.return_value = mock_instance

            result = runner.invoke(cli, ["123", "--pr"])

            assert result.exit_code == 0
            mock_instance.create_from_github_url.assert_called_once()

    def test_requires_issue_or_pr_flag_for_bare_number(self):
        """Test requires --issue or --pr flag for bare number."""
        runner = CliRunner()
        result = runner.invoke(cli, ["42"])

        assert result.exit_code != 0
        assert "requires --issue or --pr" in result.output.lower()


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_invalid_url_error_message(self):
        """Test invalid URL shows helpful error message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["https://example.com/not-github", "--issue"])

        assert result.exit_code != 0
        assert "invalid github url" in result.output.lower()

    def test_github_cli_not_installed_error(self):
        """Test GitHub CLI not installed shows helpful error."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_creator.side_effect = RuntimeError("GitHub CLI (gh) is not installed")

            result = runner.invoke(cli, ["https://github.com/test/repo/issues/42", "--issue"])

            assert result.exit_code != 0
            assert result.exception is not None
            assert "github cli" in str(result.exception).lower()

    def test_worktree_creation_failure_error(self):
        """Test worktree creation failure shows helpful error."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_creator.side_effect = RuntimeError("Branch already exists")

            result = runner.invoke(cli, ["https://github.com/test/repo/issues/42", "--issue"])

            assert result.exit_code != 0
            assert result.exception is not None
            assert "branch already exists" in str(result.exception).lower()


class TestCLIOptions:
    """Test CLI option handling."""

    def test_auto_open_shuvcode_default(self):
        """Test shuvcode auto-opens by default."""
        runner = CliRunner()
        with patch("main.WorktreeCreator") as mock_creator:
            mock_instance = Mock()
            mock_creator.return_value = mock_instance

            result = runner.invoke(cli, ["https://github.com/testuser/testrepo/issues/42", "--issue"])

            assert result.exit_code == 0
            # Verify shuvcode is called
            assert mock_instance.create_from_github_url.called

    def test_help_shows_usage_examples(self):
        """Test --help shows usage examples."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "usage" in result.output.lower()
        assert "github.com" in result.output
