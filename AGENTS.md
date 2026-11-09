# shared-ai-context 协作规则

用户已确认团队方案；当前阶段与实际证据见 [团队计划](docs/TEAM.md)。按已审接口和文件分工实施，不将阶段批准视为所有工作已经完成。

## 用户硬规则（本节为项目内唯一权威）

1. 几乎不可能发生的边界情况不自动防御。确需增加时，先说明发生概率、证据和实现代价，等待用户许可；无法估计概率就说明未知，不编造数字。
2. 外部数据只在入口校验一次；内部依赖类型和调用契约，禁止多层重复校验。Python 类型标注不等于运行时强制，不因此引入校验框架。
3. 单次使用逻辑就近内联，不拆无意义 helper。
4. 非必要不用 `try/catch`（Python 为 `try/except`）；单函数能完成的逻辑不强拆。优先最小可用、可读的实现。

## 按任务读取

- 分工、开始实施、创建 worktree、执行 Git、提交评审或整合前，读取 [团队计划](docs/TEAM.md)，遵守批准状态和文件所有权。
- 修改产品行为前，读取 [规格](specs/001-shared-context-mvp/spec.md) 及受影响的 [验收场景](specs/001-shared-context-mvp/acceptance.md)。
- 修改接口、模块或持久化前，读取 [设计](specs/001-shared-context-mvp/design.md)；按 [任务清单](specs/001-shared-context-mvp/tasks.md) 更新实际进度。

产品行为由规格定义，实现选择由设计定义，团队流程由 `docs/TEAM.md` 定义。发现冲突先报告 root 并修正文档，不自行扩大实现范围。

root 只指挥和协调；worker 实现自己的内容，Reviewer 只读评审。每个 worker 的交付和最终整合均须分别评审，修复交回原 owner 后复审。未执行的验收保留未执行状态。
