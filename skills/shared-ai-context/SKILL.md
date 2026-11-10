---
name: shared-ai-context
description: 按用户指令通过 sctx 保存和读取当前上下文，或创建会话、追加和读取历史记录。仅提供原子工具操作；内容准备和多步编排由调用方负责。
---

# 原子操作

前置：安装 Skill 已配置 `SHARED_AI_CONTEXT_CLI` 和 `SHARED_AI_CONTEXT_HOME`。缺少配置时转到 `install-shared-ai-context`；已配置就直接用下列命令，不再查 PATH、探测源码或处理安装。

只执行调用方要求的操作。示例中的路径、标题和 ID 换成当前请求的确切值；每条命令使用 `--json`。

## 覆写当前上下文

调用方提供明确的 `scope`、稳定主题名 `key`、摘要和 UTF-8 正文文件：

```sh
"$SHARED_AI_CONTEXT_CLI" context put project:shared-ai-context architecture --summary 'CLI 直接调用 SQLite 核心，当前内容与历史独立。' --file /absolute/path/to/architecture.md --json
```

`scope` 使用 `user`、`project:<非空标识>` 或 `task:<非空标识>`，按调用方指定值传入，各范围独立。每次 `put` 同时完整覆写同一 `scope/key` 的摘要和正文，只返回 `scope`、`key`、`updated_at`。正文也可通过 `--stdin` 提供，与 `--file` 二选一。内容由调用方准备，操作 Skill 不生成摘要或合并内容。

## 列出当前上下文

```sh
"$SHARED_AI_CONTEXT_CLI" context list project:shared-ai-context --json
```

仅返回该范围的 `scope`、`key`、`updated_at`，按 `key` 排序，默认最多 20 项，可用 `--limit 50` 调整。用列表定位确切主题。

## 读取当前上下文

```sh
"$SHARED_AI_CONTEXT_CLI" context get project:shared-ai-context architecture --json
"$SHARED_AI_CONTEXT_CLI" context get project:shared-ai-context architecture --detail --json
```

按调用方要求选择一条命令：默认只返回摘要，显式 `--detail` 只返回正文，均带 `scope`、`key`、`updated_at`。读取限定在确切 `scope/key`，不继承其他范围；不存在时返回 `CONTEXT_NOT_FOUND`。

当前内容的覆写不会自动归档。需要保留历史时，调用方明确要求下列 `write` 操作；当前内容与历史记录各自存取，不互相兜底。

## 创建会话

```sh
"$SHARED_AI_CONTEXT_CLI" new '导出功能修复' --project /absolute/path/to/project --json
```

返回的 `data.id` 是会话 ID，后续命令中的 `SESSION_ID` 使用此值。

## 列出会话

```sh
"$SHARED_AI_CONTEXT_CLI" list --json
```

列表仅含元信息，用于选择确切会话。

## 写入记录

正文由调用方准备为 UTF-8 文件：

```sh
"$SHARED_AI_CONTEXT_CLI" write SESSION_ID --title '导出修复交接' --kind handoff --author agent-a --file /absolute/path/to/handoff.md --json
```

返回的 `data.session_id` 和 `data.record_id` 是记录的确切引用。`--kind handoff` 只是用途；普通记录可省略，写入总是追加。

## 列出历史

```sh
"$SHARED_AI_CONTEXT_CLI" history SESSION_ID --json
```

历史仅含元信息，记录 ID 为各项的 `id`。会话与历史列表可通过 `--limit 50` 调整数量。

## 读取记录

```sh
"$SHARED_AI_CONTEXT_CLI" read SESSION_ID RECORD_ID --json
```

只按确切双 ID 读取指定正文，不把最新记录当作完整状态。成功结果含 `database_path` 和 `data`；失败时返回实际错误，不在本 Skill 排错或修改配置。
