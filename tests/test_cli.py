import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data_dir = self.root / "data"
        self.env = os.environ.copy()
        self.env.update(
            PYTHONPATH=str(ROOT / "src"),
            PYTHONDONTWRITEBYTECODE="1",
            SHARED_AI_CONTEXT_HOME=str(self.data_dir),
        )

    def run_cli(
        self, *args: str, body: str | None = None, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "shared_ai_context", *args],
            input=body,
            text=True,
            capture_output=True,
            env=self.env,
            cwd=cwd or self.root,
            timeout=15,
        )

    def test_cross_process_handoff_preserves_body_and_reference(self) -> None:
        created = self.run_cli("new", "导出修复", "--project", "/project", "--json")
        self.assertEqual(created.returncode, 0, created.stderr)
        session_id = json.loads(created.stdout)["data"]["id"]
        body = "\n# 目标\n保留中文与空白。\n\n下一步：检查导出。  \n"
        source = self.root / "handoff.md"
        source.write_text(body, encoding="utf-8")
        written = self.run_cli(
            "write", session_id, "--title", "交接", "--kind", "handoff",
            "--author", "agent-a", "--file", str(source), "--json",
        )
        self.assertEqual(written.returncode, 0, written.stderr)
        result = json.loads(written.stdout)
        record = result["data"]
        self.assertNotIn("body", record)
        self.assertNotIn("id", record)
        self.assertEqual(record["author"], "agent-a")
        self.assertEqual(record["session_id"], session_id)
        self.assertEqual(
            record["resume_prompt"],
            f"sctx read {session_id} {record['record_id']} --json",
        )
        other_cwd = self.root / "other-cwd"
        other_cwd.mkdir()
        read = self.run_cli("read", session_id, record["record_id"], "--json", cwd=other_cwd)
        self.assertEqual(read.returncode, 0, read.stderr)
        self.assertEqual(read.stderr, "")
        loaded = json.loads(read.stdout)
        self.assertEqual(loaded["database_path"], result["database_path"])
        self.assertEqual(loaded["data"]["body"], body)
        self.assertEqual(loaded["data"]["id"], record["record_id"])

    def test_history_returns_metadata_and_keeps_old_records(self) -> None:
        created = self.run_cli("new", "历史", "--json")
        session_id = json.loads(created.stdout)["data"]["id"]
        saved = []
        for index in range(2):
            result = self.run_cli(
                "write", session_id, "--title", f"记录{index}", "--stdin", "--json",
                body=f"private-body-{index}",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            saved.append(json.loads(result.stdout)["data"]["record_id"])
        history = self.run_cli("history", session_id, "--json")
        self.assertEqual(len(json.loads(history.stdout)["data"]), 2)
        self.assertNotIn("private-body", history.stdout)
        limited = self.run_cli("history", session_id, "--limit", "1", "--json")
        self.assertEqual(len(json.loads(limited.stdout)["data"]), 1)
        listing = self.run_cli("list", "--json")
        self.assertNotIn("private-body", listing.stdout)
        old = self.run_cli("read", session_id, saved[0], "--json")
        self.assertEqual(json.loads(old.stdout)["data"]["body"], "private-body-0")

    def test_invalid_external_input_fails_before_storage(self) -> None:
        cases = [
            (["new", "  "], None),
            (["list", "--limit", "0"], None),
            (["history", "session", "--limit", "abc"], None),
            (["write", "session", "--title", "标题", "--stdin"], " \n"),
            (["write", "session", "--title", "标题", "--kind", "other", "--stdin"], "正文"),
            (["write", "session", "--title", "标题", "--stdin", "--file", "x.md"], "正文"),
            (["write", "session", "--title", "标题", "--file", "missing.md"], None),
        ]
        for args, body in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args, "--json", body=body)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["error"]["code"], "INVALID_INPUT")
                self.assertFalse(self.data_dir.exists())

    def test_storage_path_failure_is_reported_without_fallback(self) -> None:
        blocker = self.root / "not-a-directory"
        blocker.write_text("preserve", encoding="utf-8")
        self.env["SHARED_AI_CONTEXT_HOME"] = str(blocker)
        result = self.run_cli("new", "任务", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["error"]["code"], "STORAGE_ERROR")
        self.assertEqual(blocker.read_text(encoding="utf-8"), "preserve")
        self.assertFalse(self.data_dir.exists())

    def test_relative_data_directory_is_an_input_error(self) -> None:
        self.env["SHARED_AI_CONTEXT_HOME"] = "relative-data"
        result = self.run_cli("list", "--json")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["error"]["code"], "INVALID_INPUT")
        self.assertFalse((self.root / "relative-data").exists())

    def test_missing_targets_have_business_error_codes(self) -> None:
        missing_session = self.run_cli("history", "missing", "--json")
        self.assertEqual(missing_session.returncode, 1)
        self.assertEqual(
            json.loads(missing_session.stdout)["error"]["code"], "SESSION_NOT_FOUND"
        )
        missing_record = self.run_cli("read", "missing", "missing", "--json")
        self.assertEqual(missing_record.returncode, 1)
        self.assertEqual(
            json.loads(missing_record.stdout)["error"]["code"], "RECORD_NOT_FOUND"
        )

    def test_two_process_writes_keep_both_records(self) -> None:
        created = self.run_cli("new", "并行共享", "--json")
        session_id = json.loads(created.stdout)["data"]["id"]
        processes = []
        for index in range(2):
            source = self.root / f"body-{index}.md"
            source.write_text(f"agent-{index}", encoding="utf-8")
            processes.append(
                subprocess.Popen(
                    [
                        sys.executable, "-m", "shared_ai_context", "write", session_id,
                        "--title", f"记录{index}", "--file", str(source), "--json",
                    ],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    env=self.env, cwd=self.root,
                )
            )
        record_ids = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, stderr)
            record_ids.append(json.loads(stdout)["data"]["record_id"])
        self.assertEqual(len(set(record_ids)), 2)
        for index, record_id in enumerate(record_ids):
            result = self.run_cli("read", session_id, record_id, "--json")
            self.assertEqual(json.loads(result.stdout)["data"]["body"], f"agent-{index}")

    def test_help_import_and_text_output(self) -> None:
        help_result = self.run_cli("--help")
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("SHARED_AI_CONTEXT_HOME", help_result.stdout)
        subprocess.run(
            [sys.executable, "-c", "import shared_ai_context; import shared_ai_context.cli"],
            cwd=self.root, env=self.env, check=True, timeout=15,
        )
        self.assertFalse(self.data_dir.exists())
        created = self.run_cli("new", "文本", "--json")
        session_id = json.loads(created.stdout)["data"]["id"]
        written = self.run_cli(
            "write", session_id, "--title", "短记录", "--stdin", "--json", body="正文\n"
        )
        record_id = json.loads(written.stdout)["data"]["record_id"]
        read = self.run_cli("read", session_id, record_id)
        self.assertEqual(read.stdout, "正文\n")
        listing = self.run_cli("list")
        self.assertIn(str(self.data_dir / "context.db"), listing.stdout)
        self.assertNotIn("正文", listing.stdout)


if __name__ == "__main__":
    unittest.main()
