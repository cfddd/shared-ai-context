# shared-ai-context

个人使用的 Engram 记忆仓库。保存经验、偏好、决策摘要和任务交接，通过 Git 在机器之间同步；`fengdi-kb-agent` 独立管理知识和配置，使用工具的 Agent 按需查询它。

这里维护记忆数据和使用约定，直接使用 Engram，不再开发 `sctx`。旧 CLI 与规格保留在本地标签 `sctx-v0.2.0`（`9f73af9`）。本轮搭建和用户自验状态见 [团队记录](docs/TEAM.md)。

## 本机入口

本机已配置 Engram `3.7.0`、统一数据目录及 Codex / Cursor / Qoder 的只读 MCP；原默认 Engram 库已一致性复制并保留原库。本轮没有写入测试记忆，宿主加载与场景效果由用户自验，具体状态见 [团队记录](docs/TEAM.md)。当前终端可在仓库根目录加载环境：

```sh
source .local/engram.env
"$ENGRAM_BIN" tui
```

环境文件提供 `ENGRAM_BIN`（可执行文件绝对路径）、`ENGRAM_DATA_DIR`（本机数据目录）和 `ENGRAM_REPO`（本仓库绝对路径）。`ENGRAM_REPO` 是本仓库的定位约定，非 Engram 官方参数；不固定全局 `ENGRAM_PROJECT`。Shell 从 `~/.zshenv` 加载环境，MCP 显式配置相同数据目录；配置写入后，现有宿主需重启或新开会话才能加载。MCP 只开放搜索和读取工具，保存由明确的 CLI 调用完成。

| 文件 | 归属 |
| --- | --- |
| `.local/engram/engram.db` | 本机记忆数据库，忽略提交 |
| `.local/engram.env` | 本机环境与绝对路径，忽略提交 |
| `.engram/manifest.json`、`.engram/chunks/` | Engram 生成的同步数据，包含记忆正文，按需提交 |
| `spaces.md` | 空间命名约定，不是程序注册表 |
| `skills/` | Skill 正本；客户端使用安装副本 |

当前 `origin` 是公开仓库。包含真实记忆的 `.engram/` 只在确定合适的远程后发布；本次用户授权提交推送的范围仅为仓库骨架、文档、Skill 与旧源码退役。

## 常用场景

先明确 [空间](spaces.md)。例如工作区用 `work-risk-platform`，个人偏好用 `personal`，学习背景用 `learning`。这些名字可以覆盖多个 Git 仓库，也可以与代码无关。

| 对 Agent 说 | 使用方式 |
| --- | --- |
| “接着做 work-risk-platform 的权限改造” | 用 [engram-memory](skills/engram-memory/SKILL.md) 搜索该空间，按需读取正文 |
| “记住这个结论，放到 personal” | 保存精简内容；已有主题沿用稳定 topic 更新 |
| “把权限改造交接一下” | 用 [engram-handoff](skills/engram-handoff/SKILL.md) 整理目标、进度、未验证项和下一步 |
| “汇总这几份 Agent 交接” | 只读取明确提供或可访问的材料，保留分歧后生成一份汇总 |
| “找一下相关知识资料” | 调用现有 `fengdi-kb-agent`；记忆仅保留必要结论和来源引用 |
| “同步记忆到另一台机器” | 用 [engram-sync](skills/engram-sync/SKILL.md) 导出或导入；Git 操作按当前授权执行 |

不在每次启动时加载所有记忆。读取的历史资料用作背景和证据，当前用户指令决定接下来做什么。

## 保存与更新

以下是写法示例，内容不会自动保存：

```sh
"$ENGRAM_BIN" save '权限改造的当前决定' \
  '结论：先调整 IAM 与 Admin。原因：本轮范围限定在鉴权入口。依据：相关设计文档路径。未验证：真实联调。' \
  --project work-risk-platform \
  --type decision \
  --topic decision/permission-refactor

"$ENGRAM_BIN" search '权限改造' --project work-risk-platform --limit 5
```

首轮统一使用默认 `scope=project`，通过显式 `--project` 区分空间。`personal` 是空间名，不代表隐私边界或自动加载。更新同一主题沿用相同 project、scope、topic；Engram 会保留旧版本，不能因此承诺数据库大小不增长。

CLI 搜索只返回截断内容；Agent 需要完整正文时使用 MCP `mem_get_observation`，人可以用 `tui`。跨机器先重新搜索，使用该机器返回的记录 ID。

## 配合知识库

先检索与当前任务相关的记忆，需要完整说明或依据时，再用 `fengdi-kb-agent` 搜索和读取原文。知识库继续使用它自己的路径、索引和笔记管理功能。

记忆中可保留普通文本引用，例如 `工具=fengdi-kb；domain=work；rel_path=项目/权限平台/鉴权链路.md`。完整知识在原位置维护；本仓库不放 `knowledge/`，不复制索引，也不实现引用解析器。

## 换机器与同步

同一台机器的 Agent 使用同一 `ENGRAM_DATA_DIR`，直接共享数据库。跨机器通过 `.engram/` 交换记忆：

```text
机器 A 数据库 → engram sync --all → Git 同步文件
Git 拉取文件 → engram sync --import --all → 机器 B 数据库
```

工作结束后，在本仓库根目录执行 `"$ENGRAM_BIN" sync --all`；确认新增文件后，再按授权提交和推送。工作开始前先拉取，再执行 `"$ENGRAM_BIN" sync --import --all`。`sync` 不替你提交或推送，Git 拉取也不自动导入数据库。

默认 Git Sync 不导出原始 prompts，明确需要时才加 `--include-prompts`。同步覆盖已导出的记忆，不等同于完整 SQLite 备份；本机数据库另纳入常规备份。跨机器优先一台结束同步、另一台开始拉取，不建设并发合并流程。

新机器安装 [官方稳定版](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/docs/INSTALLATION.md)，克隆已确定的记忆仓库后，在根目录设置本机环境并导入：

```sh
brew install gentleman-programming/tap/engram
export ENGRAM_BIN="$(command -v engram)"
export ENGRAM_REPO="$PWD"
export ENGRAM_DATA_DIR="$PWD/.local/engram"
"$ENGRAM_BIN" sync --import --all
```

在新机器的 MCP 配置中使用该机器的可执行文件和数据目录绝对路径，参照实际安装 Skill 的用法。原始记忆库不会因改变环境变量而自动搬迁。

## 本轮交付边界

[003 规格](specs/003-engram-memory/spec.md) 定义本轮范围与用户自验。未运行测试、lint、Skill 验证器或跨机器演示；不向真实记忆库写入测试条目。独立 Reviewer 仅作只读评审，配置已写入与宿主已实际加载分别记录。

官方参考：[Git Sync](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/DOCS.md#git-sync-chunked)、[按需读取与 topic](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/docs/ARCHITECTURE.md)、[scope 的同步边界](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/docs/TEAM-USAGE.md)。
