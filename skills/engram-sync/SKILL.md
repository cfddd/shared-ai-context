---
name: engram-sync
description: 用户明确要求导出记忆、从 Git 拉取记忆或换机器同步时使用。负责 Engram Git Sync 与本次已授权的 Git 操作，不负责整理记忆内容。
---

# 记忆同步

使用已配置的 `ENGRAM_BIN`、`ENGRAM_DATA_DIR`、`ENGRAM_REPO`。最后一项是本仓库的定位约定，不是 Engram 官方参数。缺少配置时先按仓库 README 配置环境，再操作。`.local/` 是本机数据库，Git 管理 `.engram/` 中的清单及记忆内容分块。

## 本机导出

在记忆仓库根目录执行：

```sh
cd "$ENGRAM_REPO"
"$ENGRAM_BIN" sync --all
```

`--all` 包含所有空间，默认不包含原始 prompts。用户明确需要同步原始 prompts 时才加 `--include-prompts`。导出成功只表示本机同步文件已更新。

## 换机器或拉取远程记忆

当前机器已安装 Engram，并已将 `ENGRAM_DATA_DIR` 指向本机数据库。在记忆仓库根目录执行本次已授权的 Git 拉取，然后导入：

```sh
cd "$ENGRAM_REPO"
git pull --ff-only
"$ENGRAM_BIN" sync --import --all
```

首次使用先克隆已选定的记忆仓库，再执行导入。各机器的绝对路径可以不同；新会话中 MCP 和 CLI 应使用同一个本机数据库。

## 提交与推送

用户仅要求导出时，到导出完成为止。用户已明确授权本次提交或推送时，先看 `git status --short` 和目标远程，按授权执行对应操作，例如：

```sh
cd "$ENGRAM_REPO"
git add .engram
git commit -m "chore: sync memories"
git push
```

当前仓库原有远程是公开的 `cfddd/shared-ai-context`；真实记忆的远程存放位置尚未确定前，保持本地导出。不要把旧代码推送授权延伸为发布个人或工作记忆的授权。

首轮按一台机器结束后同步、另一台开始前导入使用。Git 合并发生冲突时保留现场并说明冲突，不自行丢弃任一侧数据。Git Sync 用于同步记忆内容，不承诺完整还原数据库中的所有本机状态。
