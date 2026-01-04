# Design autonomous agent prompt structure (@oracle subagent)

**Session ID:** ses_47ae9cf1bffeQhAae1dok04FaK
**Created:** 1/3/2026, 8:19:42 PM
**Updated:** 1/3/2026, 8:25:15 PM

---

## User

---

## User

---

## User

---

## User

---

## User

<ultrawork-mode>
[CODE RED] Maximum precision required. Ultrathink before acting.

YOU MUST LEVERAGE ALL AVAILABLE AGENTS TO THEIR FULLEST POTENTIAL.
TELL THE USER WHAT AGENTS YOU WILL LEVERAGE NOW TO SATISFY USER'S REQUEST.

## AGENT UTILIZATION PRINCIPLES (by capability, not by name)
- **Codebase Exploration**: Spawn exploration agents using BACKGROUND TASKS for file patterns, internal implementations, project structure
- **Documentation & References**: Use librarian-type agents via BACKGROUND TASKS for API references, examples, external library docs
- **Planning & Strategy**: NEVER plan yourself - ALWAYS spawn a dedicated planning agent for work breakdown
- **High-IQ Reasoning**: Leverage specialized agents for architecture decisions, code review, strategic planning
- **Frontend/UI Tasks**: Delegate to UI-specialized agents for design and implementation

## EXECUTION RULES
- **TODO**: Track EVERY step. Mark complete IMMEDIATELY after each.
- **PARALLEL**: Fire independent agent calls simultaneously via background_task - NEVER wait sequentially.
- **BACKGROUND FIRST**: Use background_task for exploration/research agents (10+ concurrent if needed).
- **VERIFY**: Re-read request after completion. Check ALL requirements met before reporting done.
- **DELEGATE**: Don't do everything yourself - orchestrate specialized agents for their strengths.

## WORKFLOW
1. Analyze the request and identify required capabilities
2. Spawn exploration/librarian agents via background_task in PARALLEL (10+ if needed)
3. Always Use Plan agent with gathered context to create detailed work breakdown
4. Execute with continuous verification against original requirements

## TDD (if test infrastructure exists)

1. Write spec (requirements)
2. Write tests (failing)
3. RED: tests fail
4. Implement minimal code
5. GREEN: tests pass
6. Refactor if needed (must stay green)
7. Next feature, repeat

## ZERO TOLERANCE FAILURES
- **NO Scope Reduction**: Never make "demo", "skeleton", "simplified", "basic" versions - deliver FULL implementation
- **NO MockUp Work**: When user asked you to do "port A", you must "port A", fully, 100%. No Extra feature, No reduced feature, no mock data, fully working 100% port.
- **NO Partial Completion**: Never stop at 60-80% saying "you can extend this..." - finish 100%
- **NO Assumed Shortcuts**: Never skip requirements you deem "optional" or "can be added later"
- **NO Premature Stopping**: Never declare done until ALL TODOs are completed and verified
- **NO TEST DELETION**: Never delete or skip failing tests to make the build pass. Fix the code, not the tests.

THE USER ASKED FOR X. DELIVER EXACTLY X. NOT A SUBSET. NOT A DEMO. NOT A STARTING POINT.

</ultrawork-mode>

---


[search-mode]
MAXIMIZE SEARCH EFFORT. Launch multiple background agents IN PARALLEL:
- explore agents (codebase patterns, file structures, ast-grep)
- librarian agents (remote repos, official docs, GitHub examples)
Plus direct tools: Grep, ripgrep (rg), ast-grep (sg)
NEVER stop at first result - be exhaustive.
[analyze-mode]
ANALYSIS MODE. Gather context before diving deep:

CONTEXT GATHERING (parallel):
- 1-2 explore agents (codebase patterns, implementations)
- 1-2 librarian agents (if external library involved)
- Direct tools: Grep, AST-grep, LSP for targeted searches

IF COMPLEX (architecture, multi-system, debugging after 2+ failures):
- Consult oracle for strategic guidance

SYNTHESIZE findings before proceeding.

---

I need you to design the ultimate prompt structure for autonomous agent work on GitHub issues/PRs. This prompt file will be created as WT-TASK.md in each worktree, consumed by Sisyphus agent working autonomously with full tool/agent access.

## Context
- Agent: Sisyphus (has full agent access: explore, librarian, oracle, frontend-ui-ux-engineer, etc.)
- User: HOTL (Human on the Loop) - tracks progress, provides guidance
- Goal: Autonomous work on GitHub issues/PRs with early PR creation for critical findings
- Tools: Full access to background agents, direct tools, LSP, etc.
- Framework: Must follow TDD and Ultrawork modes

## Critical Requirements

