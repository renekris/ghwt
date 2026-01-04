# Quickstart Guide

## Prerequisites

Install required tools before using worktree-automation:

```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture)] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update
sudo apt install gh

# Authenticate with GitHub
gh auth login

# Install workmux (git worktree manager)
cargo install workmux
```

## Installation

```bash
cd worktree-automation
uv pip install -e .
```

## Basic Usage

### Create Worktree from GitHub Issue

```bash
worktree-automation https://github.com/owner/repo/issues/42 --issue
```

**What happens:**
1. Fetches issue #42 data from GitHub
2. Creates worktree: `.worktrees/issue-42-issue-title/`
3. Generates `WT-TASK.md` with comprehensive instructions
4. Opens shuvcode editor on the worktree

### Create Worktree from Pull Request

```bash
worktree-automation https://github.com/owner/repo/pull/123 --pr
```

**What happens:**
1. Fetches PR #123 data (including file changes)
2. Creates worktree: `.worktrees/pr-123-pr-title/`
3. Generates `WT-TASK.md` with PR-specific context
4. Opens shuvcode editor

### Using Bare Numbers

If you have just a number (not a URL), specify type:

```bash
# Issue
worktree-automation 42 --issue

# Pull Request
worktree-automation 123 --pr
```

### Dry-Run Mode (Testing)

Skip workmux/shuvcode, only generate task file:

```bash
worktree-automation 42 --issue --dry-run
```

**Use case**: Preview the `WT-TASK.md` content before creating worktree.

## Worktree Strategy

### Parent vs Worktree

- **Parent Directory** (e.g., `/path/to/repo/`): Single source of truth for gitignored data
- **Worktree Directory** (`.worktrees/issue-42-title/`): Code-only workspace with symlinks

### Symlink Setup

Worktrees should have symlinks to parent's data:

```bash
cd .worktrees/issue-42-title
ls -la | grep "^l"

# Expected output:
# .env -> ../../.env
# data -> ../../data
# logs -> ../../logs

# Recreate if missing:
ln -s ../../.env . && ln -s ../../data . && ln -s ../../logs .
```

## Branch Naming

Generated branch names follow this pattern:

- **Issues**: `issue-{number}-{sanitized-title}`
  - Example: `issue-42-fix-database-connection-error`
- **PRs**: `pr-{number}-{sanitized-title}`
  - Example: `pr-123-add-user-authentication`

Special characters in titles are replaced with hyphens.

## Branch Conflicts

If a worktree with the same branch exists:

```bash
worktree-automation 42 --issue
# Output: Branch 'issue-42-title' already exists. Remove existing worktree? (y/n):
```

- **Type `y`**: Removes existing worktree and creates new one
- **Type `n`**: Cancels operation (no changes made)

## WT-TASK.md Structure

The generated task file has 9 sections:

1. **Worktree Context & Rules** - Symlinks, workflow, commands
2. **HOTL Protocol** - Human guidance and tracking
3. **Self-Verification Conditions** - Completion gates
4. **Early PR Creation Guidance** - When and how to create PR
5. **Escalation Conditions** - When to get help
6. **Status Tracking** - Progress indicators
7. **GitHub Issue/PR Data** - Original issue/PR details
8. **Implementation Plan** - Structured task breakdown
9. **Notes & Artifacts** - Code snippets, resources, logs

## Workflows

### 1. Start New Issue Work

```bash
# Create worktree from issue URL
worktree-automation https://github.com/owner/repo/issues/42 --issue

# Work is now in: .worktrees/issue-42-title/

# After completing work, return to parent
cd ../..

# Review and merge
# (use git commands to merge feature branch into main)
```

### 2. Preview Before Creating Worktree

```bash
# Dry-run to see task file content
worktree-automation 42 --issue --dry-run

# Review the generated .worktrees/issue-42-title/WT-TASK.md

# Create actual worktree if happy with content
worktree-automation 42 --issue
```

### 3. Work on Pull Request

```bash
# Create worktree from PR URL
worktree-automation https://github.com/owner/repo/pull/123 --pr

# The worktree includes:
# - PR description and title
# - Files changed in PR
# - PR author and comments

# Make changes in the worktree
cd .worktrees/pr-123-title/

# Commit and push (workmux handles this)
```

### 4. Test Template Rendering

```bash
# Create temporary worktree without workmux
worktree-automation 999 --issue --dry-run

# Inspect the generated task file
cat .worktrees/issue-999-title/WT-TASK.md

# Delete test worktree
rm -rf .worktrees/issue-999-title
```

## Cleanup

### Remove Worktree

```bash
# Use workmux to remove worktree
workmux remove issue-42-title

# Or manually delete directory
rm -rf .worktrees/issue-42-title
```

### List All Worktrees

```bash
workmux list
```

## Environment Variables

### WORKTREE_ROOT

Set custom location for `.worktrees/` directory:

```bash
# Set environment variable
export WORKTREE_ROOT=/custom/path/to/worktrees

# Or use CLI flag
worktree-automation 42 --issue --worktree-root /custom/path/to/worktrees
```

**Default**: Parent directory (`../` relative to worktree)

## Troubleshooting

### GitHub CLI Not Found

```bash
# Check if gh is installed
which gh

# If not, install (see Prerequisites section)
```

### Worktree Creation Fails

```bash
# Verify workmux is installed
which workmux

# Check worktree root permissions
ls -la .worktrees

# Ensure you can write to directory
touch .worktrees/test
```

### Template File Not Found

```bash
# Verify WT_TASK_TEMPLATE.md exists
ls WT_TASK_TEMPLATE.md

# Should be in same directory as main.py
```

### Dry-Run Creates Files But Not Worktree

**Expected behavior**: Dry-run creates directory and `WT-TASK.md` but skips workmux.

```bash
# Dry-run output:
✓ Worktree created: .worktrees/issue-42-title/
✓ WT-TASK.md generated
✓ Dry-run mode (worktree and shuvcode skipped)
```

## Advanced Usage

### Multiple Worktrees for Same Issue

```bash
# Create first worktree
worktree-automation 42 --issue

# Remove it when done
workmux remove issue-42-title

# Create new worktree (handles conflict)
worktree-automation 42 --issue
# Prompts: Branch already exists. Remove? (y/n):
# Type 'y' to proceed
```

### Batch Worktree Creation

```bash
# Create worktrees for multiple issues
for issue in 42 43 44; do
  worktree-automation $issue --issue
done
```

### Custom Worktree Root with Docker

```bash
# Mount custom worktree root in container
docker run -v $(pwd)/my-worktrees:/worktrees \
  -e WORKTREE_ROOT=/worktrees \
  worktree-automation:latest 42 --issue
```

## Next Steps

1. **Read the WT-TASK.md**: Understand autonomous agent protocol
2. **Follow HOTL guidance**: Check in with human supervisor regularly
3. **Track progress**: Update status markers in task file
4. **Self-verify**: Complete all verification conditions before marking done
5. **Escalate early**: Get help if blocked (don't spin wheels)

## Getting Help

- **Issue tracker**: https://github.com/owner/worktree-automation/issues
- **Documentation**: See README.md for detailed API reference
- **GitHub CLI**: `gh help`
- **Workmux**: `workmux --help`
