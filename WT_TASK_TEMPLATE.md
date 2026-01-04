# WT-TASK.md — WorkTree Task Specification

> **Autonomous Agent**: Sisyphus (full agent access: explore, librarian, oracle, frontend-ui-ux-engineer)
> **HOTL**: Human on the Loop — tracks progress, provides guidance
> **Created**: {{CREATED_DATE}}
> **Worktree**: {{WORKTREE_NAME}}
> **Branch**: {{BRANCH_NAME}}
> **Parent**: {{PARENT_PATH}}

---

## 🎯 QUICK REFERENCE

| Field | Value |
|-------|-------|
| **Task Type** | Issue / Pull Request |
| **GitHub Reference** | {{GITHUB_URL}} |
| **Priority** | {{PRIORITY_LABEL}} |
| **Area** | {{AREA_LABEL}} |
| **Status** | {{STATUS_LABEL}} |
| **Estimated Effort** | {{EFFORT_ESTIMATE}} |

---

## 📋 SECTION 1: WORKTREE CONTEXT & RULES

### Worktree Strategy (MANDATORY)

**Parent Directory** (`{{PARENT_PATH}}`) = single source of truth for gitignored data.

**Current Worktree** (`.worktrees/{{WORKTREE_NAME}}`) = code-only workspace with symlinks.

**Symlink Verification (Required on start):**
```bash
# Verify symlinks exist in worktree root
ls -la | grep "^l"

# Expected output:
# .env -> ../../.env
# data -> ../../data
# logs -> ../../logs

# If missing, recreate:
ln -s ../../.env . && ln -s ../../data . && ln -s ../../logs .
```

**Worktree Workflow:**
1. ✅ Work in isolated `.worktrees/{{WORKTREE_NAME}}/` directory
2. ✅ All changes happen in feature branch: `{{BRANCH_NAME}}`
3. ✅ Symlinks provide access to parent's `.env`, `data/`, `logs/`
4. ✅ No gitignored data in worktree (via symlinks to parent)
5. ✅ Merge to parent's `dev` branch when complete
6. ✅ Clean up worktree after merge

### Codebase Conventions (STRICT COMPLIANCE)

**Python 3.13+ Standards:**
- Use `str | None` syntax (NOT `Optional[str]` or `Union[str, None]`)
- Use `list[str]`, `dict[str, int]`, `set[str]` (NOT `typing.List`, `typing.Dict`)
- Use `collections.abc.Sequence` for protocols (NOT `typing.Sequence`)
- Use `type` keyword for type aliases: `type UserID = int`
- Use `def[T]()` syntax for generics (NOT `TypeVar`)
- Use `@override` decorator for interface implementations
- Concrete types for runtime checks, abstract protocols for interface flexibility

**Import Paths (MANDATORY):**
- ALWAYS use full Python paths: `from backend.services.GeminiAIProvider import GeminiAIProvider`
- NEVER use relative imports: `from .GeminiAIProvider import GeminiAIProvider`
- Group imports: standard → third-party → local

**Naming Conventions:**
- Classes: PascalCase (`DatabaseService`)
- Functions/variables: snake_case (`store_property`)
- Private methods: `_extract_contacts_regex`
- Interfaces: Prefix `I` (`IAIProvider`)
- Constants: UPPER_SNAKE_CASE (`DEFAULT_TIMEOUT`)

**Development Rules (ZERO TOLERANCE):**
- NO `pass` blocks — log or raise errors
- NO `# type: ignore` — cast or fix types
- NO empty catch blocks — always handle with specific messages
- Type all function parameters and return values
- Use Pydantic V2 for data validation
- All I/O must be async/await
- Never hard-code secrets — use environment variables

**Type Safety (STRICT):**
- Add explicit type or `@final` decorator for class attributes
- Use `@override` from `typing` on interface method implementations
- Type all untyped variables/parameters (never leave as `Any`)
- Assign to `_` if intentionally discarding results
- Type variables at assignment point to prevent cascading `Any` types

**Common Linter Errors & Fixes:**

