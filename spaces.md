# 记忆空间与主题

空间表示这条记忆属于哪项工作或生活领域，对应 Engram 的 `project`；可以覆盖多个仓库，也可以与代码无关。主题表示空间中可以独立读取、持续修订的稳定对象，对应现有 `topic_key`（CLI 的 `--topic`）。

## 空间

下表是可读约定，不预先创建空项目，不作为程序注册表。

| project | 用途 | topic 示例 |
| --- | --- | --- |
| `personal` | 协作偏好、长期目标、必要个人背景 | `preference/collaboration` |
| `learning` | 学习进度、困惑和学习方法 | `progress/java-transactions` |
| `work-risk-platform` | 跨 IAM、Admin、RiskReview 的工作经验与决定 | `decision/permission-flow` |
| `shared-ai-context` | 本仓库的使用决定与待办 | `decision/memory-workflow` |

读写明确指定 project。首轮统一默认 `scope=project`；`personal` 空间不会自动加载，也不提供隐私隔离。多个空间可以存放在同一个本机数据库中。

## 主题

主题可采用 `前缀/对象名`。下列前缀只是可选命名约定，不是新字段、真实目录或强制枚举，也不要求与 `--type` 一一对应。按实际内容选择即可，不预建空记忆。

| 类别 | 保存什么 | topic 示例 |
| --- | --- | --- |
| 偏好 `preference` | 协作方式、沟通习惯等持续偏好 | `preference/communication` |
| 背景 `background` | 后续判断经常需要的稳定目标或约束 | `background/learning-goal` |
| 决定 `decision` | 已选择的方案、理由和适用条件 | `decision/permission-flow` |
| 经验 `lesson` | 做过之后值得记住的发现与适用条件 | `lesson/travel-planning` |
| 做法 `workflow` | 已经用顺手、可以再次采用的简短步骤 | `workflow/note-review` |
| 进度 `progress` | 当前阶段、未解决事项和下一步 | `progress/java-transactions` |
| 交接 `handoff` | 让另一位 Agent 接续某项任务的必要状态 | `handoff/permission-refactor` |

### 粒度与命名

按能否独立变化、独立读取决定粒度。一条主题尽量围绕一个对象；先用能满足当前需要的名字，内容确实变杂后再拆。例如 `preference/collaboration` 同时容纳代码风格、沟通与 Git 习惯且经常分别修改时，再拆成 `preference/coding-style`、`preference/communication` 和 `preference/git-workflow`。

长期主题名保持稳定，日期、Agent 名和会话 ID 通常放在正文或引用里。空间相同也不自动建立主题层级：`decision/storage` 与 `decision/storage-backup` 只是两个可分别读取的名字。

### 更新与交接

更新已有主题时沿用相同 project、scope、topic，提交整理后的完整新结论：保留仍有效的事实和适用条件，修正过时内容，标明尚未确认的部分。不能只追加一句补充而丢掉原先仍有效的内容；Engram 会保留旧版本，版本保留不等于自动提炼。

同一任务的 `progress` 与 `handoff` 选择一处维护完整当前状态，另一处若确有需要只写用途说明和引用，避免双份状态逐渐不一致。多个 Agent 优先分别维护自己负责的主题，再由一个汇总者整理共同交接。

空间与知识库无需一一对应。引用知识时使用工具名、domain 和相对笔记路径；路径解释与原文维护交给 `fengdi-kb-agent` 自己的配置。
