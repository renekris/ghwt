# TESTS KNOWLEDGE BASE

**Generated:** 2026-01-04
**Scope:** tests/ directory

## OVERVIEW
3-tier pytest test suite (69 total tests) with comprehensive mocking fixtures for CLI tool testing.

## STRUCTURE
```
tests/
├── conftest.py           # 25+ shared fixtures (mocks for gh, workmux, subprocess)
├── unit/                 # 42 fast tests with mocks only
├── integration/          # 18 tests with mocked external binaries
└── e2e/                 # 9 full workflow tests with temp git repos
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Shared fixtures | `conftest.py` | 25+ reusable mocks (GitHub CLI, workmux, user input) |
| Unit tests | `tests/unit/` | Fast, no external dependencies |
| Integration tests | `tests/integration/` | External services with pytest-subprocess |
| E2E tests | `tests/e2e/` | Click CliRunner + temp repos |
| Test config | `pytest.ini` | Markers: unit/integration/e2e/slow |

## CONVENTIONS

### Test Markers
- `@pytest.mark.unit`: Fast tests (default run)
- `@pytest.mark.integration`: External services (use `--integration` flag)
- `@pytest.mark.e2e`: Full workflow (use `--e2e` flag)
- `@pytest.mark.slow`: Tests >30 seconds

### Default Behavior
**Only unit tests run** by default via `-m "not integration and not e2e"` in pytest.ini.

### Fixtures
**High reuse** - All mocks in `conftest.py`:
- `mock_github_cli*`: GitHub CLI responses
- `mock_workmux*`: Worktree manager responses
- `mock_user_input_*`: User input mocking
- `mock_subprocess_command_aware`: Complex command-aware mocking

## ANTI-PATTERNS

- **NEVER** test implementation details - focus on behavior
- **NEVER** duplicate mocks - use `conftest.py` fixtures
- **NEVER** hard-code test data - use `sample_issue_data`/`sample_pr_data` fixtures
- **NEVER** skip error scenarios - test all failure paths

## UNIQUE STYLES

### 3-Tier Strategy
**Uncommon in simple projects**:
- Unit: Mock everything, instant feedback
- Integration: Test external service interfaces (not real services)
- E2E: Full workflow from CLI to WT-TASK.md output

### pytest-subprocess
**For integration tests**: Mock external binaries (gh, workmux, shuvcode) while testing subprocess integration.

### Click Testing
**For E2E**: Uses `CliRunner` for complete CLI invocation testing with temp git repos.

## COMMANDS
```bash
# Run only unit tests (default)
uv run pytest tests/

# Run unit + integration
uv run pytest tests/ -m "not e2e"

# Run all tests
uv run pytest tests/ -m "not slow"

# With coverage
uv run pytest tests/ --cov=ghwt --cov-report=html

# Specific test file
uv run pytest tests/unit/test_worktree_creator.py -v
```

## NOTES

### Fixture Dependencies
Some fixtures depend on others (e.g., `worktree_creator` needs `issue_fetcher` + `template_renderer` + `temp_worktree_root`). Check conftest.py for dependency chains.

### Temporary Resources
E2E tests create real git repos and worktree directories in `tmp_path` fixtures - cleanup is automatic.
