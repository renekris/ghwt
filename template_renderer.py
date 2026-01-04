"""Template renderer for WT-TASK.md generation."""

from pathlib import Path

import structlog
from models import IssueData, PRData


class TemplateRenderer:
    """Render WT-TASK.md template with GitHub issue/PR data."""

    def __init__(self, template_path: Path) -> None:
        """Initialize template renderer.

        Args:
            template_path: Path to WT-TASK.md template file
        """
        self.logger: structlog.typing.FilteringBoundLogger = structlog.get_logger(__name__)
        self.template_path: Path = template_path

    def render_for_issue(
        self,
        issue_data: IssueData,
        parent_path: str | Path | None = None,
        worktree_name: str | None = None,
        branch_name: str | None = None,
    ) -> str:
        """Render template for GitHub issue.

        Args:
            issue_data: Issue data from GitHub
            parent_path: Parent directory path (for worktree context)
            worktree_name: Worktree directory name
            branch_name: Branch name

        Returns:
            Rendered template string
        """
        self.logger.info(
            "Rendering template for issue",
            number=issue_data.number,
            title=issue_data.title[:50],
        )

        template = self._load_template()
        replacements = self._build_issue_replacements(issue_data, parent_path, worktree_name, branch_name)
        result = self._apply_replacements(template, replacements)

        self.logger.debug(
            "Template rendered successfully",
            number=issue_data.number,
            result_length=len(result),
        )

        return result

    def render_for_pr(
        self,
        pr_data: PRData,
        parent_path: str | Path | None = None,
        worktree_name: str | None = None,
        branch_name: str | None = None,
    ) -> str:
        """Render template for GitHub PR.

        Args:
            pr_data: PR data from GitHub
            parent_path: Parent directory path (for worktree context)
            worktree_name: Worktree directory name
            branch_name: Branch name

        Returns:
            Rendered template string
        """
        self.logger.info(
            "Rendering template for PR",
            number=pr_data.number,
            title=pr_data.title[:50],
        )

        template = self._load_template()
        replacements = self._build_pr_replacements(pr_data, parent_path, worktree_name, branch_name)
        result = self._apply_replacements(template, replacements)

        self.logger.debug(
            "Template rendered successfully",
            number=pr_data.number,
            result_length=len(result),
        )

        return result

    def _load_template(self) -> str:
        """Load template from file.

        Returns:
            Template content as string

        Raises:
            RuntimeError: If template file not found or cannot be read
        """
        self.logger.debug("Loading template", path=str(self.template_path))

        if not self.template_path.exists():
            self.logger.error("Template file not found", path=str(self.template_path))
            raise RuntimeError(f"Template file not found: {self.template_path}")

        try:
            template = self.template_path.read_text()
            self.logger.debug("Template loaded successfully", template_length=len(template))
            return template
        except OSError as e:
            self.logger.error("Failed to read template file", path=str(self.template_path), error=str(e))
            raise RuntimeError(f"Failed to read template file: {self.template_path}") from e

    def _build_issue_replacements(
        self,
        issue_data: IssueData,
        parent_path: str | Path | None = None,
        worktree_name: str | None = None,
        branch_name: str | None = None,
    ) -> dict[str, str]:
        """Build placeholder replacements for issue.

        Args:
            issue_data: Issue data from GitHub
            parent_path: Parent directory path (for worktree context)
            worktree_name: Worktree directory name
            branch_name: Branch name

        Returns:
            Dictionary mapping placeholders to values
        """
        from datetime import datetime

        # Build comments section
        comments_text = ""
        if issue_data.comments:
            comments_text = "\n".join(
                [
                    f"### Comment by {comment.author} on {comment.created_at}\n{comment.body}\n"
                    for comment in issue_data.comments
                ]
            )

        return {
            "{{ISSUE_OR_PR}}": "Issue",
            "{{ISSUE_OR_PR_NUMBER}}": str(issue_data.number),
            "{{ISSUE_NUMBER}}": str(issue_data.number),
            "{{TITLE}}": issue_data.title,
            "{{AUTHOR}}": issue_data.author,
            "{{GITHUB_URL}}": issue_data.url,
            "{{FULL_ISSUE_OR_PR_BODY_CONTENT}}": issue_data.body or "No description provided.",
            "{{GITHUB_COMMENTS}}": comments_text,
            "{{PARENT_PATH}}": str(parent_path) if parent_path else "PARENT_PATH_PLACEHOLDER",
            "{{WORKTREE_NAME}}": worktree_name or "WORKTREE_NAME_PLACEHOLDER",
            "{{BRANCH_NAME}}": branch_name or "BRANCH_NAME_PLACEHOLDER",
            "{{CREATED_DATE}}": datetime.now().strftime("%Y-%m-%d"),
        }

    def _build_pr_replacements(
        self,
        pr_data: PRData,
        parent_path: str | Path | None = None,
        worktree_name: str | None = None,
        branch_name: str | None = None,
    ) -> dict[str, str]:
        """Build placeholder replacements for PR.

        Args:
            pr_data: PR data from GitHub
            parent_path: Parent directory path (for worktree context)
            worktree_name: Worktree directory name
            branch_name: Branch name

        Returns:
            Dictionary mapping placeholders to values
        """
        from datetime import datetime

        # Build comments section
        comments_text = ""
        if pr_data.comments:
            comments_text = "\n".join(
                [
                    f"### Comment by {comment.author} on {comment.created_at}\n{comment.body}\n"
                    for comment in pr_data.comments
                ]
            )

        return {
            "{{ISSUE_OR_PR}}": "Pull Request",
            "{{ISSUE_OR_PR_NUMBER}}": str(pr_data.number),
            "{{ISSUE_NUMBER}}": str(pr_data.number),
            "{{TITLE}}": pr_data.title,
            "{{AUTHOR}}": pr_data.author,
            "{{GITHUB_URL}}": pr_data.url,
            "{{FULL_ISSUE_OR_PR_BODY_CONTENT}}": pr_data.body or "No description provided.",
            "{{GITHUB_COMMENTS}}": comments_text,
            "{{PARENT_PATH}}": str(parent_path) if parent_path else "PARENT_PATH_PLACEHOLDER",
            "{{WORKTREE_NAME}}": worktree_name or "WORKTREE_NAME_PLACEHOLDER",
            "{{BRANCH_NAME}}": branch_name or "BRANCH_NAME_PLACEHOLDER",
            "{{CREATED_DATE}}": datetime.now().strftime("%Y-%m-%d"),
        }

    def _apply_replacements(self, template: str, replacements: dict[str, str]) -> str:
        """Apply placeholder replacements to template.

        Args:
            template: Template string with placeholders
            replacements: Dictionary mapping placeholders to values

        Returns:
            Rendered template string
        """
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        return result
