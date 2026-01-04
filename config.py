"""Pydantic-based configuration for worktree automation."""

import os
import subprocess
from enum import Enum
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PromptPreset(str, Enum):
    """Prompt preset names for shuvcode agent initialization."""

    RALPH_LOOP = "ralph-loop"
    STANDARD_OOTL = "standard-ootl"
    MINIMAL = "minimal"


PROMPT_PRESETS = {
    PromptPreset.RALPH_LOOP: """Follow Ralph's autonomous development loop for all implementation work:

1. Read WT-TASK.md and consult @oracle immediately for assistance, reference WT-TASK.md, so oracle can gather critical research on the given task. Always use oracle on any issue you need more intelligence on during implementation.

2. Implement feature following the task requirements in WT-TASK.md

3. Create and update todo list to track all implementation steps

4. Run tests and ensure all pass

5. Verify code quality with linter checks

6. Update documentation as needed

7. Ask for final review from oracle before claiming completion
""",
    PromptPreset.STANDARD_OOTL: """Standard out-of-the-loop agent instructions:

1. Read WT-TASK.md thoroughly to understand the task

2. Implement the feature according to the requirements

3. Write comprehensive tests before implementation (TDD)

4. Ensure all tests pass

5. Follow code quality standards and best practices

6. Update documentation with changes made

7. Verify the implementation meets all acceptance criteria
""",
    PromptPreset.MINIMAL: """Minimal task execution:

1. Read WT-TASK.md to understand the task

2. Implement the required changes

3. Verify the implementation works correctly

4. Run existing tests and ensure they pass
""",
}


class WorktreeSettings(BaseSettings):
    """Configuration for worktree automation tool."""

    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Path configuration
    worktree_root: Path | None = Field(
        default=None,
        description="Root directory for worktrees (default: <git_repo>/.worktrees/)",
    )

    template_path: Path = Field(
        default=Path(__file__).parent / "WT_TASK_TEMPLATE.md",
        description="Path to WT-TASK.md template file",
    )

    # Timeouts
    gh_cli_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="GitHub CLI timeout in seconds",
    )

    workmux_timeout: int = Field(
        default=60,
        ge=1,
        le=300,
        description="Workmux timeout in seconds",
    )

    file_write_timeout: int = Field(
        default=5,
        ge=1,
        le=60,
        description="File write timeout in seconds",
    )

    # Logging
    verbose: bool = Field(default=False, description="Enable debug logging")
    quiet: bool = Field(default=False, description="Suppress info messages")

    # Agent prompt configuration
    agent_prompt: str | None = Field(
        default=None,
        description="Custom agent prompt (overrides preset and WT-TASK.md)",
    )

    agent_prompt_preset: PromptPreset | None = Field(
        default=None,
        description="Prompt preset to use (ralph-loop, standard-ootl, minimal)",
    )

    no_prompt: bool = Field(
        default=False,
        description="Skip prompt passing to shuvcode (current behavior)",
    )

    ci_mode: bool = Field(
        default=False,
        description="CI mode: non-interactive shuvcode execution",
    )

    @model_validator(mode="after")
    def validate_logging_flags(self) -> "WorktreeSettings":
        if self.verbose and self.quiet:
            raise ValueError(
                "Cannot set both --verbose and --quiet flags simultaneously"
            )
        return self

    @model_validator(mode="after")
    def validate_prompt_settings(self) -> "WorktreeSettings":
        """Ensure prompt options are mutually exclusive."""
        prompt_flags = [
            self.agent_prompt,
            self.agent_prompt_preset,
            self.no_prompt,
        ]
        active_flags = [f for f in prompt_flags if f]
        if len(active_flags) > 1:
            raise ValueError(
                "Cannot use --agent-prompt, --agent-preset, and --no-prompt together"
            )
        if self.ci_mode and self.no_prompt:
            raise ValueError("Cannot use --ci and --no-prompt together")
        return self

    @field_validator("worktree_root", mode="before")
    @classmethod
    def resolve_path(cls, v: str | Path | None) -> Path | None:
        """Resolve and expand paths before validation."""
        if v is None:
            return None
        if isinstance(v, str):
            v = Path(v)
        return v.expanduser().resolve()

    @field_validator("template_path", mode="before")
    @classmethod
    def resolve_template_path(cls, v: str | Path) -> Path:
        """
        Resolve template path for package resource.

        Resolution strategy:
        1. Expand user paths (~) and resolve to absolute
        2. Verify file exists
        3. Raise error if not found

        Note: Template is a package resource, not git repository content.
        """
        if isinstance(v, str):
            v = Path(v)

        resolved = v.expanduser().resolve()

        # Template is a package resource - it should exist at resolved path
        if not resolved.exists():
            raise ValueError(
                f"Template file not found: {v}\n"
                f"Resolved to: {resolved}\n"
                f"Template is packaged with ghwt tool - reinstall or check installation."
            )

        return resolved

    @classmethod
    def get_default_worktree_root(cls) -> Path:
        """
        Get default worktree root: <git_repo>/.worktrees/

        Returns:
            Path to default worktree directory

        Raises:
            RuntimeError: If not in a git repository or git not found
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            git_root = Path(result.stdout.strip()).resolve()
            return git_root / ".worktrees"
        except subprocess.CalledProcessError as e:
            if e.returncode == 128:
                raise RuntimeError(
                    "Not in a git repository. Run this command from within a git repository."
                ) from None
            stderr = (
                e.stderr
                if isinstance(e.stderr, str)
                else e.stderr.decode("utf-8", errors="replace")
            )
            raise RuntimeError(f"Git command failed: {stderr.strip()}") from None
        except FileNotFoundError:
            raise RuntimeError("Git is not installed") from None
        except subprocess.TimeoutExpired:
            raise RuntimeError("Git command timed out") from None

    def get_effective_worktree_root(self) -> Path:
        """
        Get effective worktree root, falling back to git repo default.

        Returns:
            Path to worktree root directory

        Raises:
            RuntimeError: If worktree root is not writable
        """
        if self.worktree_root is not None:
            # User-specified path (CLI flag or env var)
            self.worktree_root.mkdir(parents=True, exist_ok=True)
            # Verify write permissions
            if not os.access(self.worktree_root, os.W_OK):
                raise RuntimeError(f"Worktree root not writable: {self.worktree_root}")
            return self.worktree_root

        # Default: <git_repo>/.worktrees/
        default_root = self.get_default_worktree_root()
        default_root.mkdir(parents=True, exist_ok=True)
        # Verify write permissions
        if not os.access(default_root, os.W_OK):
            raise RuntimeError(f"Worktree root not writable: {default_root}")
        return default_root
