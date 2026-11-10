# 本轮团队记录

日期：2026-11-10。仓库搭建和首次骨架发布已完成。**本轮合作上下文职责已收紧，A/B 增量静态复审通过，两个 Skill 的安装副本已同步，一条用户授权的真实记忆已保存；本轮未提交或推送。** 宿主加载与完整用户场景尚未验收；知识库保持独立。当前产品范围见 [003 规格](../specs/003-engram-memory/spec.md)。

## 所有权与工作副本

| 角色 | 路径与所有权 |
| --- | --- |
| root | 只协调、冻结契约与汇报，不代写实现或验证 |
| Worker A | 本轮在 canonical 修改 README、AGENTS、spaces、003 规格和本记录中受影响的说明；不改 Skill 或写记忆 |
| Worker B | 本轮修改 Skill 及安装副本；候选通过后执行用户授权的一条真实记忆保存，不改知识库 |
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

## 实际进度

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

## 本轮职责收紧

| 项目 | 状态 |
| --- | --- |
| A 文档 | 已收紧为合作现场；空间按合作归属，topic 优先任务交接或少量跨会话上下文，增量静态复审通过 |
| B Skill 与安装副本 | 两个改动 Skill 全目录已同步到三个客户端，共 6 个目录，无独立用户改动被覆盖；`engram-sync` 未改。公式仅在记忆主 Skill 一处维护 |
| 增量只读评审 | A/B 候选均已静态复审通过，无剩余必修问题 |
| 用户授权的真实记忆 | B 在候选通过后实际保存成功，CLI 退出 0：本机记录 `#1`，标题“记忆仓库定位：恢复合作现场”，project=`shared-ai-context`，topic=`context/memory-purpose`。未导出或发布，跨会话效果未验收 |

仅记录实际执行。历史环境核对不替代场景验收；本轮不运行测试、lint、Skill 验证器、产品烟测或跨机器演示，不写测试条目。用户明确授权的一条真实记忆由 B 执行，结果按工具实际返回记录。
