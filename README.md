# shared-ai-context

个人使用的 Engram 记忆仓库，用于工作续接，以及保留实际任务和交互中学到的可复用经验，通过 Git 在机器之间同步。知识原理、完整资料和已有规则从原文获取；`fengdi-kb-agent` 独立管理知识和配置。

这里维护记忆数据和使用约定，直接使用 Engram，不再开发 `sctx`。旧 CLI 与规格保留在标签 `sctx-v0.2.0`（`9f73af9`）。搭建、职责调整和用户自验状态见 [团队记录](docs/TEAM.md)。

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

当前 `origin` 是公开仓库。已发布内容仅为仓库骨架、文档、Skill 与旧源码退役；包含真实记忆的 `.engram/` 只在确定合适的远程后发布。本轮职责调整与用户授权的记忆保存不包含提交或推送。

## 常用场景

Agent 从当前工作定位 [空间与主题](spaces.md)，通常无需用户填写。`work-risk-platform` 表示跨仓库合作，`personal` 表示个人协作背景与经历，`learning` 表示学习任务及实际尝试；这些是合作归属，不是知识学科目录。

| 对 Agent 说 | 使用方式 |
| --- | --- |
| “接着做 work-risk-platform 的权限改造” | 用 [engram-memory](skills/engram-memory/SKILL.md) 搜索该空间，按需读取正文 |
| “记住这次新增的协作约束” | 按 [写入准入](skills/engram-memory/SKILL.md) 选择内容，复用或定位主题后保存 |
| “记住这次实际学到的做法，注明适用条件” | 用同一准入判断经验是否值得保留，记录来源与尚未确认的判断 |
| “把权限改造交接一下” | 用 [engram-handoff](skills/engram-handoff/SKILL.md) 整理目标、进度、未验证项和下一步 |
| “汇总这几份 Agent 交接” | 只读取明确提供或可访问的材料，保留分歧后生成一份汇总 |
| “找一下相关知识资料” | 调用现有 `fengdi-kb-agent` 检索并读取原文 |
| “复核这条记忆”或“纠正并更新它” | 按 [复核纠错](skills/engram-memory/references/review.md) 区分只读复核与已授权更新 |
| “同步记忆到另一台机器” | 用 [engram-sync](skills/engram-sync/SKILL.md) 导出或导入；Git 操作按当前授权执行 |

不在每次启动时加载所有记忆。读取的历史资料用作背景和证据，当前用户指令决定接下来做什么。

## 保存与更新

以下是写法示例，内容不会自动保存：

```sh
"$ENGRAM_BIN" save '权限改造的交接现场' \
  '目标：调整鉴权入口。当前范围：仅 IAM 与 Admin。状态：仅完成设计阅读，代码尚未开始。下一步：确认接口改动位置。来源：本次任务约束，待接收方结合现场确认。' \
  --project work-risk-platform \
  --topic handoff/permission-refactor

"$ENGRAM_BIN" search '权限改造' --project work-risk-platform --limit 5
```

写入边界以 [engram-memory](skills/engram-memory/SKILL.md) 为权威。首轮统一使用默认 `scope=project`，通过显式 `--project` 区分空间；`personal` 不代表隐私边界或自动加载。更新时沿用相同 project、scope、topic，提交完整新结论；Engram 保留旧版本，不等于自动提炼。需要整理或纠错时显式选择小范围 [复核流程](skills/engram-memory/references/review.md)，不常驻扫描全部记忆。

CLI 搜索只返回截断内容；Agent 需要完整正文时使用 MCP `mem_get_observation`，人可以用 `tui`。跨机器先重新搜索，使用该机器返回的记录 ID。

## 配合知识库

续接工作或调用实际经历中的经验时检索相关记忆；查询原理或资料时直接用 `fengdi-kb-agent` 读取原文，查询本身不自动写入记忆。知识库继续使用它自己的路径、索引和笔记管理功能。

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

官方参考：[Git Sync](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/DOCS.md#git-sync-chunked)、[按需读取与 topic](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/docs/ARCHITECTURE.md)、[scope 的同步边界](https://github.com/Gentleman-Programming/engram/blob/v3.7.0/docs/TEAM-USAGE.md)。设计参考：[Anthropic 的 Agent 记忆组成](https://www.anthropic.com/research/components-of-agent-memory)，本仓库只落实经历学习与显式小范围纠错，不照搬其存储层次或后台机制。
