# Skill 用法

职责单向分开：**安装配置 → 原子操作 ← 未来独立编排 Skill**。

- [install-shared-ai-context](install-shared-ai-context/SKILL.md)：安装 CLI，设置命令和共享数据目录，提供专用 env 文件。
- [shared-ai-context](shared-ai-context/SKILL.md)：使用环境变量中的 CLI，提供 `context put/list/get` 当前上下文操作，以及 `new`、`list`、`write`、`history`、`read` 历史操作。

先让 agent 安装并配置，示例请求：

```text
使用 $install-shared-ai-context，从 /absolute/path/to/shared-ai-context 安装 CLI，
共享数据目录使用 /absolute/path/to/shared-data。
```

各 agent 随后在自己的命令执行环境加载同一个 env 文件，再直接调用 CLI：

```sh
source /absolute/path/to/shared-ai-context/.venv/shared-ai-context.env
"$SHARED_AI_CONTEXT_CLI" context put project:shared-ai-context architecture --summary 'CLI 与核心的当前设计。' --file /absolute/path/to/architecture.md --json
"$SHARED_AI_CONTEXT_CLI" context list project:shared-ai-context --json
"$SHARED_AI_CONTEXT_CLI" context get project:shared-ai-context architecture --json
"$SHARED_AI_CONTEXT_CLI" context get project:shared-ai-context architecture --detail --json
```

`scope` 显式使用 `user`、`project:<非空标识>` 或 `task:<非空标识>`，各范围不继承。当前上下文按 `scope/key` 完整覆写摘要和正文；列表只给索引，默认读取只给摘要，详情只给正文。更新不自动归档，内容由调用方准备。

也可以明确调用操作 Skill 保存当前内容：

```text
使用 $shared-ai-context，将 /absolute/path/to/architecture.md 保存为
project:shared-ai-context 范围的 architecture，摘要为“CLI 与核心的当前设计”。
```

需要追加历史时，先明确创建或选择会话，再调用原有操作：

```sh
"$SHARED_AI_CONTEXT_CLI" list --json
"$SHARED_AI_CONTEXT_CLI" new '导出功能修复' --project /absolute/path/to/project --json
```

```text
使用 $shared-ai-context，将 /absolute/path/to/handoff.md 写入会话 SESSION_ID，
标题为“导出修复交接”，用途为 handoff；返回确切引用。
```

未来编排按需放入 `skills/<workflow>/SKILL.md`，调用上述原子操作。操作 Skill 本身不承担摘要、汇总或多步编排，当前内容与历史也不互相兜底。安装 Skill 与原有 env 约定保持不变。

0.2 本轮修改操作 Skill 及用法，没有实际安装 CLI 或运行测试、校验、评审，由用户自行验收。
