# 团队计划

- 日期：2026-11-09
- 状态：**A/B 分别评审、最终整合评审、真实联调与既有验收样本已完成。** B 遇到用量限制后，root 指定 A 承接剩余收尾文档与 Git 交付；具体最终提交与推送状态以 `main` / `origin/main` 及交付报告为准。
- 规则来源：[AGENTS.md](../AGENTS.md)。本文件定义分工与流程，不重复四条用户硬规则。

## 1. 角色与文件所有权

| 角色 | 职责与所有文件 | 不代办的工作 |
| --- | --- | --- |
| root | 拆分任务、确认依赖、指挥 worker、维护状态、向用户汇报和上报决策 | 不写业务源码、不代写测试、不修代码冲突 |
| Worker A | `models.py`、`context.py`、`tests/test_context.py`；核心与 SQLite；`design.md` 的接口契约；受 root 移交承接剩余收尾文档、整合与 Git | 收尾不修改已审业务源码 |
| Worker B | `cli.py`、`__main__.py`、`__init__.py`、`pyproject.toml`、CLI/集成测试、README；已完成前期 Git、worktree 与整合候选，用量限制后剩余收尾交 A | 不修改 A 的核心规则；核心问题交 A 修复 |
| Reviewer | 只读审查接口约定、每个 worker 的交付及最终整合，给出问题与复审结果 | 不修代码、不代写测试、不合并分支 |

开发期间变更 `specs/`、`AGENTS.md` 或本文件，先交 root 协调，由一个指定 worker 修改；双方不同时改同一份约定。文件所有权是协作约定，不是访问权限沙箱。

## 2. 用户确认的具体范围

用户已确认按下列阶段实施，并授权 Worker B：

以下操作原由 B 负责；root 的收尾移交将执行人调整为 A，Git 授权范围保持不变。

1. 检查目标目录现状，保留用户新增或修改的内容，初始化本地 Git，主分支为 `main`。
2. 仅提交已经评审的项目文档基线：`README.md`、`AGENTS.md`、本文件及 `specs/001-shared-context-mvp/` 内四份 SDD；不将其他文件加入基线提交。
3. 在 `/private/tmp/shared-ai-context-team-<run>/` 创建独立 worktree 和本地分支；后续 worker 提交自己的交付，供逐次只读评审与整合。
4. 完成整合评审后，将通过的结果整合回 `/Users/luckincoffee/Projects/ExploreAI/shared-ai-context`。

用户同时授权设置 `origin` 为 `https://github.com/cfddd/shared-ai-context.git`，并执行 `push -u`。最终 Git owner 先核对远程与本地状态，按评审通过的候选提交完成正常推送；不覆盖远程已有历史、不强推。各 worker 的实现只在自己的分支提交；最终 `main` 推送由当前收尾 owner A 统一执行。

## 3. 工作副本与隔离

工作目录已从同一文档基线 `590a324e495892ffe7952e96b89e1268673d77f9` 建立。`<run>` 为 `/private/tmp/shared-ai-context-team-20261109-075289e1`：

| 目录 | 使用者 | 用途 |
| --- | --- | --- |
| 项目原目录 | 前期 B，收尾 A；root 只读协调 | 文档基线和最终交付位置 |
| `<run>/worker-a` | Worker A | `codex/core`，独立核心开发分支 |
| `<run>/worker-b` | B 实现，A 接手剩余收尾 | `codex/cli`，独立 CLI 开发与最终整合分支 |
| `<run>/reviewer` | Reviewer | detached HEAD；由当前 Git owner 准备具体候选提交，只读检查与验证 |

所有开发 worktree 从同一份文档基线建立。Reviewer 的检查对象必须写明 commit；若 review 所需命令会生成缓存或测试数据，写到临时目录，不修改候选源码。root 不进入任一 worker 的文件替其修改。

这是 Git 工作副本隔离：代码和暂存区分别管理，共享对象库与本机权限。它不构成安全沙箱。不得在两个工作副本上共同修改同一份实际文件，也不通过共享数据目录运行开发测试。

## 4. 阶段与依赖

