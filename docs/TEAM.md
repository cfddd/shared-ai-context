# 本轮团队记录

日期：2026-11-17。**本轮记忆证据锚点与四种复核结果约定已编写，A/B 增量与最终整合只读确认均通过，受影响 Skill 已同步三个客户端；用户自验未验收。** 本轮不操作实际记忆，不提交或推送。此前仓库搭建、骨架发布及 2026-11-10／11 的用途修订记录保留为历史，不能替代本轮行为验收。当前产品范围见 [003 规格](../specs/003-engram-memory/spec.md)。

## 所有权与工作副本

| 角色 | 路径与所有权 |
| --- | --- |
| root | 只协调、冻结契约与汇报，不代写实现或验证 |
| Worker A | 本轮在 canonical 只修改 003 规格和本记录；补充行为、自验场景和实际状态，不改 Skill 或操作记忆 |
| Worker B | 本轮只修改记忆主 Skill 与复核 reference，候选通过后同步 `engram-memory` 完整目录到三个客户端；保留安装副本独立用户修改，不操作实际记忆 |
| Reviewer | 只读评审 A/B 增量及职责一致性；修复交回 owner，不运行测试或改文件 |

初次搭建的隔离副本位于 `.worktrees/memory-repo` 与 `.worktrees/memory-environment`，基线为 `9f73af9af9564576d98ea1b5ed92e632bfd2d4e8`。A 在分别评审后按清单整合，首次 Git 交付已完成。本轮直接在 canonical 按文件所有权做小范围修改，保留既有内容，不另建工作副本；跨所有权调整先由 root 协调。

旧 CLI 的标签 `sctx-v0.2.0` 指向上述基线，已正常发布。没有覆盖标签、改写 Git 历史或删除旧数据库。原先 001/002 的团队和验收历史可通过标签查阅，不沿用为本轮验收证据。

## 冻结契约

- canonical 仓库：`/Users/luckincoffee/Projects/ExploreAI/shared-ai-context`。
- 环境文件：`.local/engram.env`；`ENGRAM_BIN` 指向 `/opt/homebrew/bin/engram`，`ENGRAM_DATA_DIR` 指向 canonical 仓库的 `.local/engram`，`ENGRAM_REPO` 指向 canonical 仓库。`ENGRAM_REPO` 是本仓库约定而非官方参数；Shell 通过 `~/.zshenv` 加载，MCP 显式使用相同数据目录。不设置全局 `ENGRAM_PROJECT`。
- project 表示合作或任务归属，由 Agent 结合现场定位，默认 `scope=project`；包括 `personal` 空间，不做隐私或继承承诺。内容准入仅由 [engram-memory](../skills/engram-memory/SKILL.md) 定义，空间和 topic 约定见 [spaces.md](../spaces.md)。
- 六个只读 MCP 工具与三个 Skill 的职责以 003 规格为准，直接使用 Engram，不接入官方自动保存 hooks。
- `fengdi-kb-agent` 的配置、原文与索引不属于本轮修改范围。
- 当前 `origin` 仍为公开的 `https://github.com/cfddd/shared-ai-context.git`。用户此前授权的仓库骨架、文档、Skill 与旧源码退役已以 `b9e2f8b` 正常推送，旧版标签也已发布；数据库、备份、用户配置与真实记忆未发布。本轮不提交、推送或导出记忆，不将旧发布授权延伸到真实记忆。

## 历史进度