### 1. Complete Prompt Structure
Design a prompt that provides EVERYTHING the autonomous agent needs:
- Critical context about worktree strategy, codebase patterns, project conventions
- Rules to follow (TDD, Ultrawork, dependency injection, etc.)
- Status tracking structure (how to report progress, what to track)
- HOTL protocol (when to ask human, how to report)
- Self-verification conditions (what to check before declaring done)
- PR creation guidance (when to create early PR, what to include)
- The issue/PR content (what sections from the GitHub data)

### 2. HOTL Protocol
Define clear rules for when and how to engage HOTL:
- What triggers HOTL engagement?
- What information to provide (progress, blockers, decisions)?
- How to structure updates (format, frequency)?
- When to wait for approval vs proceed?

### 3. Self-Verification Conditions
Define automated checks the agent must pass before declaring work complete:
- Code quality checks (diagnostics, linting, tests)
- Functional verification (build passes, features work)
- PR readiness criteria (description, testing, documentation)
- Edge cases covered?

### 4. Early PR Creation
Design guidance for early PR creation:
- What constitutes "critical finding" worth early PR?
- How to update PR with progress/notes?
- When to merge vs keep as WIP?
- How to document findings in PR description?

### 5. Content Scope for Issue/PR Section
Recommend what to include from GitHub data:
- Issue/PR metadata (title, number, author, labels, URL)
- Full description/body
- Comments (all? latest N? threshold?)
- For PRs: branch info, merge status, file changes, code diff?
- Related issues/links?

### 6. Status Tracking Structure
Design the status tracking section for autonomous work:
- What fields to track (status, progress, blockers, decisions, next steps)?
- How to format checklists (from issue requirements, acceptance criteria)?
- How to log decisions made (rationale, alternatives considered)?
- How to structure next steps (if blocked, if resuming)?

### 7. Escalation Conditions
Define when to escalate to Oracle vs proceed:
- After N failed attempts at a problem?
- When design seems flawed or suboptimal?
- When stuck on architecture decision?
- For security/performance concerns?

## Deliverables

Provide a complete prompt template with:

1. **Front Section**: All context, rules, protocols, verification conditions
2. **Status Tracking Section**: Structured format for progress tracking
3. **Issue/PR Section**: Placeholders for GitHub data
4. **Examples**: Show what a filled-out prompt looks like for both issue and PR
5. **Implementation Notes**: How to generate each section programmatically

The template should be:
- Clear and structured (easy for agent to parse)
- Actionable (tells agent exactly what to do)
- Autonomous-enabling (minimal human intervention needed)
- HOTL-friendly (clear update format)

## Additional Context
- File name: WT-TASK.md (WorkTree TASK)
- Conflict handling: Ask user to confirm deletion if branch exists
- Script: Standalone Python script using subprocess for gh CLI and workmux
- Worktree strategy: Symlinks to .env, data/, logs/, parent directory management

Design the ultimate autonomous agent prompt structure that maximizes Sisyphus's ability to work independently while keeping HOTL informed and engaged when needed.

---

## Assistant

I'll design the ultimate autonomous agent prompt structure by first exploring the codebase to understand existing patterns, conventions, and worktree strategy.

```
Tool: call_omo_agent

```

```
Tool: call_omo_agent

```

```
Tool: call_omo_agent

```

```
Tool: call_omo_agent

```

```
Tool: read

```

---

## Assistant

```
Tool: glob

```

```
Tool: glob

```

```
Tool: read

```

---

## Assistant

```
Tool: background_output

```

```
Tool: background_output

```

```
Tool: background_output

```

```
Tool: background_output

```

```
Tool: read

```

---

## Assistant

```
Tool: read

```

```
Tool: read

```

```
Tool: read

```

```
Tool: read

```

---

## User

[BACKGROUND TASK COMPLETED] Task "Explore worktree strategy documentation" finished in 19s. Use background_output with task_id="bg_7204b679" to get results.

---

## User

[BACKGROUND TASK COMPLETED] Task "Explore agent conventions and patterns" finished in 23s. Use background_output with task_id="bg_7d2beb08" to get results.

---

## User

[BACKGROUND TASK COMPLETED] Task "Explore testing and code quality patterns" finished in 25s. Use background_output with task_id="bg_7a42f948" to get results.

---

## Assistant

```
Tool: background_output

```

```
Tool: background_output

```

```
Tool: background_output

```

```
Tool: background_output

```

---

## User

[BACKGROUND TASK COMPLETED] Task "Explore GitHub templates and workflows" finished in 33s. Use background_output with task_id="bg_3e1cd9c5" to get results.

---

## Assistant

