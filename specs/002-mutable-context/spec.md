# 002：可覆写的当前上下文（0.2）

日期：2026-11-10。用户已批准实施；本轮不运行测试、校验、评审、lint、编译、CLI 试跑或数据库烟测，不新增自动测试，不提交或推送。实现产物与实际验收分开记录，用户自验场景均保留未执行状态。

本规格是对 [001 规格](../001-shared-context-mvp/spec.md) 和 [001 设计](../001-shared-context-mvp/design.md) 的增量：新增可覆写的当前上下文，现有会话、历史记录及五个旧命令保持原义。001 中不提供覆盖、不建立 current 状态的限制仅适用于首版历史记录；本轮以用户批准的 002 行为为准。团队的旧评审、测试和提交步骤不适用于本轮，root 继续只指挥协调，A/B 按文件所有权实施。

## 行为

- 当前上下文由显式的 `scope` 与稳定主题名 `key` 唯一定位。`scope` 仅允许 `user`、`project:<非空标识>`、`task:<非空标识>`，不建立范围注册表，不隐式继承或合并范围。`key` 作为 SQLite 参数值处理，不解释为路径或 SQL。
- 每次 `put` 同时完整覆写 `summary` 与 `body`。同一 `scope/key` 只保留一份当前内容，后写生效，不自动摘要、截断、合并，也不自动留下历史。
- 当前上下文不从旧记录自动推导；不改写已有会话和记录。需要历史时，调用者显式使用原有 `write` 保存独立记录，其追加和稳定引用语义不变。
- 列表只返回指定范围的索引，默认最多 20 项，按 `key` 升序。默认读取只返回摘要，显式详情读取只返回正文，二者均带索引元数据。`put` 只返回索引元数据。
- 输入由 CLI 在入口校验一次；核心依赖已校验的 `scope`、`key`、`summary`、`body` 与正整数 `limit`，不重复校验。摘要和正文作为调用者提供的文本存储，工具不代写内容。
- 时间复用现有 UTC、含时区的 ISO 8601 字符串风格。不存在的当前文档抛出 `ContextNotFound`；CLI 映射为 `CONTEXT_NOT_FOUND`，退出码 1。SQLite 错误直接到达 CLI，沿用 `STORAGE_ERROR` 呈现，核心不捕获或包装。

## 核心接口与存储

以下结果从 `shared_ai_context.models` 导入，均为 `frozen=True` 的 dataclass：

| 类型 | 字段 |
| --- | --- |
| `ContextIndex` | `scope: str`、`key: str`、`updated_at: str` |
| `ContextSummary(ContextIndex)` | 索引字段，加 `summary: str` |
| `ContextDetail(ContextIndex)` | 索引字段，加 `body: str`；不继承 `ContextSummary`，不携带摘要 |

异常及方法在现有 `shared_ai_context.context` 中定义，不新增模块：

```python
class ContextNotFound(Exception): ...

Context.put_context(
    scope: str, key: str, summary: str, body: str
) -> ContextIndex
Context.list_contexts(scope: str, limit: int = 20) -> list[ContextIndex]
Context.get_context(
    scope: str, key: str, detail: bool = False
) -> ContextSummary | ContextDetail
```

`get_context` 按读取模式选择 SQL 字段：默认查询不读取 `body`，详情查询不读取 `summary`。列表查询也不读取摘要或正文。

在现有 `_SCHEMA` 中增加一张表，复用原连接生命周期、`CREATE TABLE IF NOT EXISTS` 和短事务：

```sql
CREATE TABLE IF NOT EXISTS contexts (
    scope TEXT NOT NULL,
    key TEXT NOT NULL,
    summary TEXT NOT NULL,
    body TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (scope, key)
);
```

`put_context` 使用 `INSERT ... ON CONFLICT (scope, key) DO UPDATE`，同次更新摘要、正文和时间，成功提交后返回 `ContextIndex`。不增加迁移版本、通用 repository、锁服务、自动历史表或第二份 Markdown 存储。

CLI 新增以下三个显式操作，版本为 `0.2.0`，旧五个命令不变：

```text
sctx context put SCOPE KEY --summary TEXT (--file PATH | --stdin) [--json]
sctx context list SCOPE [--limit N] [--json]
sctx context get SCOPE KEY [--detail] [--json]
```

CLI 使用现有数据库位置、JSON 成功外壳 `{"database_path": "绝对路径", "data": ...}` 及错误外壳；`data` 直接映射以上三类结果字段。文本 `get` 直接输出所选摘要或正文。入口输入错误沿用 `INVALID_INPUT`、退出码 2；存储错误沿用 `STORAGE_ERROR`、退出码 1，不增加特殊兜底。B 负责新增命令、README、原子操作 Skill 和版本。

## 实施任务

| 任务 | Owner | 状态 |
| --- | --- | --- |
| 固定本轮增量规格、接口和自验场景 | A | 已编写；未校验 |
| 为现有模型和 SQLite 核心增加三种结果、表与三个方法 | A | 已编写；未验证 |
| 准备项目内隔离副本，新增 CLI、Skill 用法、README 和 0.2 版本 | B | 已编写；未验证 |
| 将 A 指定源码整合回主目录，保留用户修改 | B | 已整合；未验证 |
| 用户执行以下五个自验场景 | 用户 | 未执行 |

工作副本和本轮产物放在项目内 `.worktrees/`；A 的核心实现仅在 `.worktrees/v02-core/` 修改，B 从 A 指定文件整合。本轮不通过提交和 merge 整合，不组织 Reviewer，不将文件已生成记作验收通过。

## 用户自验（全部未执行）

| 场景 | 操作 | 预期 | 状态 |
| --- | --- | --- | --- |
| 同一文档覆盖 | 对同一 `scope/key` 连续写两组摘要和正文，再列出并读取 | 列表仍为一项；摘要和正文均为第二次完整内容 | 未执行 |
| 三类范围隔离 | 在 `user`、`project:demo`、`task:demo` 写相同 `key` 的不同内容，分别列出和读取 | 各范围只返回自己的索引与内容，不继承其他范围 | 未执行 |
| 分级读取字段 | 对已有文档分别调用列表、默认读取和详情读取 | 列表只有 `scope/key/updated_at`；默认读取只加 `summary`；详情只加 `body` | 未执行 |
| 主题与写入顺序 | 在同一范围写两个不同 `key`，再对其中一个 `key` 连续覆写 | 不同主题互不影响；同一主题后写生效；列表按 `key` 排序 | 未执行 |
| 当前内容与显式历史 | 在已有会话中显式 `write` 历史，执行多次 `put`，再查看历史并读取原记录 | `put` 不自动新增历史；显式 `write` 仍追加独立记录，原记录和引用不变 | 未执行 |

以上为自验操作与预期，不代表已运行或通过；本轮代码行为、CLI 联调及旧功能回归均未验证。