**Override decorator missing:**
```python
# ❌ ERROR
class BusinessSearch(IBusinessSearch):
    def find_tenants_at_address(self) -> list[Tenant]:

# ✅ FIX
from typing import override
class BusinessSearch(IBusinessSearch):
    @override
    def find_tenants_at_address(self) -> list[Tenant]:
```

**Type is Any (untyped parameters):**
```python
# ❌ ERROR
tenant_data = ...
result = tenants.append(tenant_data)

# ✅ FIX
tenant_data: dict[str, Any] = {}
result = tenants.append(tenant_data)
```

**@final decorator for untyped attributes:**
```python
# ❌ ERROR
class MyService:
    business_search

# ✅ FIX
from typing import final
@final
class MyService:
    business_search: IBusinessSearch
```

**Database Types:**
- Use `cast()` for dynamic libraries (SQLAlchemy, aiosqlite):
  ```python
  from typing import cast
  conn = cast(Connection, _conn)
  rows = cast(list[sqlite3.Row], await cursor.fetchall())
  ```

### Dependency Injection Patterns (MANDATORY)

**Core Principles:**
- **Constructor Injection Only**: ALL agent dependencies via constructor
- **Interface-Based Design**: Define contracts for ALL agent services
- **Explicit Dependencies**: Make ALL dependencies explicit through constructor parameters
- **No Hard Dependencies**: NEVER hard-code service instantiation

**Service Creation Pattern:**
```python
# 1. Define interface
from abc import ABC, abstractmethod
class IMyService(ABC):
    @abstractmethod
    async def do_something(self, data: str) -> dict[str, Any]:
        pass

# 2. Implement service
class MyService(IMyService):
    @override
    def __init__(self, dependency: IOtherService, config: IConfig):
        self._dependency = dependency
        self._config = config

    @override
    async def do_something(self, data: str) -> dict[str, Any]:
        result = await self._dependency.process(data)
        return {"processed": result}

# 3. Create factory
def create_my_service(
    dependency: IOtherService = Depends[IOtherService],
    config: IConfig = Depends[IConfig]
) -> IMyService:
    return MyService(dependency=dependency, config=config)

# 4. Register in container
container.register(Singleton(create_my_service, IMyService))
```

**DI Resolution Pattern:**
```python
# NEVER hard-code service instantiation
# ❌ WRONG
class Agent:
    def __init__(self):
        self.service = MyService()  # Hard dependency

# ✅ CORRECT
class Agent:
    def __init__(self, service: IMyService):
        self._service = service  # Injected dependency

# Resolve from container
async with container.context() as ctx:
    service = await ctx.resolve(IMyService)
    agent = Agent(service=service)
```

### TDD Workflow (STRICT COMPLIANCE)

**Test-Driven Development Cycle:**
```
1. Write spec (requirements from issue/PR)
2. Write tests (failing)
3. RED: Run tests, confirm they fail
4. Implement minimal code to pass
5. GREEN: Run tests, confirm they pass
6. Refactor if needed (must stay green)
7. Next feature, repeat
```

**Test Structure:**
- Use pytest fixtures (see `tests/conftest.py`, `tests/conftest_postgres.py`)
- Mark tests: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.postgres`
- Test happy paths AND error conditions
- Naming: `test_[subject]_[scenario]_[expected_result]`

**Test Commands:**
```bash
# Run all tests
uv run pytest

# Run single test
uv run pytest tests/test_di_container.py::test_container_resolution

# Run with markers
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m postgres

