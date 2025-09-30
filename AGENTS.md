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