| 阶段 | 责任人 | 交付与结束条件 | 当前状态 |
| --- | --- | --- | --- |
| P0 团队记录 | A 编写，Reviewer 审查，root 汇报 | 本计划、四条规则与 SDD 一致，评审通过后发布文档 | 用户已确认，Reviewer 已通过 |
| P1 基线与接口 | B 建立 Git 基线和 worktree；A/B 对齐；Reviewer 审查 | 在现有 `design.md` 一处固定五方法、结果字段、JSON、校验归属、错误和资源生命周期；Reviewer 通过后形成独立文档 commit，由 B 同步到两个 worker 分支再进入 P2 | 已完成；契约 `739c6e8` 已通过并同步；文档基线远端 `main` 已核验 |
| P2 各自实现 | A 核心，B CLI/包装 | 各自完成任务、必要测试和可复核交付；B 可提前写 CLI，但依赖冻结约定，不自造 mock 内核、不宣称联调通过 | 已完成 |
| P3 分别评审 | Reviewer；问题由原 owner 修复 | A、B 的交付分别评审；有问题时 owner 修复，再由 Reviewer 复审 | A `1615d99` 与 B 修复后 `caa6e7e` 均已通过 |
| P4 真实整合 | B 负责，A 修核心问题 | A 的完整核心可用后，用真实 SQLite 与 CLI 联调；冲突由文件 owner 修复；实际结果写入验收记录 | 已完成；18 项测试、真实安装、文件换行修复及 AT-02/09 当前人工样本有证据 |
| P5 整合评审 | Reviewer | 对最终整合提交和验证证据独立评审；修复后复审 | 已通过，精确候选 `8fd78e7767af5937845860293bb089e45649fdee` |
| P6 交付 | A 承接收尾并整合回原目录；root 汇报 | 保留用户变更，记录最终 commit、测试证据与未验证项；人工跨 agent 演示未执行则保持可见 | A 对收尾文档取得 delta 评审后，快进 `main`、正常 push 并核验远端；实际最终 SHA 由 Git 与交付报告给出，不预记推送结果 |

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
| P0 团队与 SDD 草稿 | A | Reviewer 已通过；输入/存储错误归属、契约同步及已授权 Git 范围的澄清已落实 | 已发布至文档基线 `590a324` | 已通过 |
| 文档基线 `590a324` | B | 内容为 P0 已审的七份文档；`git diff --cached --check` 通过，提交后本地 main 干净 | 已正常 `push -u`；远端 `main` 为完整相同 SHA | 已完成 |
| P1 接口契约 `739c6e8` | A；B 对齐 | Reviewer 已在独立 worktree 审查通过，无必要修正；B 已快进同步相同 commit | 五方法、结果字段、错误归属和连接生命周期已固定 | 已通过 |
| A 核心交付 `1615d99` | A | Reviewer 静态审查与独立副本 10 项真实 SQLite 测试均通过，无必要修正 | 无 | 已通过 |
| B CLI `7f58310` → `caa6e7e` | B | 首轮发现文件 `read_text` 将 CRLF 转换为 LF；B 就近改字节读取再 UTF-8 解码，修改两个现有保留正文用例 | Reviewer 在 `caa6e7e` 复审及 8 项既有 CLI 测试通过，无剩余必要问题 | 已通过 |
| 最终整合 `8fd78e7` | B | Reviewer 在干净独立副本同 SHA 审查通过；无源码变更、无证据偏差，30 个本地链接与围栏、5 份演示 JSON 检查通过 | 本次只补精确评审结论及完成状态，文档 delta 另确认，不重复实现测试 | 已通过 |

批准记录：**2026-11-09，用户在当前会话明确确认团队方案，并授权本地 Git、`main`、上述 `origin` 与 `push -u`。** 后续阶段按实际证据更新，不将文档提交计为功能完成。

Git preflight 与基线证据（2026-11-09）：

- 初始目录没有 `.git`，仅包含已审七份文档；使用现有 Git 作者配置建立 `main`，没有修改用户身份配置。
- GitHub 仓库 `cfddd/shared-ai-context` 已存在且为公开仓库；`git ls-remote --heads origin` 成功但没有分支，未覆盖已有历史，未修改可见性。
- `gh` 2.89.0 可用但未登录；现有 Git credential helper 虽已配置，未向 HTTPS 推送提供可用身份。
- 首次推送 35 秒超时后复查远端仍无分支；正常非 force 重试返回退出码 128：`fatal: could not read Username for 'https://github.com': terminal prompts disabled`。
- 用户完成本机 GitHub 登录后，B 复查远端仍为空，执行正常 `git push -u origin main` 成功；`git ls-remote --heads origin main` 核验为 `590a324e495892ffe7952e96b89e1268673d77f9`。

B 实施与验证证据（2026-11-09）：

- 已将通过评审的契约 `739c6e8` 与核心 `1615d99` 快进同步到 B 分支，未修改 A 的核心文件。
- `PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`：18 项通过（核心 10 项、CLI 8 项）；覆盖真实子进程、跨工作目录读取、输入错误、存储路径失败与两进程各一次写入。
- 临时虚拟环境使用现有 setuptools 执行 `pip install --no-index --no-build-isolation --no-deps -e <worker-b>` 成功；真实 `sctx --help` 和 JSON 创建会话通过，未联网安装依赖。
- 临时入口：`/private/tmp/shared-ai-context-team-20261109-075289e1/install-check/bin/sctx`。A 使用该真实入口写交接，Reviewer 读取确切引用并解释；AT-02 的无关任务与随后明确列表/读取序列也已完成，详见验收记录。
- CRLF 问题实际复现于文件输入，未声称 stdin 原先也有同样缺陷。修复没有新增异常分支或 helper；B 与 Reviewer 分别复跑现有 8 项 CLI 测试通过。
- AT-09 仅证明同一 Codex 宿主内两个独立 agent 的本次读写、解释和范围遵守；接收端已有项目背景，完全盲接续和其他宿主兼容未验证。
- 最终整合 `8fd78e7` 已独立评审通过。此后仅记录本次结论和实际完成状态，不回填本文件自身 commit，避免文档自引用循环；最终远端 HEAD 单独核验后向用户汇报。

收尾移交（2026-11-09）：B 因用量限制未完成最终 Git 交付，root 指定 A 接手。交接时主目录 `main` 干净且为文档基线 `590a324`；B 分支为已审 `8fd78e7`，只剩本文件、验收记录与任务清单三份收尾文档未提交。A 保留并续完这些修改，仅补评审结论、完成状态和实际 owner，不修改业务源码、不重复实现测试；Reviewer 另审该文档 delta 后再进行 Git 交付。root 继续只指挥和汇报。