# Coverage
uv run pytest --cov=backend --cov-report=html --cov-fail-under=30
```

### Ultrawork Mode Rules (MAXIMUM PRECISION)

**Agent Utilization Principles:**
- **Tell User WHAT Agents You Will Leverage NOW** before starting
- **Background First**: Use `background_task` for exploration/research agents
- **Parallel Execution**: Launch 10+ independent agents simultaneously
- **Wait for Notifications**: System notifies when agents complete
- **Delegate**: Don't do everything yourself — orchestrate specialized agents

**Agent Types & When to Use:**
- **Explore Agents**: Codebase patterns, file structures, AST-grep searches
- **Librarian Agents**: Remote repos, official docs, GitHub examples
- **Oracle Agents**: Strategic guidance (block=true, 5min timeout) for complex decisions
- **Planning Agents**: Work breakdown (NEVER plan yourself)
- **Frontend UI/UX**: Design and implementation

**Execution Rules:**
- TODO: Track EVERY step. Mark complete IMMEDIATELY after each.
- PARALLEL: Fire independent agent calls via background_task
- BACKGROUND FIRST: Exploration/research before direct tools
- VERIFY: Re-read request after completion. Check ALL requirements met.
- DELEGATE: Orchestrate specialized agents for their strengths

**Zero Tolerance Failures:**
- NO scope reduction: Deliver FULL implementation
- NO mockup work: 100% working feature, no demo/skeleton
- NO partial completion: Never stop at 60-80%
- NO assumed shortcuts: Complete all requirements
- NO premature stopping: Declare done only when ALL TODOs complete
- NO test deletion: Fix code, not tests

---

## 📋 SECTION 2: HOTL (Human on the Loop) PROTOCOL

### When to Engage HOTL

**MUST Engage (Block & Wait for Approval):**
1. **Critical Design Decisions**: Architecture choices affecting multiple systems
2. **Breaking Changes**: API changes, schema migrations, interface changes
3. **Security Concerns**: Vulnerability discovery, authentication changes
4. **Performance Regressions**: Identified >20% degradation
5. **Stalemate Situations**: 3+ failed attempts at same problem with different approaches
6. **Scope Changes**: Requirements appear impossible or significantly larger than estimated
7. **Early PR Creation**: Before creating PR for critical findings (see Section 5)

**Should Engage (Inform, Don't Block):**
1. **Progress Milestones**: Major features completed, ready for review
2. **Interesting Findings**: Unexpected behavior, optimization opportunities
3. **Blockers Encountered**: External dependencies, missing resources, unclear requirements
4. **Decisions Made**: Document rationale for non-trivial choices

**Can Proceed (Inform Later):**
1. **Routine Implementation**: Following established patterns
2. **Bug Fixes**: Clear error, straightforward solution
3. **Test Failures**: Self-contained within scope, clear fix path
4. **Code Refactoring**: No behavior change, internal improvements

### HOTL Update Format

**Regular Updates (Every 30-60 minutes):**
```markdown
## 🤖 Sisyphus Progress Update

**Time**: {{CURRENT_TIME}}
**Status**: {{WORKING_ON}}

### ✅ Completed
- [x] Task 1 (5 min)
- [x] Task 2 (10 min)

### 🔄 In Progress
- [ ] Task 3 (currently: {{CURRENT_ACTION}})

### 🚧 Blockers
- [ ] Blocker 1 (waiting for: {{WHAT_NEEDED}})

### 💡 Decisions
- Decision 1: Rationale - {{WHY}}, Alternatives considered: {{OPTIONS}}

### 🎯 Next Steps
1. Next immediate step
2. Planned follow-up
```

**Critical Updates (Immediately):**
```markdown
## 🚨 CRITICAL: {{ISSUE_TYPE}}

**Issue**: {{DESCRIPTION}}
**Impact**: {{HOW_THIS_BLOCKS_PROGRESS}}
**Options**:
1. Option A: {{PROS_AND_CONS}}
2. Option B: {{PROS_AND_CONS}}
3. Option C: {{PROS_AND_CONS}}

**Recommendation**: Option {{LETTER}} ({{REASON}})

**Waiting for HOTL decision**: [ ] Proceed with Option {{LETTER}} | [ ] Different approach
```

### HOTL Response Handling

**When HOTL Provides Input:**
1. **Acknowledge**: Confirm understanding of instruction
2. **Integrate**: Update approach based on feedback
3. **Proceed**: Continue with adjusted plan
4. **Verify**: Ensure new direction aligns with requirements

**When HOTL Asks Questions:**
1. **Answer Directly**: Provide specific information requested
2. **Show Context**: Include relevant code, logs, or data
3. **Offer Options**: If multiple valid approaches exist
4. **Recommend**: Suggest best path based on requirements

---

## 📋 SECTION 3: SELF-VERIFICATION CONDITIONS

### Before Declaring Work Complete (MANDATORY CHECKLIST)

**1. Code Quality Checks:**
```bash
# Linting (no errors allowed)
uv run ruff check .
# Expected: 0 errors, 0 warnings

