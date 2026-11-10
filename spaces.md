# 记忆空间与主题

空间表示合作或任务归属，对应 Engram 的 `project`；可以跨仓库，也可以与代码无关。主题表示下一位 Agent 需要接续的具体对象，对应现有 `topic_key`（CLI 的 `--topic`）。先按 [记忆写入准入](skills/engram-memory/SKILL.md) 选择内容，再定位空间和主题；命名不构成保存理由。

## 空间

下表是可读约定，不预先创建空项目，不作为程序注册表。

| project | 用途 | topic 示例 |
| --- | --- | --- |
| `personal` | 尚未固化进规则、需要跨任务延续的协作纠正 | `context/collaboration-correction` |
| `learning` | 当前学习的卡点、已尝试路线和续接状态 | `handoff/java-transactions` |
| `work-risk-platform` | 跨仓库任务的范围、执行状态和未固化取舍 | `handoff/permission-refactor` |
| `shared-ai-context` | 本项目的协作背景、当前任务和用途纠正 | `context/memory-purpose` |

读写明确指定 project。首轮统一默认 `scope=project`；`personal` 空间不会自动加载，也不提供隐私隔离。多个空间可以存放在同一个本机数据库中。

## 主题

新内容优先采用下面两种命名。前缀只是可读约定，不是新字段、真实目录、知识分类或强制枚举；不要求与 `--type` 一一对应，也不预建空记忆。

| 主题 | 用途 | topic 示例 |
| --- | --- | --- |
| `handoff/<任务名>` | 完整维护一项任务的合作现场与下一步 | `handoff/permission-refactor` |
| `context/<具体协作事项>` | 少量跨会话延续、尚未固化的增量背景 | `context/memory-purpose` |

### 粒度与命名

Agent 从当前任务和已有记忆中定位或复用主题，用户不必填写 topic；能确定归属时直接选择，仅有实质歧义才询问。按能否独立变化、独立读取决定粒度，内容实际变杂后再拆。

已有其他前缀的主题只要内容满足准入约定，仍可复用，不按名字机械删除或重命名。日期、Agent 名和会话 ID 通常放在正文或引用里。空间和前缀不产生自动继承或批量读取关系。

### 更新与交接

更新已有主题时沿用相同 project、scope、topic，提交整理后的完整新结论：保留仍有效的事实和适用条件，修正过时内容，标明尚未确认的部分。不能只追加一句补充而丢掉原先仍有效的内容；Engram 会保留旧版本，版本保留不等于自动提炼。

同一任务优先在一个 `handoff` 主题维护完整现场；已有 `progress` 若已承担此职责可沿用，其他主题只保留必要引用，避免双份状态逐渐不一致。多个 Agent 按实际协作对象分工，再由一个汇总者整理共同交接。

空间与知识库无需一一对应。引用知识时使用工具名、domain 和相对笔记路径；路径解释与原文维护交给 `fengdi-kb-agent` 自己的配置。
