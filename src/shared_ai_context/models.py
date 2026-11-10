"""Shared result types for context storage and its entry points."""

from dataclasses import dataclass
from typing import Literal


RecordKind = Literal["share", "handoff"]


@dataclass(frozen=True)
class Session:
    id: str
    title: str
    project_path: str | None
    created_at: str


@dataclass(frozen=True)
class RecordSummary:
    id: str
    session_id: str
    title: str
    kind: RecordKind
    author: str | None
    created_at: str


@dataclass(frozen=True)
class Record(RecordSummary):
    body: str


@dataclass(frozen=True)
class ContextIndex:
    scope: str
    key: str
    updated_at: str


@dataclass(frozen=True)
class ContextSummary(ContextIndex):
    summary: str


@dataclass(frozen=True)
class ContextDetail(ContextIndex):
    body: str
