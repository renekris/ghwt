"""Worktree creation and management."""

import contextlib
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import structlog
from config import WorktreeSettings, PROMPT_PRESETS
from github_fetcher import GitHubIssueFetcher
from models import IssueData, PRData
from template_renderer import TemplateRenderer

ERROR_WORKMUX_NOT_INSTALLED = (
    "workmux is not installed. Install from https://github.com/yourusername/workmux"
)
ERROR_FAILED_TO_CREATE_WORKTREE = "Failed to create worktree: {error}"
ERROR_FAILED_TO_WRITE_TASK_FILE = "Failed to write WT-TASK.md to {path}"
ERROR_USER_CANCELLED_BRANCH_CONFLICT = (
    "User cancelled. Branch '{branch}' already exists."
)

# Regex patterns
GITHUB_URL_PATTERN = r"github\.com/([^/]+)/([^/]+)/(issues|pull)/(\d+)"
WORKMUX_CREATED_PATTERN = r"Created worktree at (.+)"
BRANCH_NAME_PATTERN = r"[^a-z0-9]+"


class WorktreeCreator:
    """Create worktrees from GitHub issues/PRs with autonomous agent tracking."""

    def __init__(
        self,
        issue_fetcher: GitHubIssueFetcher,
        template_renderer: TemplateRenderer,
        settings: WorktreeSettings,
        dry_run: bool = False,
    ) -> None:
        """Initialize worktree creator.

        Args:
            issue_fetcher: GitHub issue/PR data fetcher
            template_renderer: WT-TASK.md template renderer
            settings: Configuration settings
            dry_run: If True, skip workmux and only generate WT-TASK.md
        """
        self.logger: structlog.typing.FilteringBoundLogger = structlog.get_logger(
            __name__
        )
        self.issue_fetcher: GitHubIssueFetcher = issue_fetcher
        self.template_renderer: TemplateRenderer = template_renderer
        self.settings: WorktreeSettings = settings
        self._dry_run: bool = dry_run

        # Use effective worktree root from settings
        self._worktree_root = self.settings.get_effective_worktree_root()

    def create_from_github_url(
        self,
        url_or_number: str,
        item_type: str | None = None,
    ) -> Path:
        """Create worktree from GitHub issue or PR URL.

        Args:
            url_or_number: GitHub issue/PR URL or bare issue/PR number
            item_type: Explicit type ("issue" or "pr") for bare numbers

        Returns:
            Path to created worktree

        Raises:
            ValueError: If URL is invalid
            RuntimeError: If worktree creation fails
        """
        self.logger.info(
            "Creating worktree from GitHub URL",
            url_or_number=url_or_number[:100],
            item_type=item_type,
        )

        # Parse URL to extract owner, repo, number, type
        item_type, owner, repo, number = self._parse_github_url(
            url_or_number, item_type
        )

        self.logger.debug(
            "Parsed GitHub URL",
            owner=owner,
            repo=repo,
            number=number,
            item_type=item_type,
        )

        # Fetch data from GitHub
        if item_type == "issue":
            data = self.issue_fetcher.fetch_issue(owner, repo, number)
        else:
            data = self.issue_fetcher.fetch_pr(owner, repo, number)

        # Generate branch name
        branch_name = self._generate_branch_name(data)

        self.logger.debug("Generated branch name", branch_name=branch_name)

        # Check for existing branch (skip in dry-run mode)
        if not self._dry_run:
            self._check_branch_conflict(branch_name)

        # Create worktree
        worktree_path = self._create_worktree(branch_name)

        # Generate and write WT-TASK.md
        self._write_task_file(worktree_path, data)

        # Auto-open shuvcode
        self._open_shuvcode(worktree_path)

        self.logger.info("Worktree created successfully", path=str(worktree_path))

        return worktree_path

    def _detect_git_remote(self) -> tuple[str, str]:
        """Detect GitHub owner/repo from current git remote.

        Returns:
            Tuple of (owner, repo) from git remote

        Raises:
            RuntimeError: If not in a git repo or no GitHub remote found
        """
        self.logger.debug("Detecting git remote")

        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.logger.debug("Git remote command output", stdout=result.stdout[:500])

            for line in result.stdout.splitlines():
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) < 2:
                    continue

                remote_url = parts[1]

                if "github.com" not in remote_url:
                    continue

                parsed = urlparse(remote_url)

                if parsed.scheme in ("https", "http", "ssh"):
                    repo_path = parsed.path.lstrip("/").rstrip(".git")
                else:
                    repo_path = remote_url.split(":")[-1].rstrip(".git")

                if "/" not in repo_path:
                    continue

                owner, repo = repo_path.split("/")

                self.logger.debug(
                    "Detected GitHub remote",
                    owner=owner,
                    repo=repo,
                    remote_url=remote_url[:100],
                )

                return owner, repo

            self.logger.warning("No GitHub remote found in git repository")

            raise RuntimeError(
                "No GitHub remote found. Please provide full URL or ensure you're in a repository with a GitHub remote."
            )

        except FileNotFoundError:
            self.logger.error("Git command not found")
            raise RuntimeError("Git is not installed or not in PATH") from None
        except subprocess.TimeoutExpired as e:
            self.logger.error("Timeout detecting git remote")
            raise RuntimeError("Timeout detecting git remote") from e

    def _parse_github_url(
        self,
        url_or_number: str,
        item_type: str | None = None,
    ) -> tuple[str, str, str, int]:
        """Parse GitHub URL to extract components.

        Args:
            url_or_number: GitHub URL or bare number
            item_type: Explicit type ("issue" or "pr") for bare numbers

        Returns:
            Tuple of (type, owner, repo, number)

        Raises:
            ValueError: If URL is invalid
        """
        # Check if it's a bare number
        if url_or_number.isdigit():
            self.logger.debug(
                "Detected bare number, using git remote detection",
                number=url_or_number,
                item_type=item_type,
            )

            if item_type is None:
                self.logger.error("Bare number requires --issue or --pr flag")
                raise ValueError("Bare number requires --issue or --pr flag")

            owner, repo = self._detect_git_remote()
            return item_type, owner, repo, int(url_or_number)

        # Parse GitHub URL
        pattern = GITHUB_URL_PATTERN
        match = re.search(pattern, url_or_number)

        if not match:
            self.logger.error("Failed to parse GitHub URL", url=url_or_number)
            raise ValueError(f"Invalid GitHub URL: {url_or_number}")

        owner = match.group(1)
        repo = match.group(2)
        url_type = match.group(3)
        number = int(match.group(4))

        # Normalize type
        if url_type == "issues":
            parsed_type = "issue"
        else:
            parsed_type = "pr"

        self.logger.debug(
            "Parsed GitHub URL",
            owner=owner,
            repo=repo,
            url_type=url_type,
            parsed_type=parsed_type,
            number=number,
        )

        return parsed_type, owner, repo, number

    def _generate_branch_name(
        self,
        data: IssueData | PRData,
    ) -> str:
        """Generate branch name from issue/PR data.

        Args:
            data: Issue or PR data

        Returns:
            Branch name in format: issue-42-title or pr-123-title
        """
        # Get prefix and number
        if isinstance(data, IssueData):
            prefix = "issue"
            number = data.number
        else:
            prefix = "pr"
            number = data.number

        # Sanitize title for branch name
        sanitized_title = self._sanitize_title(data.title)

        # Combine: prefix-number-title
        branch_name = f"{prefix}-{number}-{sanitized_title}"

        # Truncate if too long (Git branch limit ~255 chars)
        if len(branch_name) > 200:
            original_length = len(branch_name)
            branch_name = branch_name[:200]
            self.logger.debug(
                "Branch name truncated",
                original_length=original_length,
                truncated_length=len(branch_name),
            )

        return branch_name

    def _sanitize_title(self, title: str) -> str:
        """Sanitize title for branch name.

        Args:
            title: Original title

        Returns:
            Sanitized title (lowercase, hyphens, no special chars)
        """
        # Convert to lowercase
        sanitized = title.lower()

        # Replace special chars with hyphens
        sanitized = re.sub(BRANCH_NAME_PATTERN, "-", sanitized)

        # Remove leading/trailing hyphens
        sanitized = sanitized.strip("-")

        return sanitized

    def _check_branch_conflict(self, branch_name: str) -> None:
        """Check if branch already exists and handle conflict.

        Args:
            branch_name: Branch name to check

        Raises:
            RuntimeError: If branch exists and user cancels removal
        """
        self.logger.debug("Checking for branch conflict", branch_name=branch_name)

        # Check if branch exists in worktrees
        try:
            result = subprocess.run(
                ["workmux", "list"],
                capture_output=True,
                text=True,
                timeout=self.settings.workmux_timeout,
            )

            if branch_name in result.stdout:
                self.logger.warning("Branch already exists", branch_name=branch_name)

                # Branch exists - prompt for removal
                response = (
                    input(
                        f"Branch '{branch_name}' already exists. Remove existing worktree? (y/n): "
                    )
                    .strip()
                    .lower()
                )

                if response == "y":
                    self.logger.info(
                        "Removing existing worktree", branch_name=branch_name
                    )
                    # Remove existing worktree
                    _ = subprocess.run(
                        ["workmux", "remove", branch_name],
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=self.settings.workmux_timeout,
                    )
                    self.logger.debug(
                        "Existing worktree removed successfully",
                        branch_name=branch_name,
                    )
                else:
                    self.logger.info(
                        "User cancelled worktree creation due to branch conflict",
                        branch_name=branch_name,
                    )
                    raise RuntimeError(
                        ERROR_USER_CANCELLED_BRANCH_CONFLICT.format(branch=branch_name)
                    )
            else:
                self.logger.debug(
                    "No branch conflict detected", branch_name=branch_name
                )

        except subprocess.CalledProcessError as e:
            self.logger.warning(
                "workmux list command failed, proceeding with creation",
                error=e.stderr if e.stderr else str(e),
                branch_name=branch_name,
            )
            pass
        except FileNotFoundError:
            # workmux not installed - proceed and let creation fail
            self.logger.warning("workmux not found, proceeding with worktree creation")
            pass

    def _create_worktree(self, branch_name: str) -> Path:
        """Create worktree using workmux or dry-run mode.

        Args:
            branch_name: Branch name for worktree

        Returns:
            Path to created worktree (or temporary worktree in dry-run mode)

        Raises:
            RuntimeError: If worktree creation fails (not in dry-run mode)
        """
        if self._dry_run:
            self.logger.debug(
                "Dry-run mode: creating temporary directory for WT-TASK.md",
                branch_name=branch_name,
            )
            # Dry-run mode: create temporary directory for WT-TASK.md only
            worktree_path = Path(self._worktree_root) / branch_name
            worktree_path.mkdir(parents=True, exist_ok=True)
            self.logger.debug("Temporary directory created", path=str(worktree_path))
            return worktree_path

        self.logger.info("Creating worktree using workmux", branch_name=branch_name)

        try:
            result = subprocess.run(
                ["workmux", "add", branch_name],
                check=True,
                capture_output=True,
                text=True,
                timeout=self.settings.workmux_timeout,
            )

            self.logger.debug("workmux command output", stdout=result.stdout[:500])

            # Extract worktree path from output
            # workmux add typically prints: Created worktree at /path/to/.worktrees/branch
            match = re.search(WORKMUX_CREATED_PATTERN, result.stdout)
            if match:
                worktree_path = Path(match.group(1))
                self.logger.debug(
                    "Extracted worktree path from output", path=str(worktree_path)
                )
                return worktree_path

            # Fallback: construct path manually using configured worktree root
            fallback_path = self.settings.get_effective_worktree_root() / branch_name
            self.logger.warning(
                "Could not extract worktree path from workmux output, using fallback",
                path=str(fallback_path),
            )
            return fallback_path

        except subprocess.CalledProcessError as e:
            if isinstance(e.stderr, str):
                error_msg = e.stderr
            else:
                error_msg = e.stderr.decode("utf-8", errors="replace")
            self.logger.error(
                "Failed to create worktree",
                branch_name=branch_name,
                error=error_msg[:500],
            )
            raise RuntimeError(
                ERROR_FAILED_TO_CREATE_WORKTREE.format(error=error_msg)
            ) from e
        except subprocess.TimeoutExpired as e:
            self.logger.error("Timeout creating worktree", branch_name=branch_name)
            raise RuntimeError(f"Timeout creating worktree '{branch_name}'") from e
        except FileNotFoundError as e:
            self.logger.error("workmux command not found")
            raise RuntimeError(ERROR_WORKMUX_NOT_INSTALLED) from e

    def _write_task_file(
        self,
        worktree_path: Path,
        data: IssueData | PRData,
    ) -> None:
        """Write WT-TASK.md to worktree.

        Args:
            worktree_path: Path to worktree directory
            data: Issue or PR data

        Raises:
            RuntimeError: If file write fails
        """
        self.logger.debug(
            "Rendering WT-TASK.md template", worktree_path=str(worktree_path)
        )

        # Generate content with full path context
        if isinstance(data, IssueData):
            content = self.template_renderer.render_for_issue(
                issue_data=data,
                parent_path=str(self._worktree_root.parent),
                worktree_name=worktree_path.name,
                branch_name=worktree_path.name,
            )
        else:
            content = self.template_renderer.render_for_pr(
                pr_data=data,
                parent_path=str(self._worktree_root.parent),
                worktree_name=worktree_path.name,
                branch_name=worktree_path.name,
            )

        # Write to worktree
        task_file_path = worktree_path / "WT-TASK.md"

        try:
            _ = task_file_path.write_text(content)
            self.logger.info(
                "WT-TASK.md written successfully", path=str(task_file_path)
            )
        except OSError as e:
            self.logger.error(
                "Failed to write WT-TASK.md", path=str(task_file_path), error=str(e)
            )
            raise RuntimeError(
                ERROR_FAILED_TO_WRITE_TASK_FILE.format(path=task_file_path)
            ) from e

    def _resolve_shuvcode_prompt(self, worktree_path: Path) -> str | None:
        """Resolve prompt content for shuvcode based on priority.

        Priority order:
        1. Custom --agent-prompt flag
        2. GHWT_AGENT_INIT_PROMPT env var (via settings.agent_prompt)
        3. GHWT_AGENT_INIT_PRESET env var (via settings.agent_prompt_preset)
        4. WT-TASK.md file content
        5. None (no prompt)

        Args:
            worktree_path: Path to worktree directory

        Returns:
            Prompt content or None
        """
        # Priority 1: Custom prompt (CLI flag or env var)
        if self.settings.agent_prompt:
            self.logger.debug("Using custom agent prompt")
            return self.settings.agent_prompt

        # Priority 2: Preset (CLI flag or env var)
        if self.settings.agent_prompt_preset:
            preset = PROMPT_PRESETS[self.settings.agent_prompt_preset]
            self.logger.debug(
                "Using preset prompt",
                preset=self.settings.agent_prompt_preset.value,
            )
            return preset

        # Priority 3: WT-TASK.md content
        task_file = worktree_path / "WT-TASK.md"
        if task_file.exists():
            content = task_file.read_text()
            self.logger.debug("Using WT-TASK.md as prompt", length=len(content))
            return content

        # Priority 4: No prompt (--no-prompt or file missing)
        if self.settings.no_prompt:
            self.logger.debug("No prompt (no-prompt flag set)")

        return None

    def _open_shuvcode(self, worktree_path: Path) -> None:
        """Open shuvcode on worktree with prompt based on settings.

        Behavior:
        - CI mode: `shuvcode run "<prompt>"` (non-interactive)
        - Normal mode: `shuvcode <path> --prompt "<prompt>"` (interactive)
        - No prompt: `shuvcode <path>` (current behavior)

        Args:
            worktree_path: Path to worktree directory

        Note:
            Failures are non-fatal - logged but don't raise
            Skipped in dry-run mode
        """
        if self._dry_run:
            self.logger.debug("Skipping shuvcode in dry-run mode")
            return

        if self.settings.no_prompt:
            self.logger.debug("Skipping prompt (no-prompt flag)")
            cmd = ["shuvcode", str(worktree_path)]
            env = None  # Use parent process environment
        else:
            prompt = self._resolve_shuvcode_prompt(worktree_path)

            if not prompt:
                self.logger.debug("No prompt available, opening shuvcode normally")
                cmd = ["shuvcode", str(worktree_path)]
                env = None  # Use parent process environment
            elif self.settings.ci_mode:
                # CI mode: non-interactive execution with auto-permissions
                self.logger.info(
                    "Opening shuvcode in CI mode", prompt_length=len(prompt)
                )
                cmd = ["shuvcode", "run", prompt]
                # Set OPENCODE_PERMISSION to auto-allow all operations in CI
                env = os.environ.copy()
                env["OPENCODE_PERMISSION"] = '{"*":"allow"}'
            else:
                # Interactive mode with initial prompt
                self.logger.info(
                    "Opening shuvcode with prompt", prompt_length=len(prompt)
                )
                cmd = ["shuvcode", str(worktree_path), "--prompt", prompt]
                env = None  # Use parent process environment

        self.logger.debug("Executing shuvcode command", command=" ".join(cmd))

        with contextlib.suppress(
            subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired
        ):
            _ = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=self.settings.file_write_timeout,
                env=env,
            )
