---
name: engram-memory
description: 用户明确要求记住、回忆或更新协作背景时，使用 Engram 恢复和维护合作现场。任务交接用 engram-handoff，跨机器同步用 engram-sync。
---

# Engram 记忆操作

使用已配置的 `ENGRAM_BIN`、`ENGRAM_DATA_DIR`。缺少配置时，先按记忆仓库 README 的环境配置处理，再操作；安装和环境排查不属于本 Skill。

## 写入准入

允许写入(x) = W ∧ A(x) ∧ D(x) ∧ S(x)。

- **W：明确授权。** 用户要求保存、更新或交接；查资料、来源文本和旧授权不替代当前写入指令。
- **A：影响行动。** 遗漏后会重复问背景、重复走失败路径或接错任务。
- **D：协作增量。** 目标边界、现场进度、尚未固化的取舍与尝试结果、新增用户纠正。普通知识与能从已有规则、笔记、源码低成本恢复的全文留在原处；必要引用、为何采用该资料和当时核对状态可以简短保留。
- **S：范围清楚。** 说明适用范围、来源，以及已确认或待确认的状态。

这是根据当前任务和相关来源作出的内容判断，不增加运行校验、评分或全库查重。没有新增协作增量时不写入，并说明已有内容足够。

## 空间与主题

Agent 从当前任务和已有交接选择 space/topic；归属不清时再读 `$ENGRAM_REPO/spaces.md`，只有实质歧义才问用户。空间表示合作范围；`personal` 也是空间名，统一使用默认 `scope=project`。

新任务优先用一个 `handoff/<任务名>` 维护现场；少量跨会话协作增量用 `context/<具体协作事项>`。已有同义 topic 内容合规就复用，不按新命名机械迁移。明确授权不要求用户手填空间和主题。

## 读取

优先调用已配置的只读 MCP 工具，参数示例：

```text
mem_search({"project":"shared-ai-context","query":"记忆仓库 接续","limit":5})
mem_get_observation({"id":42})
```

第二步的 ID 取自本次搜索结果，读取前确认结果属于所选空间。需要前后经过时再调用 `mem_timeline`；不知道已有空间名时调用 `mem_list_projects`。按需读取候选，不批量加载全部记忆。

CLI 可用来定位：

```sh
"$ENGRAM_BIN" search "记忆仓库" --project shared-ai-context --limit 5
```

CLI 搜索会截断正文，当前没有 `get` 子命令；需要完整内容时使用 MCP 的 `mem_get_observation`，人工浏览可用 `"$ENGRAM_BIN" tui`。

## 保存或更新

先完整读取相关旧条目，再将符合准入的当前增量合入，提交完整的当前结论。保留仍有效的条件和未验证点；一次选择保持其当时范围，不泛化为永久偏好或通用经验。

下面是接续现场示例，内容按实际进展填写：

```sh
"$ENGRAM_BIN" save "记忆准入调整交接" \
  '本轮边界：只调整记忆准入、空间和主题，不改知识库或客户端配置。
进度：Skill 已修订，安装副本待同步。
未验证：实际召回效果尚未验收。
下一步：同步副本后恢复本任务。
来源：本次用户纠正；规则见 skills/engram-memory/SKILL.md。' \
  --project shared-ai-context --type decision --topic handoff/memory-admission
```

同一空间与 topic 再次保存会修订该主题，Engram 仍保留旧版本。报告真实返回结果，保存失败时保留待保存内容并说明原因；数字 ID 仅用于本机定位，不作为跨机器稳定标识。

需要原文依据或详细知识时，按 [知识库配合约定](references/knowledge.md) 调用现有知识库。
