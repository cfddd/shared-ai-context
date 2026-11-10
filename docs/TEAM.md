# 本轮团队记录

日期：2026-11-10。状态：**A/B 分别静态复审与最终整合只读评审均已通过，三个 Skill 已安装到三个客户端；用户随后明确授权推送代码，Git 交付进行中。** 宿主加载与用户场景尚未验收；知识库保持独立。当前产品范围见 [003 规格](../specs/003-engram-memory/spec.md)。

## 所有权与工作副本

| 角色 | 路径与所有权 |
| --- | --- |
| root | 只协调、冻结契约与汇报，不代写实现或验证 |
| Worker A | `.worktrees/memory-repo`（`codex/memory-repo`）；README、AGENTS、spaces、规格、团队记录、忽略规则与旧实现退役；独占主目录最终整合 |
| Worker B | `.worktrees/memory-environment`（`codex/memory-environment`）；三个 Skill、环境文件、Engram 数据目录与客户端配置、安装副本及旧入口退役 |
| Reviewer | 只读评审 A、B 和最终整合；修复交回 owner，不运行测试或改文件 |

工作副本都在项目目录内，基线为 `9f73af9af9564576d98ea1b5ed92e632bfd2d4e8`。各 owner 只修改自己的文件；跨所有权调整先由 root 协调。A 在分别评审完成后已复制指定产物整合，不以 commit/merge 代替文件归属；本次 Git 交付由 A 负责。

旧 CLI 的本地标签 `sctx-v0.2.0` 已指向上述基线。没有覆盖标签、改写 Git 历史或删除旧数据库。原先 001/002 的团队和验收历史可通过标签查阅，不沿用为本轮验收证据。

## 冻结契约

- canonical 仓库：`/Users/luckincoffee/Projects/ExploreAI/shared-ai-context`。
- 环境文件：`.local/engram.env`；`ENGRAM_BIN` 指向 `/opt/homebrew/bin/engram`，`ENGRAM_DATA_DIR` 指向 canonical 仓库的 `.local/engram`，`ENGRAM_REPO` 指向 canonical 仓库。`ENGRAM_REPO` 是本仓库约定而非官方参数；Shell 通过 `~/.zshenv` 加载，MCP 显式使用相同数据目录。不设置全局 `ENGRAM_PROJECT`。
- project 是空间名，默认 `scope=project`；包括 `personal` 空间，不做隐私或继承承诺。
- 六个只读 MCP 工具与三个 Skill 的职责以 003 规格为准，直接使用 Engram，不接入官方自动保存 hooks。
- `fengdi-kb-agent` 的配置、原文与索引不属于本轮修改范围。
- 当前 `origin` 仍为公开的 `https://github.com/cfddd/shared-ai-context.git`。搭建阶段未提交或推送；2026-11-10 用户随后明确要求“推送代码”，授权将仓库骨架、文档、三个 Skill 与旧源码退役提交并正常推送。此授权不包含数据库、备份、用户配置或真实记忆导出；不创建远程、不改变可见性、不强推。

## 实际进度

| 项目 | 状态与证据 |
| --- | --- |
| 起始主目录 | `main`，工作区干净，HEAD 为上述基线 |
| CLI 保留点与隔离 | A 已创建本地标签及 A/B 两个 worktree |
| 本机 Engram | B 已发现安装版本 `3.7.0`；原默认库的 observations、sessions、user_prompts 为 0，原库保留 |
| A 交付 | 文档与旧实现退役候选已编写；Reviewer 首轮要求区分旧 sctx 数据与已有 Engram 数据，owner 已修复，独立静态复审通过 |
| B 数据与 Shell | 已用 SQLite backup API 将原默认 Engram 库一致性复制至 `.local/engram/engram.db`；原目录保留，未写测试记忆。已创建环境文件及 `~/.zshenv` 的短 source 块 |
| B 客户端配置 | Codex 原位收窄已有 Engram MCP，Cursor / Qoder 新增同一可执行文件、数据目录和六个只读工具；未调用官方 setup，未安装主动保存 hook 或 HTTP 常驻服务 |
| B 本机记录与备份 | `.local/environment.md` 记录落地状态；原配置备份为 `.local/backups/20261110-engram/`，均留本机，不提交 |
| B Skill | 四个文件已整合；三个 Skill 全目录安装到 Codex、Cursor、Qoder，共 9 个目录。旧两个 Skill 的 6 个副本与旧版原文匹配，已完整备份到 `.local/backups/20261110-engram/retired-skills/` 并退役，无用户改写副本 |
| A/B 分别评审 | 两个 worker 分别静态评审已通过；实际客户端运行和用户验收未执行 |
| 主目录整合与最终评审 | A 已按 owner 清单整合 A 的 6 份文件、B 的 4 份文件，退役 17 份旧跟踪文件，保留 `.local/` 与 `.worktrees/`；Reviewer 已读 canonical 产物、实际配置及 9 个安装副本，最终整合只读评审通过，无新的必修问题 |
| 用户自验 | 全部未执行 |
| 本次 Git 交付 | 用户已授权上述非敏感候选，A 正在执行；具体提交 SHA、推送结果与远端引用以交付报告为准，不在本文预记成功 |

仅记录实际执行。版本读取、现有文件/数据库的只读核对属于环境配置事实，不替代场景验收。本轮没有运行测试、lint、Skill 验证器、产品烟测、跨机器演示，也不写测试记忆。