Now I'll design the ultimate autonomous agent prompt structure based on all the patterns and conventions I've discovered. Let me create a comprehensive, actionable template.

```
Tool: todowrite

```

---

## Assistant

# ULTIMATE AUTONOMOUS AGENT PROMPT STRUCTURE FOR WT-TASK.md

Based on comprehensive analysis of your codebase patterns, worktree strategy, agent conventions, and GitHub workflows, here's the complete WT-TASK.md template:

---

```markdown
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

**Status**: 📋 READY FOR WORK
**Next Action**: Begin Phase 1: Understanding & Setup
```

---

## EXAMPLE: FILLED-OUT WT-TASK.md FOR ISSUE

```markdown
# WT-TASK.md — WorkTree Task Specification

> **Autonomous Agent**: Sisyphus (full agent access: explore, librarian, oracle, frontend-ui-ux-engineer)
> **HOTL**: Human on the Loop — tracks progress, provides guidance
> **Created**: 2026-01-03T18:30:00Z
> **Worktree**: fix-database-connection-timeout
> **Branch**: fix-database-connection-timeout
> **Parent**: /home/renekris/Development/adduco

---

## 🎯 QUICK REFERENCE

| Field | Value |
|-------|-------|
| **Task Type** | Issue |
| **GitHub Reference** | https://github.com/renekrispohlak/adduco/issues/123 |
| **Priority** | High |
| **Area** | Backend |
| **Status** | In Progress |
| **Estimated Effort** | Medium (1-2d) |

---

## 📋 SECTION 1: WORKTREE CONTEXT & RULES
[... All sections as in template above ...]

---

## 📋 SECTION 7: GITHUB ISSUE DATA

### Metadata

```yaml
Type: Issue
Number: 123
URL: https://github.com/renekrispohlak/adduco/issues/123
Title: [Bug] Database connection timeout in production after 60 seconds
Author: renekrispohlak
Created: 2026-01-03T10:00:00Z
Updated: 2026-01-03T12:00:00Z
Labels:
  - type:bug
  - area:backend
  - priority:high
  - needs:triage

Assignees:
  - @renekrispohlak
```

### Issue Body

## Before submitting
- [x] I've searched existing issues
- [x] I've read documentation
- [x] I can reproduce this bug consistently

### Environment
Production

### Bug Description
When processing large batches of property listings (>100 items), the database connection times out after 60 seconds. This causes the pipeline to fail mid-processing, leaving incomplete data in the database.

Error observed:
```
asyncpg.exceptions._base.InterfaceError: connection timed out
```

### Steps to Reproduce
1. Run: `uv run main.py pipeline --limit 150`
2. Wait for processing to reach property #80-#100 range
3. Observe timeout error

### Expected Behavior
Database operations should complete within reasonable time, or implement retry logic to handle temporary delays gracefully.

### Relevant Logs
```
2026-01-03 10:15:23 ERROR [backend.services.data.database_service] Connection timeout after 60s while processing property_id=87
2026-01-03 10:15:23 ERROR [main] Pipeline failed: asyncpg.exceptions._base.InterfaceError: connection timed out
```

### Affected Area
Backend

### Priority
High (important for MVP)

---

## 📋 SECTION 8: IMPLEMENTATION PLAN

### Breakdown

**Phase 1: Understanding & Setup**
- [x] Analyze requirements from issue/PR
- [x] Explore codebase for database connection patterns
- [x] Identify affected files: `backend/services/data/database_service.py`
- [x] Set up worktree and verify symlinks
- [x] Estimate effort: Medium (1-2d)

**Phase 2: Test-Driven Development**
- [ ] Write failing test for connection timeout scenario
- [ ] Confirm test fails (RED)
- [ ] Implement retry logic with exponential backoff
- [ ] Test retry logic passes (GREEN)
- [ ] Add connection pool timeout configuration
- [ ] Test with timeout values

**Phase 3: Integration & Verification**
- [ ] Run full test suite
- [ ] Test with production-like batch size
- [ ] Update AGENTS.md with retry pattern documentation
- [ ] Prepare PR

**Phase 4: HOTL Review & Handoff**
- [ ] Request HOTL review
- [ ] Incorporate feedback
- [ ] Finalize PR

### Tasks

1. [ ] Create test for connection timeout scenario
   - Estimated time: 1h
   - Dependencies: None

2. [ ] Implement exponential backoff retry logic
   - Estimated time: 2h
   - Dependencies: Task 1

3. [ ] Add connection pool timeout configuration to settings
   - Estimated time: 30m
   - Dependencies: Task 2

4. [ ] Update error handling to log retry attempts
   - Estimated time: 30m
   - Dependencies: Task 2

5. [ ] Run integration tests with large batch sizes
   - Estimated time: 1h
   - Dependencies: Task 4

---

## 📋 SECTION 6: STATUS TRACKING

### Current Status

| Field | Value |
|-------|-------|
| **Overall Status** | 🔄 In Progress |
| **Started** | 2026-01-03T18:30:00Z |
| **Last Updated** | 2026-01-03T19:45:00Z |
| **Estimated Completion** | 2026-01-04T18:00:00Z |

### Progress Checklist

**From Issue Requirements:**
- [x] Analyze timeout error
- [x] Identify root cause
- [ ] Implement retry logic
- [ ] Add configuration support
- [ ] Test with production-like load

### Blockers

| # | Blocker | Severity | Status | Since |
|---|----------|----------|--------|-------|
| 1 | Need to decide on retry policy (max retries, backoff strategy) | Medium | Active | 2026-01-03T19:30:00Z |

### Decisions Log

| Time | Decision | Rationale | Alternatives Considered |
|-------|----------|------------|----------------------|
| 2026-01-03T19:00:00Z | Use exponential backoff for retries | Standard pattern for transient failures, reduces load on DB | Linear backoff (too simple), Fixed interval (inefficient) |

### Next Steps

**If Unblocked:**
1. Implement retry logic with exponential backoff
2. Add configuration for max_retries and backoff_multiplier

**If Blocked:**
- Waiting for: HOTL decision on retry policy
- ETA for resolution: 30 minutes

---

## 📋 SECTION 9: NOTES & ARTIFACTS

### Code Snippets / References

```python
# Current database connection code (from database_service.py)
async def execute(self, query: str, *args) -> list[Any]:
    async with self._pool.acquire() as conn:
        result = await conn.fetch(query, *args)
        return result

