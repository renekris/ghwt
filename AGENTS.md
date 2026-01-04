# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-04
**Commit:** HEAD
**Branch:** main

## OVERVIEW
GitHub WorkTree (ghwt) - CLI tool that creates isolated git worktrees from GitHub issues/PRs with autonomous agent task tracking files.

## STRUCTURE
```
./
├── main.py                  # Click CLI entry point
├── github_fetcher.py        # GitHub CLI wrapper (gh)
├── template_renderer.py     # WT-TASK.md rendering
├── worktree_creator.py      # Core orchestration logic
├── models.py               # Dataclass definitions
├── config.py               # Pydantic settings management
├── logging_config.py        # Structlog configuration
├── WT_TASK_TEMPLATE.md      # 9-section agent instruction template
├── pyproject.toml          # Package config (flat module layout)
├── pytest.ini             # 3-tier test markers
├── .pre-commit-config.yaml # Ruff + security hooks
└── tests/                 # Unit/integration/e2e tests (13 files)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI entry point | `main.py` | Click command `ghwt` |
| GitHub fetching | `github_fetcher.py` | Wraps `gh` CLI |
| Worktree orchestration | `worktree_creator.py` | URL parsing, branch naming |
| Template rendering | `template_renderer.py` | WT-TASK.md generation |
| Data models | `models.py` | IssueData, PRData, CommentData |
| Configuration | `config.py` | Pydantic V2 settings |
| Test definitions | `pytest.ini` | Markers: unit/integration/e2e/slow |
| Shared fixtures | `tests/conftest.py` | 25+ reusable fixtures |

## CONVENTIONS (Deviations from Standard)

### Package Structure
**Non-standard**: Flat module layout (all .py in root) instead of `src/ghwt/` package.
- Uses `py-modules` in pyproject.toml
- Root `__init__.py` creates implicit package
- Prefer refactoring to standard `src/package_name/` layout for future maintainability

### Branch Naming
**Enforced convention**:
- Issues: `issue-{number}-{sanitized-title}`
- PRs: `pr-{number}-{sanitized-title}`
- Example: `issue-42-fix-database-connection-error`

### Test Organization
**3-tier strategy** (uncommon):
- Unit (42 tests): Fast, mocks only, default run
- Integration (18 tests): External services with mocked binaries
- E2E (9 tests): Full workflow with temp git repos
- Markers: `@pytest.mark.unit/integration/e2e/slow`
- Default: Only unit tests run (`-m "not integration and not e2e"`)

### CI/CD
**Missing**: No GitHub Actions workflows in `.github/workflows/` (empty directory).
- Relies on pre-commit hooks for quality enforcement
- Tests run on pre-push (unusual - typically pre-commit)
- Consider adding CI for automated testing on PRs

### Python 3.13+ Standards
**Enforced**:
- Type syntax: `str | None` (NOT `Optional[str]`)
- Collections: `list[str]`, `dict[str, int]` (NOT `typing.List`)
- Type hints: Required for all functions (no `Any` types)
- Pydantic V2 for data validation

### Import Style
**Forbidden**: Relative imports (`from .module import X`)
**Required**: Full paths for internal imports

## ANTI-PATTERNS (THIS PROJECT)

### Code Structure
- **NEVER** use relative imports - use full Python paths
- **NEVER** hard-code service instantiation - use dependency injection
- **NEVER** use `# type: ignore` - cast or fix properly
- **NEVER** leave empty catch blocks - handle with specific messages

### Agent Behavior (Ultrawork Mode)
- **NEVER** plan yourself - ALWAYS spawn planning agents
- **NEVER** wait sequentially - Fire independent agents in parallel
- **NEVER** stop at first result - Be exhaustive in searches
- **ALWAYS** tell user which agents you'll leverage BEFORE starting

### Development Workflow
- **NEVER** delete tests to fix failures - Fix code instead
- **NEVER** stop at 60-80% completion - Deliver full implementation
- **ALWAYS** use TDD cycle: Spec → Test (fail) → Implement → Pass → Refactor

## UNIQUE STYLES

### WT-TASK.md Template
9-section autonomous agent instruction file:
1. Worktree Context & Rules
2. HOTL Protocol
3. Self-verification Gates
4. Early PR Guidance
5. Escalation Protocol
6. Status Tracking
7. GitHub Data
8. Implementation Plan
9. Notes & Artifacts

### Pre-Commit Hooks
**Comprehensive security-first**:
- Ruff (linting + formatting)
- TruffleHog (secrets detection)
- Semgrep (SAST patterns, ERROR-only)
- General file checks (YAML, TOML, merge conflicts)
- **Tests run on pre-push** (not pre-commit)

### Environment Variables
- `WORKTREE_ROOT`: Custom worktree location
- `GH_TOKEN`: GitHub authentication (via gh CLI)

## COMMANDS
```bash
# Installation
uv pip install -e .

# Development
uv run ruff check .
uv run ruff format .
uv run pytest tests/                    # Unit tests only (default)
uv run pytest tests/ --integration      # Unit + integration
uv run pytest tests/ --e2e             # Unit + integration + e2e
uv run pytest tests/ --cov=ghwt       # With coverage

# Usage
ghwt https://github.com/owner/repo/issues/42
ghwt 123 --pr --dry-run               # Skip workmux/shuvcode
ghwt 42 --issue --verbose              # Debug logging
```

## NOTES

### Gotchas
- **Missing LICENSE file**: pyproject.toml specifies MIT but no LICENSE file exists
- **No CI workflows**: Empty `.github/workflows/` directory - all quality checks are local
- **Root entry point**: Uses `main.py` pattern instead of package entry point - less reusable as library

### External Dependencies
- **GitHub CLI (`gh`)**: Required, must be authenticated
- **workmux**: Required for worktree creation (skip with `--dry-run`)
- **shuvcode**: Auto-opened editor (skip with `--dry-run`)

### Test Architecture
- **pytest-subprocess**: For mocking external binaries in integration tests
- **Click's CliRunner**: For E2E CLI testing
- **25+ fixtures**: In conftest.py for consistent mocking across all tiers

### Timeouts (Defined in code)
- `GH_CLI_TIMEOUT`: 30 seconds
- `WORKMUX_TIMEOUT`: 60 seconds
- `FILE_WRITE_TIMEOUT`: 5 seconds

### Error Handling
All errors raise `RuntimeError` or `ValueError` with descriptive messages:
- Invalid GitHub URL → ValueError
- GitHub CLI not installed → RuntimeError
- Worktree creation failure → RuntimeError
- User cancelled conflict → RuntimeError
