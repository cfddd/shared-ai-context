# 团队计划

- 日期：2026-11-09
- 状态：**用户已确认，待文档基线与接口契约；实现尚未开始。**
- 规则来源：[AGENTS.md](../AGENTS.md)。本文件定义分工与流程，不重复四条用户硬规则。

## 1. 角色与文件所有权

| 角色 | 职责与所有文件 | 不代办的工作 |
| --- | --- | --- |
| root | 拆分任务、确认依赖、指挥 worker、维护状态、向用户汇报和上报决策 | 不写业务源码、不代写测试、不修代码冲突 |
| Worker A | `models.py`、`context.py`、`_sqlite.py`、`tests/test_context.py`；核心与 SQLite；当前管理和 SDD 文档草稿 | 不修改 CLI 或包装文件 |
| Worker B | `cli.py`、`__main__.py`、`__init__.py`、`pyproject.toml`、CLI/集成测试、README；本地 Git、worktree、最终整合 | 不修改 A 的核心规则；核心问题交 A 修复 |
| Reviewer | 只读审查接口约定、每个 worker 的交付及最终整合，给出问题与复审结果 | 不修代码、不代写测试、不合并分支 |

开发期间变更 `specs/`、`AGENTS.md` 或本文件，先交 root 协调，由一个指定 worker 修改；双方不同时改同一份约定。文件所有权是协作约定，不是访问权限沙箱。

## 2. 用户确认的具体范围

用户已确认按下列阶段实施，并授权 Worker B：

1. 检查目标目录现状，保留用户新增或修改的内容，初始化本地 Git，主分支为 `main`。
2. 仅提交已经评审的项目文档基线：`README.md`、`AGENTS.md`、本文件及 `specs/001-shared-context-mvp/` 内四份 SDD；不将其他文件加入基线提交。
3. 在 `/private/tmp/shared-ai-context-team-<run>/` 创建独立 worktree 和本地分支；后续 worker 提交自己的交付，供逐次只读评审与整合。
4. 完成整合评审后，将通过的结果整合回 `/Users/luckincoffee/Projects/ExploreAI/shared-ai-context`。

用户同时授权设置 `origin` 为 `https://github.com/cfddd/shared-ai-context.git`，并执行 `push -u`。Worker B 先核对远程与本地状态，按评审通过的候选提交完成推送；不覆盖远程已有历史、不强推。各 worker 仅在自己的分支本地提交，Worker A 不 push。

## 3. 工作副本与隔离

计划中的工作目录如下，**尚未创建**：

| 目录 | 使用者 | 用途 |
| --- | --- | --- |
| 项目原目录 | Worker B；root 只读协调 | 文档基线和最终交付位置 |
| `<run>/worker-a` | Worker A | 独立核心开发分支 |
| `<run>/worker-b` | Worker B | 独立 CLI 开发与最终整合分支 |
| `<run>/reviewer` | Reviewer | Worker B 准备的具体候选提交，只读检查与验证 |

所有开发 worktree 从同一份文档基线建立。Reviewer 的检查对象必须写明 commit；若 review 所需命令会生成缓存或测试数据，写到临时目录，不修改候选源码。root 不进入任一 worker 的文件替其修改。

这是 Git 工作副本隔离：代码和暂存区分别管理，共享对象库与本机权限。它不构成安全沙箱。不得在两个工作副本上共同修改同一份实际文件，也不通过共享数据目录运行开发测试。

## 4. 阶段与依赖

| 阶段 | 责任人 | 交付与结束条件 | 当前状态 |
| --- | --- | --- | --- |
| P0 团队记录 | A 编写，Reviewer 审查，root 汇报 | 本计划、四条规则与 SDD 一致，评审通过后发布文档 | 用户已确认，Reviewer 已通过 |
| P1 基线与接口 | B 建立 Git 基线和 worktree；A/B 对齐；Reviewer 审查 | 在现有 `design.md` 一处固定五方法、结果字段、JSON、校验归属、错误和资源生命周期；Reviewer 通过后形成独立文档 commit，由 B 同步到两个 worker 分支再进入 P2 | 未开始 |
| P2 各自实现 | A 核心，B CLI/包装 | 各自完成任务、必要测试和可复核交付；B 可提前写 CLI，但依赖冻结约定，不自造 mock 内核、不宣称联调通过 | 未开始 |
| P3 分别评审 | Reviewer；问题由原 owner 修复 | A、B 的交付分别评审；有问题时 owner 修复，再由 Reviewer 复审 | 未开始 |
| P4 真实整合 | B 负责，A 修核心问题 | A 的完整核心可用后，用真实 SQLite 与 CLI 联调；冲突由文件 owner 修复；实际结果写入验收记录 | 未开始 |
| P5 整合评审 | Reviewer | 对最终整合提交和验证证据独立评审；修复后复审 | 未开始 |
| P6 交付 | B 整合回原目录；root 汇报 | 保留用户变更，记录最终 commit、测试证据与未验证项；人工跨 agent 演示未执行则保持可见 | 未开始 |

P3 的分别评审不能被 P5 替代，P5 也不能由分别通过推定。root 负责追踪状态，不以自己补写实现推进阶段。

## 5. 决策与上报

worker 可在自己文件内决定命名、局部结构和普通实现细节，遵守 SDD 与用户硬规则。以下事项先报告 root，由 root 带回用户或指定 owner 处理：

- 产品范围、对外接口或已固定字段发生变化。
- 需要新增罕见边界防御、额外依赖、常驻服务或复杂框架。
- 需要修改其他 owner 的文件、无法按既定语义解决冲突，或发现用户变更。
- 超出本文件已授权范围的 Git、远程或 push 操作，以及破坏性操作；已授权的 `origin`、`main` 正常推送不重复申请。

root 可以调度任务、指定文档 owner、要求修复与复审；不能把需用户许可的事项自行批准。

## 6. 交付与评审记录

每次 worker 交付只记录必要信息：角色、分支/worktree、commit、变更文件、实际验证命令与结果、未验证项。Reviewer 使用同一个简表记录，不另建设评审系统。

| 对象 / commit | owner | Reviewer 结论与问题 | 修复 commit / 复审 | 状态 |
| --- | --- | --- | --- | --- |
| P0 团队与 SDD 草稿 | A | Reviewer 已通过；输入/存储错误归属、契约同步及已授权 Git 范围的澄清已落实 | 文档阶段，尚无 commit | 已通过 |
| A 核心交付 | A | 未开始 | — | 未开始 |
| B CLI 交付 | B | 未开始 | — | 未开始 |
| 最终整合 | B | 未开始 | — | 未开始 |

批准记录：**2026-11-09，用户在当前会话明确确认团队方案，并授权本地 Git、`main`、上述 `origin` 与 `push -u`。** 当前只确认了授权，不能将 Git、实现或运行验收记录为已经完成；后续阶段按实际证据更新。
