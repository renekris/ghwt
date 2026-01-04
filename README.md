# ghwt

GitHub WorkTree - Create git worktrees from GitHub issues/PRs with autonomous agent task tracking.

## Features

- Accepts GitHub issue or PR URLs (or bare numbers with flags)
- Auto-detects issue/PR type from URL
- Creates worktrees using workmux
- Generates `WT-TASK.md` with comprehensive 9-section autonomous agent instructions
- Auto-opens shuvcode editor on worktree
- Handles branch conflicts with user confirmation
- Strict error handling with clear error messages
- **Dry-run mode** (skip workmux/shuvcode, generate WT-TASK.md only)
- **WORKTREE_ROOT environment variable** for custom worktree location

## Installation

### Prerequisites

- Python 3.13+
- GitHub CLI (`gh`) installed and authenticated
- workmux CLI tool installed

### Install Tool

```bash
cd worktree-automation
uv pip install -e .
```

This installs the tool as an editable package, making `ghwt` command available system-wide.

### Install Dependencies

```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture)] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh

# Authenticate
gh auth login

# Install workmux (git worktree manager)
gh repo clone https://github.com/yourusername/workmux
cd workmux
cargo install --path .
```

See [workmux documentation](https://github.com/yourusername/workmux) for details.

## Usage

### Basic Usage

```bash
# From GitHub issue URL
ghwt https://github.com/owner/repo/issues/42

# From GitHub PR URL
ghwt https://github.com/owner/repo/pull/123

# From bare issue number (requires --issue flag)
ghwt 42 --issue

# From bare PR number (requires --pr flag)
ghwt 123 --pr

# Dry-run mode (skip workmux, generate WT-TASK.md only)
ghwt 42 --issue --dry-run
```

### Branch Naming Convention

- Issues: `issue-{number}-{sanitized-title}`
- PRs: `pr-{number}-{sanitized-title}`

Example: `issue-42-fix-database-connection-error`

### Branch Conflict Handling

If a worktree with the same branch name exists, the tool prompts:

```bash
Branch 'issue-42-fix-db' already exists. Remove existing worktree? (y/n):
```

- `y`: Removes existing worktree and creates new one
- `n`: Cancels operation (UserCancelled error)

### Environment Variables

```bash
# Set custom worktree root directory
export WORKTREE_ROOT=/path/to/worktrees
ghwt https://github.com/owner/repo/issues/42
```

### Output

The tool generates a `WT-TASK.md` file in the worktree directory with:

1. Worktree Context & Rules
2. HOTL Protocol
3. Self-verification Gates
4. Early PR Guidance
5. Escalation Protocol
6. Status Tracking
7. GitHub Data
8. Implementation Plan
9. Notes & Artifacts

See `WT_TASK_TEMPLATE.md` for the full template structure.

## Architecture

### Components

- **GitHubIssueFetcher** (`github_fetcher.py`): Fetches issue/PR data via `gh` CLI
  - `fetch_issue()`: Issue data with comments, labels, state
  - `fetch_pr()`: PR data with file changes, merge status

- **TemplateRenderer** (`template_renderer.py`): Renders WT-TASK.md template
  - `render_for_issue()`: Replace placeholders with issue data
  - `render_for_pr()`: Replace placeholders with PR data

- **WorktreeCreator** (`worktree_creator.py`): Orchestrates worktree creation
  - URL parsing and type detection
  - Branch name generation
  - Conflict handling
  - Worktree creation via workmux (or dry-run mode for testing)
  - Task file generation with path context (PARENT_PATH, WORKTREE_NAME, BRANCH_NAME, CREATED_DATE)
  - Auto-opening shuvcode (skip in dry-run mode)

- **CLI** (`main.py`): Click command-line interface
  - Input validation (URL vs bare number)
  - Error handling and user feedback
  - Integration with all components

### Data Models

- `IssueData`: Issue metadata (title, body, number, author, labels, state, url, comments)
- `PRData`: PR metadata (same as Issue + branches, mergeable, changes)
- `CommentData`: Comment metadata (author, body, created_at)
- `FileChange`: File change metadata (path)

### Error Handling

All errors raise `RuntimeError` or `ValueError` with descriptive messages:

- Invalid GitHub URL → ValueError
- GitHub CLI not installed → RuntimeError
- GitHub CLI timeout → RuntimeError
- GitHub CLI fetch failure → RuntimeError
- Worktree creation failure → RuntimeError
- Task file write failure → RuntimeError
- User cancelled conflict → RuntimeError

### Timeouts

- GH_CLI_TIMEOUT: 30 seconds
- WORKMUX_TIMEOUT: 60 seconds
- FILE_WRITE_TIMEOUT: 5 seconds

## Development

### Running Tests

```bash
# Run all unit tests (fast, no external dependencies)
PYTHONPATH=. uv run pytest tests/ -v -c /dev/null

# Run integration tests (external services with mocks)
PYTHONPATH=. uv run pytest tests/ --integration -v

# Run e2e tests (full workflow with temporary repositories)
PYTHONPATH=. uv run pytest tests/ --e2e -v

# Run specific test file
PYTHONPATH=. uv run pytest tests/unit/test_worktree_creator.py -v -c /dev/null

# Run with coverage
PYTHONPATH=. uv run pytest tests/ --cov=ghwt --cov-report=html

# Run specific test class
PYTHONPATH=. uv run pytest tests/integration/test_github_integration.py::TestGitHubIntegration::test_fetch_issue_success -v
```

### Test Structure

The test suite follows a 3-tier testing strategy:

- **Unit tests** (`tests/unit/`): Fast tests with no external dependencies (use mocks)
  - 42 tests currently passing
  - Run by default (skips integration/e2e)
  - Target: < 30 seconds total

- **Integration tests** (`tests/integration/`): Tests with external services (GitHub CLI, workmux, file I/O)
  - Use pytest-subprocess for mocking external binaries
  - Test GitHub CLI wrapper and worktree creation
  - Run with `--integration` flag

- **E2E tests** (`tests/e2e/`): Full workflow tests with temporary git repositories
  - Test complete CLI workflow from command to WT-TASK.md output
  - Use Click's CliRunner for CLI testing
  - Run with `--e2e` flag

### Test Markers

Tests use pytest markers for categorization:
- `@pytest.mark.unit`: Fast unit tests (default)
- `@pytest.mark.integration`: Integration tests requiring external services
- `@pytest.mark.e2e`: End-to-end workflow tests
- `@pytest.mark.slow`: Tests taking >30 seconds

By default, pytest runs only unit tests. Use flags to run integration or e2e tests:

```bash
# Run only unit tests (default)
uv run pytest tests/

# Run unit + integration tests
uv run pytest tests/ -m "not e2e"

# Run all tests (unit + integration + e2e)
uv run pytest tests/ -m "not slow"
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Format code
uv run ruff format .

# Type checking (if mypy is configured)
uv run mypy .
```

### Project Structure

```
worktree-automation/
├── main.py                  # Click CLI entry point
├── github_fetcher.py        # GitHub CLI wrapper
├── template_renderer.py     # WT-TASK.md template rendering
├── worktree_creator.py      # Worktree orchestration
├── models.py                # Dataclass definitions
├── WT_TASK_TEMPLATE.md      # 9-section agent instruction template
├── pyproject.toml           # Package configuration
├── pytest.ini              # Pytest configuration with test markers
└── tests/                   # Test suite
    ├── conftest.py         # Shared fixtures for all tests
    ├── unit/               # Fast unit tests (42 tests)
    │   ├── test_cli.py
    │   ├── test_template_validation.py
    │   ├── test_url_parsing.py
    │   ├── test_worktree_automation.py
    │   └── test_worktree_creator.py
    ├── integration/         # Integration tests with mocked external binaries
    │   ├── test_github_integration.py
    │   └── test_worktree_creator_integration.py
    └── e2e/               # End-to-end workflow tests
        └── test_full_workflow.py
```

## Requirements

- Python 3.13+
- `click>=8.0.0`
- GitHub CLI (`gh`) installed and authenticated
- workmux CLI tool installed

## Troubleshooting

### GitHub CLI Not Found

```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture)] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh

# Authenticate
gh auth login
```

### Worktree Creation Fails

- Ensure workmux is installed: `which workmux`
- Check workmux permissions: Ensure you can write to `.worktrees/`
- Verify GitHub authentication: `gh auth status`

### Template File Not Found

- Ensure `WT_TASK_TEMPLATE.md` exists in the same directory as `main.py`
- The template is loaded from `Path(__file__).parent / "WT_TASK_TEMPLATE.md"`

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`uv run pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Changelog

### Version 0.1.0 (2026-01-04)

- Initial release as `ghwt` command
- GitHub issue/PR fetching via `gh` CLI
- Worktree creation via workmux
- WT-TASK.md generation with 9-section autonomous agent template
- Branch conflict handling with user confirmation
- Auto-opening shuvcode editor
- Dry-run mode for testing template generation without worktrees
- **3-tier test strategy**: 42 unit tests + 18 integration tests + 9 e2e tests = 69 total tests
- **pytest-subprocess** for mocking external binaries
- **Test markers** for categorizing unit/integration/e2e tests
- **WORKTREE_ROOT** environment variable support
