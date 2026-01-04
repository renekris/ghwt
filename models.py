"""Data models for GitHub issue/PR data."""

from dataclasses import dataclass


@dataclass
class CommentData:
    """GitHub comment data."""

    author: str
    body: str
    created_at: str


@dataclass
class IssueData:
    """GitHub issue data."""

    title: str
    body: str
    number: int
    author: str
    labels: list[str]
    state: str
    url: str
    comments: list[CommentData]


@dataclass
class FileChange:
    """GitHub PR file change data."""

    path: str


@dataclass
class PRData:
    """GitHub PR data."""

    title: str
    body: str
    number: int
    author: str
    labels: list[str]
    state: str
    url: str
    comments: list[CommentData]
    head_branch: str
    base_branch: str
    mergeable: bool | None
    additions: int | None
    deletions: int | None
    files_changed: list[FileChange]
