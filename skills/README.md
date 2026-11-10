# Skill 用法

职责单向分开：**安装配置 → 原子操作 ← 未来独立编排 Skill**。

- [install-shared-ai-context](install-shared-ai-context/SKILL.md)：安装 CLI，设置命令和共享数据目录，提供专用 env 文件。
- [shared-ai-context](shared-ai-context/SKILL.md)：使用环境变量中的 CLI，提供 `new`、`list`、`write`、`history`、`read` 五项操作。

先让 agent 安装并配置，示例请求：

```text
使用 $install-shared-ai-context，从 /absolute/path/to/shared-ai-context 安装 CLI，
共享数据目录使用 /absolute/path/to/shared-data。
```

各 agent 随后在自己的命令执行环境加载同一个 env 文件，再直接调用 CLI：

```sh
source /absolute/path/to/shared-ai-context/.venv/shared-ai-context.env
"$SHARED_AI_CONTEXT_CLI" list --json
"$SHARED_AI_CONTEXT_CLI" new '导出功能修复' --project /absolute/path/to/project --json
```

也可以明确调用操作 Skill：

```text
使用 $shared-ai-context，将 /absolute/path/to/handoff.md 写入会话 SESSION_ID，
标题为“导出修复交接”，用途为 handoff；返回确切引用。
```

未来编排按需放入 `skills/<workflow>/SKILL.md`，调用上述原子操作。多源汇总属于未来独立 Skill；目前调用方仍可组合多次 `read` 和一次 `write`，操作 Skill 本身不承担摘要或汇总。

本轮只生成和同步这两份 Skill 及用法，没有实际安装 CLI 或运行验证，由用户自行验收。
