# task202509270946-todolist-rule-update

## Summary
- Add a structured task workflow using `z-todolist`, with per-task IDs, a running checklist in `_todolis.md`, and a per-task execution log file. Persist the rules in `AGENTS.md` and follow them for all future work.

## Original Request
后续开发任务处理规则重大更新：我在项目中，创建了一个文件夹'z-todolist'，里面的主要文件是_todolis.md，每次我发布任务后，你首先要增加一个任务项'task202509270946-**'，其中'**'为任务的大致内容，需要你总结精简这个名称，然后，先把我的需求原文列出来，然后，理解需求后，分解为工作任务，把工作任务细化为列表清单，然后按照列表清单每一次独立执行，每一个列表项，最前面，都需要有方框[]，空方框表示未完任务，[x]方框表示完成任务。列完任务后，就可以逐个执行，直至任务完成。除了在文档_todolis.md中列出所有任务外，还需要生成一个和任务名称对应的任务执行文件，文件命名为'task202509270946-**.md',需要把完成这个任务的所有工作内容，都写入这个文件夹，做工作任务流程备忘。将上面这个规则写入AGENTS.md，后续所有工作内容，都需要严格执行。

## Environment
- Repo root: `/mnt/d/_projects/odoo.github.rainth888`
- WSL path mapping: `D:\\_projects\\...` ↔ `/mnt/d/_projects/...`

## Steps Executed
1. Chose task slug: `todolist-rule-update`.
2. Updated `AGENTS.md` with a new section “Task Workflow (z-todolist)” describing the procedure.
3. Created `z-todolist/_todolis.md` and added this task with original request and a checkbox checklist.
4. Created this execution log file.

## Files Changed
- `AGENTS.md` — added “Task Workflow (z-todolist)” section.
- `z-todolist/_todolis.md` — initialized and recorded task checklist.
- `z-todolist/task202509270946-todolist-rule-update.md` — execution notes.

## Verification
- Open both `z-todolist/_todolis.md` and this file to confirm the workflow is documented.
- Future tasks will be added as `task<timestamp>-<slug>` entries with checkboxes updated as work proceeds.

## Follow‑ups
- None. Ready to apply the workflow to the next tasks.
