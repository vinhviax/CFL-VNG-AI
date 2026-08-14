# GitHub Handoff Publish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cập nhật hồ sơ dự án, tạo handoff/prompt chuyển máy và publish toàn bộ project lên `https://github.com/vinhviax/CFL-VNG-AI` mà không commit credential.

**Architecture:** Root hiện tại được khởi tạo thành Git repository nhánh `main`. Toàn bộ artifact được track trừ secret/cache do `.gitignore` chặn; tài liệu trạng thái và audit là nguồn truy nguyên cho phiên tiếp theo.

**Tech Stack:** Markdown, PowerShell, Python 3, Git, GitHub HTTPS remote.

## Global Constraints

- Root duy nhất: `J:\My Drive\CFL\VNG AI\Knowledge Base VNG`.
- Remote: `https://github.com/vinhviax/CFL-VNG-AI.git`; branch: `main`.
- Không đọc, in, stage hoặc commit credential/token/private key.
- Không mutation VNG AI Web trong công việc publish Git.
- Không mô tả custom Agent là runtime/gold-set ready.
- Repository chưa có lịch sử nên làm việc tại root hiện hữu; không thể tạo worktree trước commit đầu tiên.

---

### Task 1: Tạo ranh giới Git an toàn

**Files:**
- Create: `.gitignore`
- Create: `audit/github-publish-2026-08-14.md`

- [x] **Step 1:** Ignore chính xác vùng credential, `.env`, private key, cache Python và metadata hệ điều hành.
- [x] **Step 2:** Ghi audit scope publish, ngoại lệ secret, kích thước và gate kiểm chứng.
- [x] **Step 3:** Xác minh credential đã biết không xuất hiện trong danh sách stage dự kiến.

### Task 2: Cập nhật tài liệu và prompt chuyển máy

**Files:**
- Modify: `AGENTS.md`
- Modify: `PROJECT.md`
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`
- Modify: `DECISIONS.md`
- Create: `NEXT_SESSION_PROMPT.md`

- [x] **Step 1:** Ghi remote/branch, quy tắc Git và scope toàn bộ project trừ secret.
- [x] **Step 2:** Đồng bộ thứ tự đọc phiên mới và trạng thái 10 Agent/25-file meta-KB.
- [x] **Step 3:** Viết prompt copy/paste có lệnh pull, thứ tự đọc, snapshot và safety constraints.
- [x] **Step 4:** Quét link/tên cũ/placeholder và kiểm tra tính nhất quán.

### Task 3: Khởi tạo repository và kiểm chứng artifact

**Files:**
- Create: `.git/` bằng Git

- [x] **Step 1:** Chạy `git init -b main` và thêm `origin` đúng URL.
- [x] **Step 2:** Stage toàn bộ project không bị ignore; kiểm tra file count, tổng size và file lớn nhất.
- [x] **Step 3:** Secret scan staged text chỉ trả về count/path, không in giá trị.
- [x] **Step 4:** Chạy `python scripts\build_handbook.py` và `python -m unittest discover -s tests -v`.
- [x] **Step 5:** Chạy validation 25-file meta-KB, 10 custom Agent ID/tool matrix và tài liệu Git handoff.

### Task 4: Commit, push và đối chiếu remote

**Files:**
- Modify: `STATUS.md`
- Modify: `HANDOFF.md`
- Modify: `audit/github-publish-2026-08-14.md`
- Modify: `docs/superpowers/plans/2026-08-14-github-handoff-publish.md`

- [ ] **Step 1:** Commit snapshot đã kiểm chứng với message mô tả Agent/KB handoff.
- [ ] **Step 2:** Push `main` lên `origin` không force.
- [ ] **Step 3:** Đối chiếu local HEAD với remote `refs/heads/main`.
- [ ] **Step 4:** Ghi trạng thái publish, tick plan, commit/push handoff cuối và xác minh working tree sạch.
