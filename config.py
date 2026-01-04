"""Pydantic-based configuration for worktree automation."""

import os
import subprocess
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    @model_validator(mode="after")
    def validate_logging_flags(self) -> "WorktreeSettings":
        if self.verbose and self.quiet:
            raise ValueError("Cannot set both --verbose and --quiet flags simultaneously")
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
                raise RuntimeError("Not in a git repository. Run this command from within a git repository.") from None
            stderr = e.stderr if isinstance(e.stderr, str) else e.stderr.decode("utf-8", errors="replace")
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
