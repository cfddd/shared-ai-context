---
name: install-shared-ai-context
description: 安装 shared-ai-context 的 sctx CLI 并配置 SHARED_AI_CONTEXT_CLI、SHARED_AI_CONTEXT_HOME。用户要求安装，或操作 Skill 缺少这两项配置时使用。
---

# 安装与配置

只负责 CLI 安装和环境配置。源码使用用户指定的本地目录，或当前 shared-ai-context 项目；不清楚时询问源码路径。

在 Bash 或 Zsh 执行以下命令，将两个示例路径换成绝对路径。Python 版本应满足源码 `pyproject.toml` 的要求；已有项目 `.venv` 可直接用于安装。

```sh
REPO=/absolute/path/to/shared-ai-context
DATA_HOME=/absolute/path/to/shared-data

python3 -m venv "$REPO/.venv"
"$REPO/.venv/bin/python" -m pip install -e "$REPO"

export SHARED_AI_CONTEXT_CLI="$REPO/.venv/bin/sctx"
export SHARED_AI_CONTEXT_HOME="$DATA_HOME"

printf 'export SHARED_AI_CONTEXT_CLI=%q\nexport SHARED_AI_CONTEXT_HOME=%q\n' \
  "$SHARED_AI_CONTEXT_CLI" "$SHARED_AI_CONTEXT_HOME" \
  > "$REPO/.venv/shared-ai-context.env"
```

安装成功后，提供这两个变量的实际值和 env 文件的绝对路径。每个参与 agent 在自己的执行环境加载同一文件：

```sh
source /absolute/path/to/shared-ai-context/.venv/shared-ai-context.env
```

`SHARED_AI_CONTEXT_HOME` 是共享数据目录，数据库文件为其中的 `context.db`。可编辑安装依赖源码目录继续存在；env 文件也可放到用户指定的位置。只配置当前环境和该专用文件，不修改 shell profile。

安装失败直接报告实际命令和错误。此流程不升级源码、不修复系统环境，也不创建测试记录；后续工具操作交给 `shared-ai-context` Skill。