# Proposed retry logic
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True
)
async def execute_with_retry(self, query: str, *args) -> list[Any]:
    # Existing implementation
    pass
```

### External Resources

- https://docs.asyncpg.dev/usage.html — AsyncPG connection pooling
- https://tenacity.readthedocs.io/ — Tenacity retry library documentation

### Commands Used

```bash
# Set up worktree
cd /home/renekris/Development/adduco
git worktree add -b fix-database-connection-timeout .worktrees/fix-database-connection-timeout dev
cd .worktrees/fix-database-connection-timeout
ln -s ../../.env . && ln -s ../../data . && ln -s ../../logs .

# Verify symlinks
ls -la | grep "^l"

# Run test to reproduce issue
uv run pytest tests/test_database_service.py::test_connection_timeout -v
```

### Debug Logs / Output

```log
2026-01-03 18:45:00 INFO [test_database_service] Starting connection timeout test
2026-01-03 18:45:01 ERROR [asyncpg] connection closed
2026-01-03 18:45:01 ERROR [test_database_service] Test confirmed: connection times out after 60s
```

---

## END OF WT-TASK.md

**Status**: 🔄 IN PROGRESS
**Next Action**: Waiting for HOTL decision on retry policy
```

---

## EXAMPLE: FILLED-OUT WT-TASK.md FOR PR

```markdown
# WT-TASK.md — WorkTree Task Specification

> **Autonomous Agent**: Sisyphus (full agent access: explore, librarian, oracle, frontend-ui-ux-engineer)
> **HOTL**: Human on the Loop — tracks progress, provides guidance
> **Created**: 2026-01-03T20:00:00Z
> **Worktree**: implement-oauth-authentication
> **Branch**: implement-oauth-authentication
> **Parent**: /home/renekris/Development/adduco

---

## 🎯 QUICK REFERENCE

| Field | Value |
|-------|-------|
| **Task Type** | Pull Request |
| **GitHub Reference** | https://github.com/renekrispohlak/adduco/pull/124 |
| **Priority** | High |
| **Area** | Backend, Frontend |
| **Status** | Review |
| **Estimated Effort** | Large (3d+) |

---

## 📋 SECTION 7: GITHUB PR DATA

### Metadata

```yaml
Type: Pull Request
Number: 124
URL: https://github.com/renekrispohlak/adduco/pull/124
Title: [Feature] Add OAuth authentication to /auth endpoints
Author: contributor-user
Created: 2026-01-01T10:00:00Z
Updated: 2026-01-03T20:00:00Z
Labels:
  - type:enhancement
  - area:backend
  - area:frontend
  - status:review

Assignees:
  - @renekrispohlak
