"""Click CLI interface for worktree automation."""

from pathlib import Path

import click
import structlog
from config import WorktreeSettings
from github_fetcher import GitHubIssueFetcher
from logging_config import configure_logging
from template_renderer import TemplateRenderer
from worktree_creator import WorktreeCreator


@click.command(name="ghwt")
@click.argument("input", type=str)
@click.option(
    "--issue",
    "item_type",
    flag_value="issue",
    help="Input is an issue (for bare numbers)",
)
@click.option(
    "--pr",
    "item_type",
    flag_value="pr",
    help="Input is a pull request (for bare numbers)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Skip workmux/shuvcode, only generate WT-TASK.md",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable debug logging",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress info messages, show only warnings/errors",
)
@click.option(
    "--worktree-root",
    type=click.Path(path_type=Path, exists=False),
    default=None,
    help="Root directory for worktrees (default: <git_repo>/.worktrees/)",
)
def cli(
    input: str,
    item_type: str | None,
    dry_run: bool,
    verbose: bool,
    quiet: bool,
    worktree_root: Path | None,
) -> None:
    """Create worktree from GitHub issue or PR.

    Accepts GitHub issue/PR URL or bare number with --issue/--pr flag.

    Examples:
        ghwt https://github.com/owner/repo/issues/42
        ghwt https://github.com/owner/repo/pull/123
        ghwt 42 --issue
        ghwt 123 --pr
        ghwt 42 --issue --dry-run
        ghwt 42 --issue --verbose
        ghwt 42 --issue --quiet

    The tool will:
        1. Fetch issue/PR data from GitHub
        2. Create a worktree using workmux (skip with --dry-run)
        3. Generate WT-TASK.md with comprehensive autonomous agent instructions
        4. Auto-open shuvcode editor on worktree (skip with --dry-run)
    """
    settings = WorktreeSettings(
        worktree_root=worktree_root,
        verbose=verbose,
        quiet=quiet,
    )

    configure_logging(verbose=settings.verbose, quiet=settings.quiet)
    logger = structlog.get_logger()

    logger.info(
        "CLI invoked",
        input=input,
        item_type=item_type,
        dry_run=dry_run,
        worktree_root=str(worktree_root) if worktree_root else "auto",
    )

    logger.debug("Initializing dependencies")
    issue_fetcher = GitHubIssueFetcher(gh_timeout=settings.gh_cli_timeout)

    template_renderer = TemplateRenderer(settings.template_path)

    creator = WorktreeCreator(
        issue_fetcher=issue_fetcher,
        template_renderer=template_renderer,
        settings=settings,
        dry_run=dry_run,
    )

    try:
        logger.info("Creating worktree from input", input=input)
        worktree_path = creator.create_from_github_url(input, item_type)

        logger.info("Worktree created successfully", worktree_path=str(worktree_path))
        logger.info("WT-TASK.md generated")

        if not dry_run:
            logger.info("Opening shuvcode editor")
            click.echo(f"✓ Worktree created: {worktree_path}")
            click.echo("✓ WT-TASK.md generated")
            click.echo("✓ shuvcode opened")
        else:
            logger.info("Dry-run mode: worktree and shuvcode skipped")
            click.echo(f"✓ Worktree created: {worktree_path}")
            click.echo("✓ WT-TASK.md generated")
            click.echo("✓ Dry-run mode (worktree and shuvcode skipped)")

    except ValueError as e:
        logger.error("Validation error", error=str(e))
        raise click.ClickException(str(e)) from None
    except RuntimeError as e:
        logger.error("Runtime error", error=str(e))
        raise click.ClickException(str(e)) from None
    except Exception as e:
        logger.exception("Unexpected error", error=str(e))
        raise


if __name__ == "__main__":
    cli()
