# LiveOps Custom Agents Implementation Plan

> **Execution mode:** Inline in the current task; local artifacts first, then VNG AI Web UI.

**Goal:** Document and create ten least-privilege custom Agents supporting the LiveOps operating lifecycle.

**Architecture:** Each Agent owns one bounded workflow and begins read-only or draft-only. Knowledge Base access is allowlisted per Agent; because the CFL business KBs have not yet been audited, initial Web creation must not select `Tất cả kho tri thức` or bind an unaudited business KB.

**Surfaces:** Markdown artifacts in `agent/` and the integrated Codex browser at `https://vnggames.ai/kb/agents`.

## Global constraints

- Do not read, copy or store credentials, tokens, cookies, local storage or session data.
- Do not use `Data Private Weapon`.
- Do not bind `GS9 Knowledge VNG - Image Assets` as an answer corpus.
- Do not automatically bind CFL KBs whose contents, owner, permissions and retention have not been audited.
- Do not enable outbound messaging, publishing, production/config writes, compensation, sanctions, account mutation or database writes.
- Every action-producing output is `DRAFT` and requires Human approval.
- Use only the integrated Codex browser; do not call private APIs or reverse-engineer the site.

## Task 1 — Local catalog and per-Agent configuration

- [ ] Create `agent/liveops-custom-agent-catalog.md` with the ten Agent names, purposes, data boundaries and rollout state.
- [ ] Create one folder per Agent containing `README.md`, `config.md`, `tests.md` and `handoff.md`.
- [ ] Record full prompts, model baseline, mode/preset, retrieval, tools, limits and Human-approval boundary.
- [ ] Mark KB binding as `None — pending audit` until the Web UI proves an empty binding is supported.
- [ ] Validate that all ten folders and required Markdown files exist and contain no placeholder configuration.

## Task 2 — Inspect Agent creation workflow

- [ ] Open the integrated browser at `/kb/agents` and confirm the signed-in session.
- [ ] Inspect the visible create workflow without saving a test Agent.
- [ ] Determine whether an Agent can be created with no KB binding and without publishing/sharing.
- [ ] If the UI requires `All KB` or an unaudited KB, stop Web creation and record the blocker rather than weakening the data boundary.

## Task 3 — Create ten custom Agents

- [ ] Create each Agent using the local name, description, prompt and safe baseline settings.
- [ ] Leave unaudited capabilities off, including image/audio upload, database write paths and external actions.
- [ ] Save only the Agent configuration required to create it; do not share, publish, clone or test against private data.
- [ ] Capture the visible Agent ID or URL and creation state in its local `handoff.md`.

## Task 4 — Verification and handoff

- [ ] Re-open each created Agent and compare the visible configuration with its local `config.md`.
- [ ] Verify the Agent list contains exactly the intended ten new names, with no accidental duplicate.
- [ ] Classify every result as `Đã kiểm chứng`, `Có điều kiện` or `Bị chặn–Chưa xác định`.
- [ ] Update `agent/liveops-custom-agent-catalog.md`, `STATUS.md` and `HANDOFF.md` with fresh evidence.
- [ ] Do not run the handbook builder or unit tests because this task changes only Agent documentation and Web configuration.