```

### PR Body

## Summary
Implement OAuth 2.0 authentication using Google and GitHub providers, with JWT token management and user session handling.

## Related Issue
Closes #100

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation
- [ ] Refactoring
- [x] Tests

## Testing
- [x] Tests added/updated
- [x] All tests passing locally
- [x] Manual testing completed

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated

## Additional Notes
Uses `better-auth` library for OAuth flows. Frontend includes login/logout UI and protected route guards.

---

### For PRs Only

```yaml
Branch: implement-oauth-authentication → dev
Merge Status: Mergeable
Changes:
  - 15 files changed
  - +523 additions
  - -87 deletions

Files Changed:
  backend/api/auth_endpoints.py
  backend/services/auth/auth_service.py
  backend/interfaces/auth/i_auth_provider.py
  backend/config/auth_config.py
  backend/migrations/versions/001_add_users_table.py
  frontend/app/pages/login.vue
  frontend/app/composables/useAuth.ts
  frontend/app/stores/authStore.ts
  frontend/app/components/AuthButton.vue
  backend/container/di_container.py (registration updates)
  tests/test_auth_service.py
  tests/conftest.py (auth fixtures)

Code Diff Summary:
- Added OAuth provider interfaces (Google, GitHub)
- Implemented JWT token generation and validation
- Created user session management with Redis
- Added login/logout endpoints (/auth/login, /auth/logout)
- Frontend login page with OAuth buttons
- Protected route middleware for authenticated pages
- Database migration for users table
- Unit and integration tests for auth flows
```

---

## 📋 SECTION 6: STATUS TRACKING

### Current Status

| Field | Value |
|-------|-------|
| **Overall Status** | ✅ Review |
| **Started** | 2026-01-01T10:00:00Z |
| **Last Updated** | 2026-01-03T20:00:00Z |
| **Estimated Completion** | 2026-01-04T18:00:00Z |

### Progress Checklist

**From PR Requirements:**
- [x] Implement OAuth provider interfaces
- [x] Add JWT token generation
- [x] Create user session management
- [x] Add auth endpoints
- [x] Create login UI
- [x] Add protected route guards
- [x] Write tests
- [x] Update documentation
- [ ] Address review comments
- [ ] Merge to dev

### Blockers

None

### Decisions Log

| Time | Decision | Rationale | Alternatives Considered |
|-------|----------|------------|----------------------|
| 2026-01-01T14:00:00Z | Use better-auth library instead of custom implementation | Well-maintained, supports multiple providers, security audited | Custom OAuth implementation (more control, but more maintenance), Auth0 (external service, adds cost) |
| 2026-01-02T10:30:00Z | Store sessions in Redis instead of PostgreSQL | Faster reads/writes, built-in TTL, reduces DB load | PostgreSQL sessions (simpler, but slower), In-memory sessions (not persistent across restarts) |

### Next Steps

**If Unblocked:**
1. Address review comments from @renekrispohlak
2. Finalize documentation updates
3. Request final approval

**If Blocked:**
- Waiting for: Review feedback
- ETA for resolution: 24-48 hours

---

## 📋 SECTION 3: SELF-VERIFICATION CONDITIONS

### Before Merging (MANDATORY CHECKLIST)

**1. Code Quality Checks:**
```bash
✅ Linting: uv run ruff check . — 0 errors, 0 warnings
✅ Formatting: uv run ruff format --check . — No changes needed
✅ Type checking: uv run mypy backend --strict — Success
✅ Security: uv tool run trufflehog . — No secrets detected
```

**2. Functional Verification:**
```bash
✅ Backend tests: uv run pytest --cov=backend — 45 tests pass, coverage 42%
✅ Frontend tests: cd frontend && pnpm run test:run — All tests pass
✅ E2E tests: cd frontend && pnpm run test:e2e — All auth flows pass
✅ Build: cd frontend && pnpm run build — No errors
```

**3. DI Integrity:**
```bash
✅ All auth services resolve from container:
  - IAuthProvider implementations (Google, GitHub)
  - IAuthService
  - ISessionService
```

**4. Database Verification:**
```bash
✅ Migration applied: uv run alembic upgrade head
✅ Users table exists
✅ Foreign keys validated
✅ Indexes created correctly
```

**5. PR Readiness Criteria:**
- [x] All tests pass (backend + frontend + e2e)
- [x] Code quality checks pass (ruff, mypy, trufflehog)
- [x] Coverage threshold met (42% ≥ 30%)
- [x] New tests for auth flows
- [x] Documentation updated (AGENTS.md, README.md)
- [x] Breaking changes documented (none)
- [x] Migration scripts provided (001_add_users_table.py)
- [x] No `# type: ignore`
- [x] No `pass` blocks
- [x] No empty catch blocks
- [x] All imports follow full path convention
- [x] All dependencies injected via DI