| 项目 | 状态与证据 |
| --- | --- |
| 起始主目录 | `main`，工作区干净，HEAD 为上述基线 |
| CLI 保留点与隔离 | A 已创建本地标签及 A/B 两个 worktree |
| 本机 Engram | 初次搭建时 B 已发现安装版本 `3.7.0`；当时原默认库的 observations、sessions、user_prompts 为 0，原库保留 |
| A 交付 | 文档与旧实现退役候选已编写；Reviewer 首轮要求区分旧 sctx 数据与已有 Engram 数据，owner 已修复，独立静态复审通过 |
| B 数据与 Shell | 已用 SQLite backup API 将原默认 Engram 库一致性复制至 `.local/engram/engram.db`；原目录保留，未写测试记忆。已创建环境文件及 `~/.zshenv` 的短 source 块 |
| B 客户端配置 | Codex 原位收窄已有 Engram MCP，Cursor / Qoder 新增同一可执行文件、数据目录和六个只读工具；未调用官方 setup，未安装主动保存 hook 或 HTTP 常驻服务 |
| B 本机记录与备份 | `.local/environment.md` 记录落地状态；原配置备份为 `.local/backups/20261110-engram/`，均留本机，不提交 |
| B Skill | 四个文件已整合；三个 Skill 全目录安装到 Codex、Cursor、Qoder，共 9 个目录。旧两个 Skill 的 6 个副本与旧版原文匹配，已完整备份到 `.local/backups/20261110-engram/retired-skills/` 并退役，无用户改写副本 |
| A/B 分别评审 | 两个 worker 分别静态评审已通过；实际客户端运行和用户验收未执行 |
| 主目录整合与最终评审 | A 已按 owner 清单整合 A 的 6 份文件、B 的 4 份文件，退役 17 份旧跟踪文件，保留 `.local/` 与 `.worktrees/`；Reviewer 已读 canonical 产物、实际配置及 9 个安装副本，最终整合只读评审通过，无新的必修问题 |
| 用户自验 | 全部未执行 |
| 首次 Git 交付 | 已知提交 `b9e2f8b` 与标签 `sctx-v0.2.0` 已正常发布；本轮不重复远端检查或 Git 交付 |

## 历史实施记录（2026-11-11）

| 步骤 | Owner | 交付与当前状态 |
| --- | --- | --- |
| 调整用途、空间与主题说明 | A | 已完成现有五份文档的小增量，工作续接与经历中学到的可复用经验并存 |
| 调整准入与显式复核入口 | B | 已完成主 Skill 与相关 reference，公式只在主 Skill，详细流程只在 reference；未加调度器或存储层 |
| 增量只读评审 | Reviewer | A/B 候选分别静态评审通过，无剩余问题 |
| 安装与更新既有记忆 | B | `engram-memory` 完整目录已同步三个客户端共 3 个目录，无独立用户改动被覆盖；`handoff` / `sync` 未改。同 topic 保存退出 0，仍为本机 `#1`，标题“记忆仓库定位：续接与经历学习”，project=`shared-ai-context`，topic=`context/memory-purpose`，未新增条目 |

2026-11-10 的实际记录：A/B 增量静态复审已通过，两个改动 Skill 已同步三个客户端共 6 个目录；B 正式保存了本机 `#1`，project=`shared-ai-context`，topic=`context/memory-purpose`。2026-11-11 在这条记忆上修订，保留仍有效的来源背景，不把历史正文复制进团队记录。

历史用途记忆的保存与修订不代表跨会话效果或完整场景已验收，不能解释为本轮继续写入的任务。

## 本轮实施计划（2026-11-17）

| 步骤 | Owner | 交付与当前状态 |
| --- | --- | --- |
| 补充行为与五项用户自验 | A | 003 规格与本记录已编写，增量只读评审通过 |
| 补充证据锚点、读取规则和四种结论级复核结果 | B | 主 Skill 与复核 reference 已编写，增量只读评审通过，现有命令示例保留 |
| 分别审查 A/B 增量并确认最终整合 | Reviewer | A/B 增量与最终整合只读确认均通过，无剩余必修问题 |
| 同步受影响 Skill | B | `engram-memory` 全目录 3 个文件已同步 Codex、Cursor、Qoder，共 3 个目录，复制命令退出 0；写前与改前基线比较无独立用户修改，未运行验证器 |
| 用户执行五项新增自验 | 用户 | 未验收 |

详细规则集中在 [记忆主 Skill](../skills/engram-memory/SKILL.md) 和按需读取的 [复核纠错](../skills/engram-memory/references/review.md)。本轮沿用空间、topic、交接与同步约定，不新增数据库字段、状态机、归档删除操作或工具接口。

仅记录实际执行。本轮不运行测试、lint、Skill 验证器、产品烟测或记忆试写，不调用 Engram、批量迁移、写入、导出或发布实际记忆，不提交或推送。约定编写、安装副本同步、只读评审与用户行为验收分开记录。
