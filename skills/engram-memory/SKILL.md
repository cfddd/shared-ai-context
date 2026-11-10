---
name: engram-memory
description: 用户明确要求记住、回忆或更新某个主题时，使用 Engram 读写精简记忆。任务交接用 engram-handoff，跨机器同步用 engram-sync。
---

# Engram 记忆操作

使用已配置的 `ENGRAM_BIN`、`ENGRAM_DATA_DIR`。缺少配置时，先按记忆仓库 README 的环境配置处理，再操作；安装和环境排查不属于本 Skill。

## 选择空间与主题

按用户指定的空间操作，例如 `work-risk-platform`、`learning`、`personal`；没有明确归属时先确认。`personal` 是空间名，所有空间统一使用默认 `scope=project`。

一个主题使用稳定的 topic，如 `decision/storage`、`preference/collaboration`。更新前先定位已有记忆，沿用原 topic，提交整理后的完整结论。保存工具成功返回的引用，不把旧的数字 ID 当成跨机器标识。

## 读取

优先调用已配置的只读 MCP 工具，参数示例：

```text
mem_search({"project":"work-risk-platform","query":"SQLite","limit":5})
mem_get_observation({"id":42})
```

第二步的 ID 取自本次搜索结果，读取前确认结果属于所选空间。需要前后经过时再调用 `mem_timeline`；不知道已有空间名时调用 `mem_list_projects`。按需读取候选，不批量加载全部记忆。

CLI 可用来定位：

```sh
"$ENGRAM_BIN" search "SQLite" --project work-risk-platform --limit 5
```

CLI 搜索会截断正文，当前没有 `get` 子命令；需要完整内容时使用 MCP 的 `mem_get_observation`，人工浏览可用 `"$ENGRAM_BIN" tui`。

## 保存或更新

仅在用户明确要求记住或更新时写入。保存下次仍有价值的结论，注明适用范围、必要依据和未确认事项；原始工具输出留在原处。

```sh
"$ENGRAM_BIN" save "存储方案" \
  '结论：使用本地 SQLite。原因：单人、本机使用。依据：相关设计文档。' \
  --project work-risk-platform --type decision --topic decision/storage
```

同一空间与 topic 再次保存会修订该主题，Engram 仍保留旧版本。保存个人偏好也明确传空间：

```sh
"$ENGRAM_BIN" save "协作偏好" '偏好简洁实现，避免提前抽象。' \
  --project personal --type learning --topic preference/collaboration
```

上例为用法示意，实际内容以用户当前要求为准。报告真实返回结果，保存失败时保留待保存内容并说明原因。

需要原文依据或详细知识时，按 [知识库配合约定](references/knowledge.md) 调用现有知识库。