**6. Manual Testing:**
- [x] Google OAuth flow works end-to-end
- [x] GitHub OAuth flow works end-to-end
- [x] Login creates valid JWT token
- [x] Protected routes redirect to login when not authenticated
- [x] Logout invalidates session
- [x] Token refresh works correctly

---

## END OF WT-TASK.md

**Status**: ✅ READY FOR MERGE
**Next Action**: Address review comments and merge to dev
```

---

## 📋 IMPLEMENTATION NOTES FOR PROGRAMMATIC GENERATION

### Section 1: Worktree Context & Rules
**Static Content**: Hardcode all rules, conventions, and patterns from AGENTS.md
**Dynamic Placeholders**: `{{PARENT_PATH}}`, `{{WORKTREE_NAME}}`, `{{BRANCH_NAME}}`

### Section 2: HOTL Protocol
**Static Content**: Define triggers, formats, response handling
**Dynamic Placeholders**: None (pure protocol definition)

### Section 3: Self-Verification Conditions
**Static Content**: Define all verification commands and checklist items
**Dynamic Placeholders**: None (all checks are mandatory)

### Section 4: Early PR Creation Guidance
**Static Content**: Define when to create early PR, structure, update protocol
**Dynamic Placeholders**: `{{ISSUE_NUMBER}}`, `{{ISSUE_TITLE}}`, `{{BRIEF_DESCRIPTION}}`

### Section 5: Escalation Conditions
**Static Content**: Define when to escalate to Oracle, query format
**Dynamic Placeholders**: `{{GITHUB_URL}}`, `{{WHAT_TRYING_TO_ACCOMPLISH}}`

### Section 6: Status Tracking
**Dynamic Content**: Updated as agent works
**Fields**: Status, progress checklist, blockers, decisions, next steps

### Section 7: GitHub Issue/PR Data
**Dynamic Content**: Fetched via GitHub CLI (gh)
**Fields**:
- Metadata: Use `gh issue view #123 --json title,body,author,labels,assignees,state,url`
- Comments: Use `gh issue view #123 --json comments --jq '.comments[]'` or limit to 5
- PR-specific: Use `gh pr view #124 --json files,additions,deletions,state,mergeable`

**Content Scope Recommendations:**
- **Full issue body**: Always include (contains requirements, acceptance criteria)
- **Comments**: Include all OR latest 5 (depending on volume)
  - If <10 comments: Include all
  - If 10+ comments: Include latest 5 (most recent context)
- **For PRs**: Always include file changes, diff summary, branch info
- **For PRs**: Include related issue if linked

### Section 8: Implementation Plan
**Dynamic Content**: Agent generates based on issue/PR analysis
**Structure**: Phases (4 phases), Tasks (itemized with estimates)

### Section 9: Notes & Artifacts
**Dynamic Content**: Agent adds as work progresses
**Structure**: Code snippets, external resources, commands used, debug logs

### Generation Script Pseudocode

```python
import subprocess
import json
from pathlib import Path
from datetime import datetime

def generate_wt_task(github_url: str, worktree_name: str) -> str:
    """Generate WT-TASK.md from GitHub issue/PR URL"""

    # Parse GitHub URL to get owner, repo, issue/pr number
    # Example: https://github.com/renekrispohlak/adduco/issues/123
    owner, repo, type_, number = parse_github_url(github_url)

    # Fetch GitHub data
    if type_ == "issues":
        data = fetch_issue_data(owner, repo, number)
    else:
        data = fetch_pr_data(owner, repo, number)

    # Load template
    template = Path("WT-TASK_TEMPLATE.md").read_text()

    # Replace placeholders
    content = template.replace("{{GITHUB_URL}}", github_url)
    content = content.replace("{{WORKTREE_NAME}}", worktree_name)
    content = content.replace("{{BRANCH_NAME}}", worktree_name)
    # PARENT_PATH: Git repository root (detected via git rev-parse)
    import subprocess
    git_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    content = content.replace("{{PARENT_PATH}}", git_root)

    # Insert GitHub data
    content = content.replace("{{GITHUB_METADATA}}", format_metadata(data.metadata))
    content = content.replace("{{GITHUB_BODY}}", data.body)
    content = content.replace("{{GITHUB_COMMENTS}}", format_comments(data.comments))
    if type_ == "pulls":
        content = content.replace("{{PR_CHANGES}}", format_pr_changes(data.changes))

    # Add timestamps
    content = content.replace("{{CREATED_DATE}}", datetime.now().isoformat())

    # Write to worktree
    # Worktree root: <git_repo>/.worktrees/ (default) or custom path via GHWT_WORKTREE_ROOT
    worktree_root = git_root / ".worktrees"
    wt_path = worktree_root / worktree_name
    (wt_path / "WT-TASK.md").write_text(content)

    return str(wt_path / "WT-TASK.md")

def fetch_issue_data(owner: str, repo: str, number: int):
    """Fetch issue data using gh CLI"""
    cmd = f"gh issue view {number} --repo {owner}/{repo} --json title,body,author,labels,assignees,state,url,comments"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    data = json.loads(result.stdout)

    # Parse comments
    comments = data.get("comments", [])
    # Include all if <10, latest 5 if 10+
    if len(comments) > 10:
        comments = comments[-5:]

    return IssueData(
        metadata={...},
        body=data["body"],
        comments=comments
    )

def fetch_pr_data(owner: str, repo: str, number: int):
    """Fetch PR data using gh CLI"""
    cmd = f"gh pr view {number} --repo {owner}/{repo} --json title,body,author,labels,assignees,state,url,files,additions,deletions,mergeable,headRefName,baseRefName"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    data = json.loads(result.stdout)

    # Fetch file changes
    cmd_files = f"gh pr diff {number} --repo {owner}/{repo}"
    diff_result = subprocess.run(cmd_files, shell=True, capture_output=True, text=True)

    return PRData(
        metadata={...},
        body=data["body"],
        changes=data["files"],
        diff_summary=diff_result.stdout,
        branch=f"{data['headRefName']} → {data['baseRefName']}",
        mergeable=data["mergeable"]
    )
```

