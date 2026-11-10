---
name: shared-ai-context
description: 按用户指令通过 sctx 创建会话、列出会话、写记录、列历史或读取指定记录。仅提供原子工具操作；正文准备和多步编排由调用方负责。
---

# 原子操作

前置：安装 Skill 已配置 `SHARED_AI_CONTEXT_CLI` 和 `SHARED_AI_CONTEXT_HOME`。缺少配置时转到 `install-shared-ai-context`；已配置就直接用下列命令，不再查 PATH、探测源码或处理安装。

只执行调用方要求的操作。示例中的路径、标题和 ID 换成当前请求的确切值；每条命令使用 `--json`。

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