# Formatting (no changes needed)
uv run ruff format --check .
# Expected: No files need formatting

# Type checking (strict mode)
uv run mypy backend --strict
# Expected: Success, no errors

# Security scan
uv tool run trufflehog --json . > trufflehog-results.json
# Expected: No secrets detected (or explicitly approved exceptions)
```

**2. Functional Verification:**
```bash
# Backend tests
uv run pytest --cov=backend --cov-fail-under=30
# Expected: All tests pass, coverage ≥30%

# Frontend tests (if applicable)
cd frontend && pnpm run test:run
# Expected: All tests pass

# E2E tests (if applicable)
cd frontend && pnpm run test:e2e
# Expected: All tests pass

# Build check
uv run python -c "import backend; print('OK')"
cd frontend && pnpm run build
# Expected: No build errors
```

**3. DI Integrity:**
```bash
# Verify all services resolve from container
uv run python -c "
import asyncio
from backend.container.di_container import container

async def check():
    async with container.context() as ctx:
        # Test key services resolve
        services = [
            'backend.services.ai.gemini_ai_provider.GeminiAIProvider',
            'backend.services.data.database_service.DatabaseService',
        ]
        for service_path in services:
            try:
                # Attempt resolution
                pass
            except Exception as e:
                print(f'FAILED: {service_path}: {e}')
                raise

asyncio.run(check())
"
# Expected: All services resolve without errors
```

**4. Database Verification:**
```bash
# PostgreSQL migrations (if applicable)
uv run alembic upgrade head
# Expected: No migration errors

# Schema validation (if applicable)
uv run python -c "
import asyncio
from backend.services.data.database_service import DatabaseService

async def verify():
    db = DatabaseService()
    await db.initialize()
    # Verify key tables exist
    result = await db.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = %s', ('adduco_dev',))
    tables = [row[0] for row in result]
    required = ['properties', 'business_searches', 'moving_lead_tracking']
    for table in required:
        assert table in tables, f'Missing table: {table}'
    print(f'✅ All required tables present: {tables}')

asyncio.run(verify())
"
# Expected: All required tables present
```

**5. PR Readiness Criteria:**
- [ ] All tests pass (backend + frontend + e2e)
- [ ] Code quality checks pass (ruff, mypy, trufflehog)
- [ ] Coverage threshold met (≥30%)
- [ ] New/updated tests for changed code
- [ ] Documentation updated (if applicable)
- [ ] Breaking changes documented (if applicable)
- [ ] Migration scripts provided (if schema changes)
- [ ] No `# type: ignore` (unless absolutely necessary and documented)
- [ ] No `pass` blocks (all implemented or logged)
- [ ] No empty catch blocks (all exceptions handled)
- [ ] All imports follow full path convention
- [ ] All dependencies injected via DI (no hard-coded instantiation)

### Edge Cases to Cover

**Error Handling:**
- [ ] Network failures handled gracefully
- [ ] External API timeouts handled with retries
- [ ] Invalid input returns clear error messages
- [ ] Database connection failures don't crash app
- [ ] File system errors handled (missing files, permissions)

**Performance:**
- [ ] No N+1 query problems
- [ ] Large files handled efficiently (streaming, not loading all)
- [ ] Caching used appropriately for expensive operations
- [ ] Async/await used for all I/O
- [ ] Connection pooling configured for DB/external services

**Security:**
- [ ] User input validated before use
- [ ] SQL injection prevented (ORM only, no string concatenation)
- [ ] Secrets not logged or exposed in errors
- [ ] Authentication/authorization checks in place
- [ ] Rate limiting configured (if applicable)

**Compatibility:**
- [ ] Works on Python 3.13+
- [ ] PostgreSQL and SQLite support (if applicable)
- [ ] Frontend works in modern browsers (Chrome, Firefox, Safari, Edge)
- [ ] Responsive design (mobile + desktop)
- [ ] Environment variables properly defaulted

---

## 📋 SECTION 4: EARLY PR CREATION GUIDANCE