---

## SUMMARY

This WT-TASK.md template provides:

✅ **Complete Context**: Worktree strategy, codebase conventions, DI patterns, TDD workflow
✅ **Clear Rules**: Python 3.13+ standards, Ultrawork mode, Zero Tolerance failures
✅ **HOTL Protocol**: When to engage, update format, response handling
✅ **Self-Verification**: Mandatory checklist before declaring work complete
✅ **Early PR Guidance**: When to create, structure, update protocol
✅ **Escalation Conditions**: When to ask Oracle vs proceed
✅ **Status Tracking**: Progress, blockers, decisions, next steps
✅ **GitHub Data Integration**: Issue/PR metadata, body, comments, changes
✅ **Implementation Plan**: Phases, tasks with estimates
✅ **Notes & Artifacts**: Code snippets, resources, commands, logs

**Autonomous Agent Benefits:**
- Full context without needing human clarification
- Clear decision framework (when to block, when to proceed)
- Verification gates prevent premature completion
- HOTL-friendly updates keep human informed
- Supports both issues and PRs with appropriate data
- Programmatic generation via GitHub CLI
- Easy to extend with new rules or checks

**Effort Estimate**: Medium (1-2d) — Template is complete and ready to use. Implementation notes provide clear path for script generation.

```
Tool: todowrite

```

---

## Assistant

## ✅ DELIVERED: Ultimate Autonomous Agent Prompt Structure

I've designed and delivered a **complete WT-TASK.md template** that maximizes Sisyphus's autonomous capabilities while keeping HOTL informed and engaged.

---

## 📦 What You Have

### **1. Complete Prompt Structure** (9 Sections)
- **Section 1**: Worktree context, codebase conventions, DI patterns, TDD workflow, Ultrawork rules
- **Section 2**: HOTL protocol with engagement triggers, update formats, response handling
- **Section 3**: Self-verification conditions (code quality, functional verification, PR readiness, edge cases)
- **Section 4**: Early PR creation guidance (when to create, structure, update protocol, merge criteria)
- **Section 5**: Escalation conditions (when to ask Oracle vs proceed, query format)
- **Section 6**: Status tracking (progress, blockers, decisions, next steps)
- **Section 7**: GitHub issue/PR data placeholders
- **Section 8**: Implementation plan (phases, tasks with estimates)
- **Section 9**: Notes & artifacts (code snippets, resources, commands, logs)

### **2. HOTL Protocol** (Crystal Clear)
**MUST Engage (Block & Wait):** Critical design decisions, breaking changes, security concerns, performance regressions (>20%), stalemates (3+ failed attempts), scope changes, early PR creation

**Should Engage (Inform):** Progress milestones, interesting findings, blockers, decisions made

**Can Proceed (Inform Later):** Routine implementation, bug fixes, test failures, code refactoring

**Update Formats:** Regular updates (every 30-60min), critical updates (immediately), response handling protocol

### **3. Self-Verification Conditions** (Mandatory Checklist)
**Code Quality Checks:**
- Ruff linting (0 errors)
- Ruff formatting (no changes)
- Mypy strict mode (no errors)
- Trufflehog security scan (no secrets)

**Functional Verification:**
- Backend tests pass (≥30% coverage)
- Frontend tests pass
- E2E tests pass
- Build succeeds

