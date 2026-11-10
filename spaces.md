# 记忆空间

Engram 的 `project` 表示工作归属，可以对应多个仓库、一个学习主题或个人背景。下表是可读约定，不预先创建空项目，不作为程序注册表。

| project | 用途 | topic 示例 |
| --- | --- | --- |
| `personal` | 协作偏好、长期目标、必要个人背景 | `preference/collaboration` |
| `learning` | 学习进度、困惑和学习方法 | `progress/java-transactions` |
| `work-risk-platform` | 跨 IAM、Admin、RiskReview 的工作经验与决定 | `decision/permission-flow` |
| `shared-ai-context` | 本仓库的使用决定与待办 | `decision/memory-workflow` |

读写明确指定 project。首轮统一默认 `scope=project`；`personal` 空间不会自动加载，也不提供隐私隔离。多个空间可以存放在同一个本机数据库中。

新增空间时使用稳定、可读的名字；已有主题沿用 topic，不把日期、Agent 名或会话 ID 放进长期主题名。任务交接可用 `handoff/<任务名>`，各 Agent 优先负责不同主题，再由一个汇总者整理共同交接。

空间与知识库无需一一对应。引用知识时使用工具名、domain 和相对笔记路径；路径解释与原文维护交给 `fengdi-kb-agent` 自己的配置。
