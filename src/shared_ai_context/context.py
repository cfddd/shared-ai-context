"""Store explicit context records in a local SQLite database.

Callers validate external input before invoking this module. Business queries
report missing objects; SQLite failures propagate to the entry point.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .models import Record, RecordKind, RecordSummary, Session


_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    project_path TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS records (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    title TEXT NOT NULL,
    kind TEXT NOT NULL,
    body TEXT NOT NULL,
    author TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS records_session_created
    ON records(session_id, created_at DESC, id DESC);
"""


class SessionNotFound(Exception):
    """The requested session does not exist."""


class RecordNotFound(Exception):
    """The record does not exist in the requested session."""


class Context:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def create_session(
        self, title: str, project_path: str | None = None
    ) -> Session:
        session = Session(
            id=str(uuid4()),
            title=title,
            project_path=project_path,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        with self._connection() as connection:
            connection.execute(
                "INSERT INTO sessions (id, title, project_path, created_at) "
                "VALUES (?, ?, ?, ?)",
                (session.id, session.title, session.project_path, session.created_at),
            )
        return session

    def list_sessions(self, limit: int = 20) -> list[Session]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, title, project_path, created_at FROM sessions "
                "ORDER BY created_at DESC, id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [Session(**dict(row)) for row in rows]

    def append_record(
        self,
        session_id: str,
        title: str,
        body: str,
        kind: RecordKind = "share",
        author: str | None = None,
    ) -> RecordSummary:
        with self._connection() as connection:
            _require_session(connection, session_id)
            record = RecordSummary(
                id=str(uuid4()),
                session_id=session_id,
                title=title,
                kind=kind,
                author=author,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            connection.execute(
                "INSERT INTO records "
                "(id, session_id, title, kind, body, author, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    record.id,
                    record.session_id,
                    record.title,
                    record.kind,
                    body,
                    record.author,
                    record.created_at,
                ),
            )
        return record

    def list_records(self, session_id: str, limit: int = 20) -> list[RecordSummary]:
        with self._connection() as connection:
            _require_session(connection, session_id)
            rows = connection.execute(
                "SELECT id, session_id, title, kind, author, created_at "
                "FROM records WHERE session_id = ? "
                "ORDER BY created_at DESC, id DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
        return [RecordSummary(**dict(row)) for row in rows]

    def get_record(self, session_id: str, record_id: str) -> Record:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT id, session_id, title, kind, author, created_at, body "
                "FROM records WHERE session_id = ? AND id = ?",
                (session_id, record_id),
            ).fetchone()
        if row is None:
            raise RecordNotFound(f"Record not found in session: {record_id}")
        return Record(**dict(row))

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        with closing(sqlite3.connect(self._db_path)) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(_SCHEMA)
            with connection:
                yield connection


def _require_session(connection: sqlite3.Connection, session_id: str) -> None:
    row = connection.execute(
        "SELECT 1 FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    if row is None:
        raise SessionNotFound(f"Session not found: {session_id}")