### What Constitutes "Critical Finding" Worth Early PR

**Create Early PR When:**

**Security Vulnerabilities:**
- Secret exposure in logs or errors
- Authentication bypass possible
- SQL injection vectors
- XSS vulnerabilities in frontend
- Privilege escalation paths

**Performance Regressions:**
- Identified >20% performance degradation
- N+1 query problems discovered
- Memory leaks or excessive resource usage
- Database blocking issues

**Breaking Changes Required:**
- API interface changes affecting multiple callers
- Database schema migrations requiring data migration
- Dependency upgrades with breaking changes
- Interface contract changes requiring widespread updates

**Architecture Issues:**
- Design flaw requiring significant rework
- Dependency injection violations discovered
- Circular dependencies preventing resolution
- Scalability bottlenecks

**Blockers Found:**
- Missing critical functionality for completion
- External API changes breaking integration
- Third-party library bugs requiring workarounds
- Environment-specific issues not replicable locally

### Early PR Structure

**Title Format:** `[WIP] Critical Finding: {{BRIEF_DESCRIPTION}} (#{{ISSUE_NUMBER}})`

**Body Template:**
```markdown
## 🚨 Critical Finding Discovered

**Issue**: {{ISSUE_NUMBER}} - {{ISSUE_TITLE}}

### What Was Found

{{DESCRIPTION_OF_FINDING}}

### Impact

- **Severity**: {{CRITICAL/HIGH/MEDIUM/LOW}}
- **Scope**: {{WHAT_SYSTEMS_AFFECTED}}
- **Risk**: {{WHY_THIS_MATTERS}}

### Current Status

- [ ] Finding documented
- [ ] Root cause identified
- [ ] Proposed solution outlined
- [ ] Initial implementation in progress
- [ ] Tests being written
- [ ] HOTL review requested

### Next Steps

1. {{IMMEDIATE_ACTION}}
2. {{FOLLOW_UP_ACTION}}
3. {{COMPLETION_CRITERIA}}

### HOTL Input Needed

{{DECISION_REQUIRED_OR_PROGRESS_REPORT}}

---

**Note**: This is an EARLY PR to track critical findings. Not ready for merge. Status updates will be added as work progresses.
```

### Updating PR with Progress

**Add Update Comments When:**
- Root cause confirmed
- Solution designed and approved
- Implementation started
- Tests written
- HOTL feedback incorporated
- Ready for review

**Comment Template:**
```markdown
### Progress Update — {{DATE_TIME}}

**Status**: {{IN_PROGRESS/READY_FOR_REVIEW/BLOCKED}}

**Completed Since Last Update:**
- {{WHAT_WAS_DONE}}

**Current Work:**
- {{CURRENTLY_IMPLEMENTING}}

**Blockers:**
- {{IF_ANY}}

**ETA for Next Update**: {{WHEN_TO_EXPECT_NEXT_UPDATE}}
```

### When to Merge vs Keep as WIP

**Merge Early PR When:**
- [ ] Critical finding verified by HOTL
- [ ] Solution approved by HOTL
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Documentation updated
- [ ] HOTL approval received

**Keep as WIP When:**
- [ ] Waiting for HOTL decision
- [ ] Implementing complex solution (multi-day)
- [ ] Testing in progress
- [ ] Gathering additional information

---

## 📋 SECTION 5: ESCALATION CONDITIONS

### When to Escalate to Oracle vs Proceed

**Escalate to Oracle (block=true, 5min timeout) When:**

**After 3+ Failed Attempts:**
- Same problem approached 3+ different ways without success
- Each attempt failed with different error
- No clear path forward from research

**Design Seems Flawed or Suboptimal:**
- Current approach feels overcomplicated
- Simpler solution might exist but not obvious
- Architecture decision has significant trade-offs

**Stuck on Architecture Decision:**
- Multiple valid approaches, unclear which is best
- Impact on future extensibility uncertain
- Performance implications not quantifiable

**Security/Performance Concerns:**
- Discovered potential security issue
- Performance degradation identified but cause unclear
- Need expert guidance on best practices