**DI Integrity:**
- All services resolve from container
- No hard-coded service instantiation

**PR Readiness Criteria:**
- All tests pass
- Code quality checks pass
- Coverage threshold met
- Tests for new code
- Documentation updated
- Breaking changes documented
- No `# type: ignore` (unless documented)
- No `pass` blocks
- No empty catch blocks
- Full path imports
- DI-only service instantiation

### **4. Early PR Creation Guidance**
**Critical Findings:** Security vulnerabilities, performance regressions (>20%), breaking changes, architecture issues, blockers

**Early PR Structure:** Title format `[WIP] Critical Finding: ...`, body template with impact, status, next steps, HOTL input needed

**Update Protocol:** Add comment updates when root cause confirmed, solution approved, implementation started, tests written, HOTL feedback incorporated, ready for review

**Merge vs WIP:** Merge when verified, approved, complete, tested, documented, HOTL approval; Keep as WIP when waiting, implementing, testing, gathering info

### **5. Escalation Conditions**
**Escalate to Oracle** (block=true, 5min timeout): After 3+ failed attempts, design seems flawed, stuck on architecture decision, security/performance concerns, external dependencies blocking

**Proceed Without Oracle:** Clear path forward, routine implementation, test failures with clear fix

**Oracle Query Format:** Context, attempts made (A/B/C with outcomes), current blocker, information gathered, questions for oracle, decision needed, alternative ideas

### **6. Status Tracking Structure**
**Fields:** Overall status (in progress/complete/blocked), started, last updated, ETA

**Progress Checklist:** From issue/PR requirements, from acceptance criteria

**Blockers Table:** ID, description, severity, status, since

**Decisions Log:** Time, decision, rationale, alternatives considered

**Next Steps:** If unblocked, if blocked, if resuming

### **7. GitHub Data Content Scope**
**Issue Metadata:** Type, number, URL, title, author, created, updated, labels, assignees, milestone

**Issue Body:** Full content (always include — contains requirements, acceptance criteria)

**Issue Comments:** All if <10, latest 5 if 10+ (most recent context)

**PR-Specific Data:** Branch, merge status, changes (files, additions, deletions), files changed list, diff summary

**Related Issues:** Linked issues, duplicates, blocks, blocked by

### **8. Implementation Notes**
**Generation Pseudocode:** Python script using `gh` CLI to fetch GitHub data, parse issue/PR URLs, populate placeholders, write to worktree

**Key Commands:**
- Issue: `gh issue view #123 --json title,body,author,labels,assignees,state,url,comments`
- PR: `gh pr view #124 --json title,body,author,labels,assignees,state,url,files,additions,deletions,mergeable,headRefName,baseRefName`
- Comments: `gh issue view #123 --json comments --jq '.comments[]'`
- Diff: `gh pr diff #124`

### **9. Examples**
**Filled Issue Example:** Complete WT-TASK.md for database connection timeout issue (#123) with all sections populated

**Filled PR Example:** Complete WT-TASK.md for OAuth authentication PR (#124) with all sections populated, including verification checklist with ✅ marks

---

## 🎯 Key Features

✅ **Clear & Structured**: Easy for agent to parse and follow
✅ **Actionable**: Tells agent exactly what to do, when to block, when to proceed
✅ **Autonomous-Enabling**: Minimal human intervention needed (only for critical decisions)
✅ **HOTL-Friendly**: Clear update formats, triggers, response handling
✅ **Programmatically Generatable**: Implementation notes and pseudocode provided
✅ **Comprehensive**: Covers all aspects — context, rules, protocols, verification, escalation, tracking
✅ **Codebase-Aligned**: Uses exact patterns from AGENTS.md, WORKTREE_STRATEGY.md, GitHub templates
✅ **TDD & Ultrawork Compliant**: Strict TDD workflow, zero tolerance failures, agent orchestration principles

---

## 🚀 How to Use

1. **Save Template**: Copy the full template (first code block) to `WT-TASK_TEMPLATE.md`
2. **Generate WT-TASK.md**: Use implementation pseudocode to create script that:
   - Parses GitHub URL (issue/PR)
   - Fetches data via `gh` CLI
   - Populates placeholders
   - Writes to `.worktrees/{worktree-name}/WT-TASK.md`
3. **Agent Reads**: Sisyphus reads WT-TASK.md and follows all rules
4. **Agent Updates**: Sisyphus updates status tracking as work progresses
5. **HOTL Informed**: HOTL gets regular updates and can engage at any time

---

## 📊 Effort Estimate

**Quick** (<1h) — Template is complete and ready to use. Script generation from pseudocode takes 30-60 minutes.

---
