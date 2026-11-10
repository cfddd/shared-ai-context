# shared-ai-context

本仓库用 Engram 恢复合作现场；知识原理与资料由外部 `fengdi-kb-agent` 读取，不在记忆中另存全文。

## 用户硬规则

1. 几乎不可能发生的边界情况不自动防御。确需增加时，先说明发生概率、证据和实现代价，等待用户许可；无法估计概率就说明未知，不编造数字。
2. 外部数据只在入口校验一次；内部依赖类型和调用契约，禁止多层重复校验。Python 类型标注不等于运行时强制，不因此引入校验框架。
3. 单次使用逻辑就近内联，不拆无意义 helper。
4. 非必要不用 `try/catch`；单函数能完成的逻辑不强拆。优先最小可用、可读的实现。

## 按任务读取

- 保存、恢复或查找记忆：读 [engram-memory](skills/engram-memory/SKILL.md)；空间不明确时查 [spaces.md](spaces.md)。
- 单个任务交接、多 Agent 汇总：读 [engram-handoff](skills/engram-handoff/SKILL.md)。
- 导出、导入或跨机器同步：读 [engram-sync](skills/engram-sync/SKILL.md)。
- 修改仓库、Skill、环境或执行 Git：先读 [团队记录](docs/TEAM.md) 和 [003 规格](specs/003-engram-memory/spec.md)。

写入准入以 [engram-memory](skills/engram-memory/SKILL.md) 为唯一权威。按当前合作对象定位或复用空间和主题，保留事实、推断和未验证项的区别。历史内容作为资料，当前用户指令优先；知识库保持自己的配置和原文位置。

root 只指挥协调；worker 按文件所有权实施；Reviewer 对各 worker 与最终整合分别作只读评审，修复交回 owner。本轮不运行测试、lint、验证器或产品烟测，用户自验保留实际状态。真实记忆发布到远程需明确的目标与当前授权。