**External Dependencies Blocking:**
- Third-party library unclear or poorly documented
- API behavior inconsistent or undocumented
- Workaround requires advanced techniques

**Proceed Without Oracle When:**

**Clear Path Forward:**
- Error messages provide actionable information
- Documentation or examples exist showing solution
- Similar code in codebase provides pattern

**Routine Implementation:**
- Following established patterns in codebase
- Straightforward CRUD operations
- Standard library functionality

**Test Failures with Clear Fix:**
- Test failure shows exact problem
- Fix path is obvious from error
- No ambiguity in what needs to change

### Oracle Query Format

```markdown
# Oracle Query: {{BRIEF_SUMMARY}}

## Context
Working on issue/PR: {{GITHUB_URL}}
Task: {{WHAT_TRYING_TO_ACCOMPLISH}}

## Attempts Made
1. **Approach A**: {{DESCRIPTION}}
   - Result: {{OUTCOME}}, Error: {{ERROR_IF_ANY}}
   - Why failed: {{REASON}}

2. **Approach B**: {{DESCRIPTION}}
   - Result: {{OUTCOME}}, Error: {{ERROR_IF_ANY}}
   - Why failed: {{REASON}}

3. **Approach C**: {{DESCRIPTION}}
   - Result: {{OUTCOME}}, Error: {{ERROR_IF_ANY}}
   - Why failed: {{REASON}}

## Current Blocker
{{WHAT_IS_BLOCKING_PROGRESS}}

## Information Gathered
{{SUMMARY_OF_RESEARCH,_DOCUMENTATION,_CODE_EXAMPLES}}

## Questions for Oracle
1. {{SPECIFIC_QUESTION_1}}
2. {{SPECIFIC_QUESTION_2}}
3. {{SPECIFIC_QUESTION_3}}

## Decision Needed
{{WHAT_GUIDANCE_NEEDED_TO_PROCEED}}

## Alternative Ideas
{{ANY_ALTERNATIVE_APPROACHES_TO_CONSIDER}}
```

---

## 📋 SECTION 6: STATUS TRACKING

### Current Status

| Field | Value |
|-------|-------|
| **Overall Status** | 🔄 In Progress / ✅ Complete / 🚫 Blocked |
| **Started** | {{START_TIME}} |
| **Last Updated** | {{LAST_UPDATE_TIME}} |
| **Estimated Completion** | {{ETA}} |

### Progress Checklist

**From Issue/PR Requirements:**
- [ ] {{REQUIREMENT_1}}
- [ ] {{REQUIREMENT_2}}
- [ ] {{REQUIREMENT_3}}

**From Acceptance Criteria:**
- [ ] {{ACCEPTANCE_CRITERION_1}}
- [ ] {{ACCEPTANCE_CRITERION_2}}
- [ ] {{ACCEPTANCE_CRITERION_3}}

### Blockers

| # | Blocker | Severity | Status | Since |
|---|----------|----------|--------|-------|
| 1 | {{BLOCKER_DESCRIPTION}} | {{CRITICAL/HIGH/MEDIUM/LOW}} | {{ACTIVE/RESOLVED}} | {{DATETIME}} |

### Decisions Log

| Time | Decision | Rationale | Alternatives Considered |
|-------|----------|------------|----------------------|
| {{DATETIME}} | {{DECISION_MADE}} | {{WHY_THIS_DECISION}} | {{OPTION_A, OPTION_B, OPTION_C}} |

### Next Steps

**If Unblocked:**
1. {{NEXT_IMMEDIATE_ACTION}}
2. {{FOLLOW_UP_ACTION}}

**If Blocked:**
- Waiting for: {{WHAT_NEEDED_TO_UNBLOCK}}
- ETA for resolution: {{WHEN_EXPECTED}}

**If Resuming Work:**
- Last checkpoint: {{WHAT_WAS_LAST_COMPLETED}}
- Resume at: {{WHERE_TO_PICK_UP}}

---

## 📋 SECTION 7: GITHUB ISSUE/PR DATA

### Metadata

