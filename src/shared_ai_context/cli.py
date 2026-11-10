"""Command line boundary: validate external input and present core results."""

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sqlite3
import sys

from .context import Context, ContextNotFound, RecordNotFound, SessionNotFound


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise argparse.ArgumentError(None, message)


def nonblank_title(value: str) -> str:
    if not value.strip():
        raise argparse.ArgumentTypeError("标题不能为空")
    return value


def positive_limit(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("数量必须为正整数")
    return number


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    want_json = "--json" in argv
    parser = Parser(
        prog="sctx",
        description="按明确指令保存、读取和交接本机 agent 的精简上下文。",
        epilog=(
            "数据目录：SHARED_AI_CONTEXT_HOME（绝对路径），"
            "默认 ~/.shared-ai-context；数据库文件名为 context.db。"
        ),
    )
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="创建任务会话")
    new.add_argument("title", type=nonblank_title)
    new.add_argument("--project", help="项目路径，仅作为定位文字")
    listing = commands.add_parser("list", help="列出会话元信息")
    listing.add_argument("--limit", type=positive_limit, default=20)
    write = commands.add_parser("write", help="追加共享或交接记录")
    write.add_argument("session_id")
    write.add_argument("--title", required=True, type=nonblank_title)
    write.add_argument("--kind", choices=("share", "handoff"), default="share")
    write.add_argument("--author")
    source = write.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path)
    source.add_argument("--stdin", action="store_true")
    history = commands.add_parser("history", help="列出会话历史元信息")
    history.add_argument("session_id")
    history.add_argument("--limit", type=positive_limit, default=20)
    read = commands.add_parser("read", help="读取确切记录")
    read.add_argument("session_id")
    read.add_argument("record_id")
    current = commands.add_parser("context", help="保存和读取可覆写的当前上下文")
    context_commands = current.add_subparsers(dest="context_command", required=True)
    put = context_commands.add_parser("put", help="完整覆写指定范围与主题的当前内容")
    put.add_argument("scope")
    put.add_argument("key")
    put.add_argument("--summary", required=True)
    context_source = put.add_mutually_exclusive_group(required=True)
    context_source.add_argument("--file", type=Path)
    context_source.add_argument("--stdin", action="store_true")
    context_listing = context_commands.add_parser("list", help="列出指定范围的上下文索引")
    context_listing.add_argument("scope")
    context_listing.add_argument("--limit", type=positive_limit, default=20)
    get = context_commands.add_parser("get", help="读取摘要，或用 --detail 读取正文")
    get.add_argument("scope")
    get.add_argument("key")
    get.add_argument("--detail", action="store_true")
    for command in (new, listing, write, history, read, put, context_listing, get):
        command.add_argument("--json", action="store_true", help="输出一个 JSON 结果对象")

    try:
        args = parser.parse_args(argv)
        if args.command == "context":
            scope_kind, _, scope_id = args.scope.partition(":")
            if args.scope != "user" and (
                scope_kind not in ("project", "task") or not scope_id.strip()
            ):
                parser.error("scope 必须是 user、project:<非空标识> 或 task:<非空标识>")
            if args.context_command in ("put", "get") and not args.key.strip():
                parser.error("key 不能为空")
            if args.context_command == "put" and not args.summary.strip():
                parser.error("摘要不能为空")

        if args.command == "write" or (
            args.command == "context" and args.context_command == "put"
        ):
            try:
                body = (args.file.read_bytes() if args.file else sys.stdin.buffer.read()).decode("utf-8")
            except (OSError, UnicodeError) as error:
                parser.error(f"无法读取 UTF-8 正文：{error}")
            if not body.strip():
                parser.error("正文不能为空")

        data_dir = Path(
            os.environ.get("SHARED_AI_CONTEXT_HOME", str(Path.home() / ".shared-ai-context"))
        ).expanduser()
        if not data_dir.is_absolute():
            parser.error("SHARED_AI_CONTEXT_HOME 必须是绝对数据目录")
        data_dir = data_dir.resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
        database_path = data_dir / "context.db"
        context = Context(database_path)

        if args.command == "new":
            data = asdict(context.create_session(args.title, args.project))
        elif args.command == "list":
            data = [asdict(session) for session in context.list_sessions(args.limit)]
        elif args.command == "write":
            data = asdict(
                context.append_record(
                    args.session_id, args.title, body, args.kind, args.author
                )
            )
            data["record_id"] = data.pop("id")
            if args.kind == "handoff":
                data["resume_prompt"] = (
                    f"sctx read {data['session_id']} {data['record_id']} --json"
                )
        elif args.command == "history":
            data = [asdict(record) for record in context.list_records(args.session_id, args.limit)]
        elif args.command == "context":
            if args.context_command == "put":
                data = asdict(context.put_context(args.scope, args.key, args.summary, body))
            elif args.context_command == "list":
                data = [asdict(item) for item in context.list_contexts(args.scope, args.limit)]
            else:
                data = asdict(context.get_context(args.scope, args.key, args.detail))
        else:
            data = asdict(context.get_record(args.session_id, args.record_id))
    except argparse.ArgumentError as error:
        code, message, status = "INVALID_INPUT", str(error), 2
    except (SessionNotFound, RecordNotFound) as error:
        code = "SESSION_NOT_FOUND" if isinstance(error, SessionNotFound) else "RECORD_NOT_FOUND"
        message, status = str(error), 1
    except ContextNotFound as error:
        code, message, status = "CONTEXT_NOT_FOUND", str(error), 1
    except (sqlite3.Error, OSError) as error:
        code, message, status = "STORAGE_ERROR", str(error), 1
    else:
        if want_json:
            print(json.dumps({"database_path": str(database_path), "data": data}, ensure_ascii=False))
        elif args.command == "read":
            print(data["body"], end="")
        elif args.command == "context" and args.context_command == "get":
            print(data["body" if args.detail else "summary"], end="")
        elif isinstance(data, list):
            print(f"database_path: {database_path}")
            for item in data:
                if args.command == "context":
                    print(f"{item['scope']}\t{item['key']}\t{item['updated_at']}")
                else:
                    print(f"{item['id']}\t{item['created_at']}\t{item['title']}")
        else:
            for key, value in data.items():
                print(f"{key}: {value}")
        return 0

    if want_json:
        print(json.dumps({"error": {"code": code, "message": message}}, ensure_ascii=False))
    else:
        print(f"{code}: {message}", file=sys.stderr)
    return status
