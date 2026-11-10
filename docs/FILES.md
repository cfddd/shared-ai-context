# 文件归属

本次正式产物统一以 `/Users/luckincoffee/Projects/ExploreAI/shared-ai-context` 为源目录：

- `skills/install-shared-ai-context/SKILL.md`：安装 CLI 与配置环境。
- `skills/shared-ai-context/SKILL.md`：五项原子操作与命令示例。
- `skills/README.md`：具体用法及未来独立编排的扩展约定。
- `README.md`：项目说明与 Skill 入口。

KISS 与 root 仅领导协调的规则见 `AGENTS.md`；本轮 Skill 由用户自行验收的范围及单向职责见 `skills/README.md`，不另建一套规则。

项目外保留的文件各有独立用途：

- `~/.codex/skills/`、`~/.cursor/skills/`、`~/.qoder/skills/` 下的两份同名 Skill 是宿主安装副本，正式源文件仍在本项目 `skills/`。
- `~/.codex/memories_v2/extensions/ad_hoc/notes/2026-11-09-shared-ai-context-kiss.md` 是平台记忆副本，保留在平台要求的位置。
- `/private/tmp/shared-ai-context-skills-20261109-d808e18/` 与 `/private/tmp/shared-ai-context-team-20261109-075289e1/` 是旧工作副本、废弃草稿及临时实验材料，不是本次交付；保持原状，不迁入正式源码。

本次未从临时目录搬入旧多源 Skill、长评审记录、虚拟环境、缓存、测试数据库或 Git worktree 元数据，也未删除外部历史和安装副本。没有运行功能验证。
