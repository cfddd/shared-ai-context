import sqlite3
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from shared_ai_context.context import Context, RecordNotFound, SessionNotFound


class ContextTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.db_path = Path(directory.name) / "context.db"
        self.context = Context(self.db_path)

    def test_constructor_has_no_storage_side_effect(self):
        self.assertFalse(self.db_path.exists())

    def test_sessions_persist_across_instances(self):
        session = self.context.create_session("上下文设计", "/project/notes")

        self.assertEqual(Context(self.db_path).list_sessions(), [session])
        self.assertEqual(str(UUID(session.id)), session.id)
        self.assertEqual(
            datetime.fromisoformat(session.created_at).utcoffset(), timedelta(0)
        )

    def test_session_list_has_default_limit_and_stable_order(self):
        sessions = [self.context.create_session(f"Task {i}") for i in range(21)]
        expected = sorted(
            sessions, key=lambda session: (session.created_at, session.id), reverse=True
        )

        self.assertEqual(self.context.list_sessions(), expected[:20])
        self.assertEqual(self.context.list_sessions(limit=2), expected[:2])

    def test_record_persists_exact_body_and_metadata(self):
        session = self.context.create_session("CLI")
        body = "\n# 已确认\n中文与 '引号'、$()、反引号 `code`\n\n"
        summary = self.context.append_record(
            session.id, "交接", body, kind="handoff", author="Agent A"
        )

        record = Context(self.db_path).get_record(session.id, summary.id)
        metadata = asdict(record)
        self.assertEqual(metadata.pop("body"), body)
        self.assertEqual(metadata, asdict(summary))
        self.assertNotIn("body", asdict(summary))

    def test_history_keeps_old_records_and_contains_only_metadata(self):
        session = self.context.create_session("Keep history")
        first = self.context.append_record(session.id, "First", "original")
        second = self.context.append_record(session.id, "Second", "later")

        self.assertEqual(self.context.list_records(session.id), [second, first])
        self.assertEqual(self.context.get_record(session.id, first.id).body, "original")
        self.assertEqual(self.context.get_record(session.id, second.id).body, "later")
        self.assertTrue(
            all("body" not in asdict(item) for item in self.context.list_records(session.id))
        )

    def test_history_has_default_and_explicit_limits(self):
        session = self.context.create_session("Long history")
        records = [
            self.context.append_record(session.id, f"Record {i}", f"Body {i}")
            for i in range(21)
        ]
        expected = sorted(
            records, key=lambda record: (record.created_at, record.id), reverse=True
        )

        self.assertEqual(self.context.list_records(session.id), expected[:20])
        self.assertEqual(self.context.list_records(session.id, limit=3), expected[:3])

    def test_record_lookup_and_history_are_isolated_by_session(self):
        first = self.context.create_session("First")
        second = self.context.create_session("Second")
        record = self.context.append_record(second.id, "Private scope", "only second")

        self.assertEqual(self.context.list_records(first.id), [])
        with self.assertRaises(RecordNotFound):
            self.context.get_record(first.id, record.id)
        with self.assertRaises(RecordNotFound):
            self.context.get_record(second.id, "missing")

    def test_missing_session_is_a_business_error(self):
        with self.assertRaises(SessionNotFound):
            self.context.append_record("missing", "Note", "Body")
        with self.assertRaises(SessionNotFound):
            self.context.list_records("missing")
        self.assertEqual(self.context.list_sessions(), [])

    def test_independent_writers_preserve_both_records(self):
        session = self.context.create_session("Two writers")
        with ThreadPoolExecutor(max_workers=2) as executor:
            first = executor.submit(
                Context(self.db_path).append_record, session.id, "A", "from A"
            )
            second = executor.submit(
                Context(self.db_path).append_record, session.id, "B", "from B"
            )
            records = [first.result(), second.result()]

        self.assertEqual(len({record.id for record in records}), 2)
        self.assertEqual(
            {self.context.get_record(session.id, record.id).body for record in records},
            {"from A", "from B"},
        )

    def test_sqlite_failure_propagates_to_caller(self):
        blocked_path = self.db_path.parent / "not-a-directory"
        blocked_path.write_text("occupied", encoding="utf-8")

        with self.assertRaises(sqlite3.Error):
            Context(blocked_path / "context.db").list_sessions()


if __name__ == "__main__":
    unittest.main()
