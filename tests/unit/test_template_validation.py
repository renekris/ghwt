"""Test template rendering and WT-TASK.md generation."""

from pathlib import Path

from models import CommentData, FileChange, IssueData, PRData
from template_renderer import TemplateRenderer


def test_template_has_all_required_sections() -> None:
    """Verify template contains all 9 required sections."""
    template_path = Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md"
    template = template_path.read_text()

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
        assert section in template, f"Missing section: {section}"


def test_template_has_all_placeholders() -> None:
    """Verify template contains all required placeholders."""
    template_path = Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md"
    template = template_path.read_text()

    required_placeholders = [
        "{{PARENT_PATH}}",
        "{{WORKTREE_NAME}}",
        "{{BRANCH_NAME}}",
        "{{CREATED_DATE}}",
        "{{ISSUE_OR_PR}}",
        "{{ISSUE_OR_PR_NUMBER}}",
        "{{ISSUE_NUMBER}}",
        "{{TITLE}}",
        "{{AUTHOR}}",
        "{{FULL_ISSUE_OR_PR_BODY_CONTENT}}",
        "{{GITHUB_URL}}",
    ]

    for placeholder in required_placeholders:
        assert placeholder in template, f"Missing placeholder: {placeholder}"


def test_render_for_issue_replaces_all_placeholders() -> None:
    """Verify issue rendering replaces all placeholders with actual data."""
    renderer = TemplateRenderer(Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md")

    issue_data = IssueData(
        title="Test Issue",
        body="Test body",
        number=123,
        author="testuser",
        labels=["bug", "backend"],
        state="open",
        url="https://github.com/owner/repo/issues/123",
        comments=[
            CommentData(author="commenter1", body="Comment 1", created_at="2026-01-03T10:00:00Z"),
        ],
    )

    rendered = renderer.render_for_issue(
        issue_data=issue_data,
        parent_path="/home/renekris/Development/adduco",
        worktree_name="issue-123-test-issue",
        branch_name="issue-123-test-issue",
    )

    assert "{{TITLE}}" not in rendered
    assert "{{AUTHOR}}" not in rendered
    assert "{{ISSUE_NUMBER}}" not in rendered
    assert "{{FULL_ISSUE_OR_PR_BODY_CONTENT}}" not in rendered
    assert "Test Issue" in rendered
    assert "testuser" in rendered
    assert "123" in rendered
    assert "Test body" in rendered
    assert "/home/renekris/Development/adduco" in rendered


def test_render_for_pr_includes_pr_specific_fields() -> None:
    """Verify PR rendering includes PR-specific data."""
    renderer = TemplateRenderer(Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md")

    pr_data = PRData(
        title="Test PR",
        body="Test PR body",
        number=124,
        author="testuser",
        labels=["enhancement"],
        state="open",
        url="https://github.com/owner/repo/pull/124",
        comments=[],
        head_branch="feature/test",
        base_branch="dev",
        mergeable=True,
        additions=100,
        deletions=50,
        files_changed=[FileChange(path="backend/test.py")],
    )

    rendered = renderer.render_for_pr(
        pr_data=pr_data,
        parent_path="/home/renekris/Development/adduco",
        worktree_name="pr-124-test-pr",
        branch_name="pr-124-test-pr",
    )

    assert "Pull Request" in rendered


def test_render_preserves_all_static_sections() -> None:
    """Verify rendering preserves all static sections unchanged."""
    renderer = TemplateRenderer(Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md")

    issue_data = IssueData(
        title="Test",
        body="Body",
        number=1,
        author="user",
        labels=[],
        state="open",
        url="https://github.com/owner/repo/issues/1",
        comments=[],
    )

    rendered = renderer.render_for_issue(
        issue_data=issue_data,
        parent_path="/tmp/test",
        worktree_name="test",
        branch_name="test",
    )

    # Verify static sections are present
    assert "SECTION 1: WORKTREE CONTEXT & RULES" in rendered
    assert "SECTION 2: HOTL (Human on the Loop) PROTOCOL" in rendered
    assert "SECTION 3: SELF-VERIFICATION CONDITIONS" in rendered
    assert "SECTION 4: EARLY PR CREATION GUIDANCE" in rendered
    assert "SECTION 5: ESCALATION CONDITIONS" in rendered


def test_template_contains_python_13_standards() -> None:
    """Verify template includes Python 3.13+ type syntax."""
    template_path = Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md"
    template = template_path.read_text()

    assert "str | None" in template
    assert "list[str]" in template
    assert "dict[str, int]" in template
    assert "set[str]" in template


def test_template_contains_di_patterns() -> None:
    """Verify template includes dependency injection patterns."""
    template_path = Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md"
    template = template_path.read_text()

    assert "constructor injection" in template.lower()
    assert "interface" in template.lower()
    assert "container" in template.lower()
    assert "resolve" in template.lower()


def test_template_contains_hotl_protocol() -> None:
    """Verify template includes HOTL protocol."""
    template_path = Path(__file__).parent.parent.parent / "WT_TASK_TEMPLATE.md"
    template = template_path.read_text()

    assert "When to Engage HOTL" in template
    assert "MUST Engage" in template
    assert "Should Engage" in template
    assert "Can Proceed" in template
    assert "HOTL Update Format" in template
