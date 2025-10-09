# 工作流与协作约定（z-todolist 规则）

本文件为本仓库内的代理协作规范，适用于仓库根目录及其子目录的全部工作范围。除非用户指令另有明确要求，所有任务均需严格遵守以下流程。

## 任务登记与命名
- 每次接收到新任务，必须先在 `z-todolist/_todolis.md` 中登记一个任务条目。
- 任务命名格式：`task<时间戳>-<简短摘要>`，例如：`task202509270946-init-todolist-rules`。
  - `<时间戳>` 为用户给定或任务开始时的时间标签（不改动用户给定值）。
  - `<简短摘要>` 需由代理基于任务内容进行简洁概括（英文或拼音短语更便于文件命名）。

## _todolis.md 内容要求
- 在 `z-todolist/_todolis.md` 中为每个任务新增一节，内容包含：
  - Original Request（原始需求原文）
  - 工作任务清单（Checklist）：
    - 以 `[]` 表示未完成、`[x]` 表示已完成。
    - 列表按最小可独立执行单元拆分。
- 列完任务后，逐项执行；每完成一项，回写 `[x]` 标记。

## 任务执行文件（每任务一档）
- 除了在 `_todolis.md` 登记外，必须创建与任务同名的执行文件：
  - 路径：`z-todolist/task<时间戳>-<简短摘要>.md`
  - 文件需包含以下章节：
    - Original Request
    - Improved English Phrasing
    - Technical Analysis
    - Steps
    - Files Changed
    - Apply / Verify
    - Next
    - 详细技术分析过程（Detailed Technical Analysis Process）
  - 同步对外说明：每次助理在会话中的“工作结果/变更说明/验证与注意事项”等总结性文字，需原样（或适当精炼）粘贴进任务文件，建议使用“Work Summary / 变更说明”小节，保证知识沉淀与可追溯。

## 执行与回写规则
- 执行顺序：严格按照 `_todolis.md` 的清单从上到下、逐项完成。
- 每次完成一项：
  - 在 `_todolis.md` 勾选该项为 `[x]`；
  - 如有重要细节或决策，补充到对应的任务执行文件中。
- 所有文件改动应最小化且紧扣任务本身，不扩展修复无关问题。

## 语言与格式
- `_todolis.md` 与任务执行文件以中文为主，可辅以简短英文术语。
- 文件、命令、路径、代码标识使用反引号包裹（如 `z-todolist/_todolis.md`）。

## 示例
- 新任务：整理规则并初始化清单
  - 任务名：`task202509270946-init-todolist-rules`
  - 在 `_todolis.md` 登记原始需求与清单；
  - 创建 `z-todolist/task202509270946-init-todolist-rules.md`，补充各章节内容；
  - 执行完成后，回写勾选清单项。

---

# Repository Guidelines

## Project Structure & Module Organization
- Core framework in `odoo/`; official addons in `addons/`; custom modules in `addons_custom/`.
- Typical module layout: `<module>/models`, `views`, `security/ir.model.access.csv`, `data`, `tests`, `__manifest__.py`.
- Config in `odoo.conf`; logs in `logs/`; docs in `doc/`; packaging in `debian/`; helper script `run.sh`.

## Build, Test, and Development Commands
- Create venv and install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run server (recommended): `python odoo-bin -c odoo.conf` or `./run.sh`.
- Update a module in-place: `python odoo-bin -c odoo.conf -u <module>`.
- Run module tests: `python odoo-bin -c odoo.conf -i <module> --test-enable --stop-after-init`.
- Database defaults (see `odoo.conf`): `127.0.0.1:5432`, user `proot`, password `proot`, db `odoo`.

## Coding Style & Naming Conventions
- Python 3, PEP 8, 4-space indentation; avoid one-letter names.
- Use snake_case for module and file names; model classes in CamelCase.
- Keep Odoo module structure and manifest fields consistent; name XML files descriptively (e.g., `sale_order_views.xml`).
- Linting via `flake8` (configured in `setup.cfg`). Run `flake8` locally before opening a PR.

## Testing Guidelines
- Place tests under each module’s `tests/` as `test_*.py` using `odoo.tests.common` (`SavepointCase`/`TransactionCase`).
- Tests must be deterministic; freeze time where needed (see `freezegun` in requirements).
- Run with `--test-enable --stop-after-init` to execute tests headlessly.

## Commit & Pull Request Guidelines
- Commit style: `[ADD|FIX|IMP|REF] module: short imperative summary` (e.g., `[FIX] sale: recompute unit price`).
- One logical change per commit; reference modules in scope.
- PRs: use `.github/PULL_REQUEST_TEMPLATE.md`; include context (before/after), linked issues, and screenshots for UI.
- Ensure `flake8` passes and module tests run locally; follow upstream Odoo contribution guidance.

## Security & Configuration Tips
- Do not commit real credentials; prefer env vars (e.g., `PGPASSWORD=...`).
- Keep `report.url`/`web.base.url` aligned with your access URL; ensure `wkhtmltopdf` path is valid.

## Task Workflow (z-todolist)
- For every new user task, create an ID: `taskYYYYMMDDHHMM-<slug>` where `<slug>` is a short summary.
- Record the task in `z-todolist/_todolis.md`:
  - Paste the original request.
  - Add a checklist of actionable steps using `[ ]` for pending and `[x]` for done.
  - Update the checklist status as each step is completed.
- Create a per-task log file `z-todolist/taskYYYYMMDDHHMM-<slug>.md` capturing:
  - Summary, assumptions, and environment notes.
  - The executed steps, commands, and files changed.
  - Any follow‑ups or verification notes.
- Keep changes minimal and safe; avoid breaking POS UI. Use WSL path mapping (`D:\_projects\...` → `/mnt/d/_projects/...`).