```yaml
Type: {{ISSUE_OR_PR}}
Number: {{ISSUE_OR_PR_NUMBER}}
URL: {{GITHUB_URL}}
Title: {{TITLE}}
Author: {{AUTHOR}}
Created: {{CREATED_DATE}}
Updated: {{LAST_UPDATED}}
Labels:
  - {{LABEL_1}}
  - {{LABEL_2}}
  - {{LABEL_3}}

Assignees:
  - {{ASSIGNEE_1}}

Milestone: {{MILESTONE_IF_ANY}}
```

### Issue/PR Body

{{FULL_ISSUE_OR_PR_BODY_CONTENT}}

### Comments (Latest 5 or All)

```markdown
## Comment 1
**Author**: {{AUTHOR}}
**Date**: {{DATE}}
**Content**:
{{COMMENT_BODY}}

---

## Comment 2
**Author**: {{AUTHOR}}
**Date**: {{DATE}}
**Content**:
{{COMMENT_BODY}}

---
(Continue for all comments or latest 5)
```

### For PRs Only

```yaml
Branch: {{SOURCE_BRANCH}} → {{TARGET_BRANCH}}
Merge Status: {{MERGEABLE/CONFLICT/DRAFT}}
Changes:
  - {{NUM_FILES_CHANGED}} files changed
  - +{{ADDITIONS}} additions
  - -{{DELETIONS}} deletions

Files Changed:
  {{FILE_PATH_1}}
  {{FILE_PATH_2}}
  {{FILE_PATH_3}}

Code Diff Summary:
  {{BRIEF_SUMMARY_OF_CHANGES}}
```

### Related Issues/Links

- Related Issue #{{ISSUE_NUMBER}}: {{TITLE}}
- Duplicate of #{{ISSUE_NUMBER}}: {{TITLE}}
- Blocks #{{ISSUE_NUMBER}}: {{TITLE}}
- Blocked by #{{ISSUE_NUMBER}}: {{TITLE}}

---

## 📋 SECTION 8: IMPLEMENTATION PLAN

### Breakdown

**Phase 1: Understanding & Setup**
- [ ] Analyze requirements from issue/PR
- [ ] Explore codebase for relevant patterns
- [ ] Identify affected files and services
- [ ] Set up worktree and verify symlinks
- [ ] Estimate effort and communicate to HOTL

**Phase 2: Test-Driven Development**
- [ ] Write failing tests for new functionality
- [ ] Confirm tests fail (RED)
- [ ] Implement minimal code to pass (GREEN)
- [ ] Refactor while keeping tests green
- [ ] Repeat for each feature/fix

**Phase 3: Integration & Verification**
- [ ] Run full test suite
- [ ] Verify code quality checks pass
- [ ] Test manually if applicable
- [ ] Update documentation
- [ ] Prepare PR (if issue) or merge (if PR)

**Phase 4: HOTL Review & Handoff**
- [ ] Prepare summary of work completed
- [ ] Identify any remaining concerns
- [ ] Request HOTL review
- [ ] Incorporate feedback
- [ ] Finalize and merge/cleanup

### Tasks

```markdown
1. [ ] {{TASK_1_DESCRIPTION}}
   - Estimated time: {{ESTIMATE}}
   - Dependencies: {{WHAT_THIS_DEPENDS_ON}}

2. [ ] {{TASK_2_DESCRIPTION}}
   - Estimated time: {{ESTIMATE}}
   - Dependencies: {{WHAT_THIS_DEPENDS_ON}}

3. [ ] {{TASK_3_DESCRIPTION}}
   - Estimated time: {{ESTIMATE}}
   - Dependencies: {{WHAT_THIS_DEPENDS_ON}}
```

---

## 📋 SECTION 9: NOTES & ARTIFACTS

### Code Snippets / References

```python
# {{DESCRIPTION_OF_SNIPPET}}
{{CODE}}
```

### External Resources

- {{RESOURCE_1_URL}} — {{DESCRIPTION}}
- {{RESOURCE_2_URL}} — {{DESCRIPTION}}

### Commands Used

```bash
# {{PURPOSE}}
{{COMMAND}}

# {{PURPOSE}}
{{COMMAND}}
```

### Debug Logs / Output

```log
{{RELEVANT_LOG_OUTPUT}}
```

---

## END OF WT-TASK.md
