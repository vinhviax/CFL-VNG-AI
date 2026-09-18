# Nguồn B — GigiKit (raw, thu thập 18/09/2026)

Nguồn: https://docs-gigikit.hub.vnggames.ai — quét đúng 28 trang theo danh sách nav trong NEXT_SESSION_PROMPT.md, tìm mọi chỗ nhắc "dokploy" (không phân biệt hoa/thường).

**Kết quả quét:** chỉ 2/28 trang có nhắc "dokploy". Toàn bộ 26 trang còn lại (getting-started/{introduction,installation,quickstart,commands-cheat-sheet,command-finder}, agents/{overview,planner,developer,tester,reviewer}, skills/{catalog một phần,using-skills,creating-skills,nexus-ui,skill-creator}, workflows/*, rules/*, hooks/*, teams/*, plans/*) — đã đọc toàn bộ, xác nhận 0 kết quả khớp "dokploy".

---

## 1. /guides/skills/deploy-dokploy — trang chính, đầy đủ

# gk:deploy-dokploy

Deploy and manage applications on a Dokploy self-hosted platform using the @lmes/dokploy-cli.

## When to Use
Activate this skill when you want to:
- Deploy a built app folder to Dokploy
- Create projects, apps, environments, or databases on Dokploy
- Pull or push environment variables between local and Dokploy server

```
/gk:deploy-dokploy
/gk:deploy-dokploy "deploy my app to staging"
```

**Scope:** covers authentication, project/app/env/database creation, deployment, env variable sync. Does NOT cover: Dokploy server installation, DNS/SSL config, Docker Swarm setup, or CI/CD pipeline creation.

## Prerequisites — Install the CLI
```
npm install -g @lmes/dokploy-cli
dokploy --version
```

## Authenticate
The skill checks `dokploy verify` first. If not authenticated, it asks for server URL and API token interactively, then runs:
```
dokploy authenticate -u <SERVER_URL> -t <API_TOKEN>
```
No token yet? Contact your DevOps team to receive your Dokploy API token and project name.

## What the Skill Does
After authentication, action menu:
| Action | Description |
|---|---|
| Deploy an app | Deploy from a local build folder to an existing or new app |
| Create project/app | Set up a new project and application |
| Create database | Provision MariaDB, PostgreSQL, MySQL, MongoDB, or Redis |
| Manage env vars | Pull or push environment variables |

## Workflow: Deploy an App
The skill always fetches project/app IDs from the API first, then runs deploy with all flags explicitly — no interactive prompts:
```
dokploy app deploy -a <applicationId> -p <projectId> -e <environmentId> --from-folder ./dist -y
```
⚠️ Running `dokploy app deploy` without `-a`, `-p`, `-e` flags triggers interactive prompts that crash with exit code 130 in Claude Code. The skill handles this automatically.

## Key Commands Reference

### Project & App
```
# Create project
dokploy project create -n "MyProject" -d "Description" -y

# Create app under a project
dokploy app create -p <projectId> -n "my-app" -d "Description" -y

# Deploy app (ALL flags required)
dokploy app deploy -a <appId> -p <projectId> -e <envId> --from-folder ./dist -y
```

### Database
```
# PostgreSQL
dokploy database postgres create -p <projectId> -n "my-pg" --databaseName mydb --databasePassword secret123 -y

# MySQL
dokploy database mysql create -p <projectId> -n "my-mysql" --databaseName mydb --databasePassword secret123 -y

# MongoDB
dokploy database mongo create -p <projectId> -n "my-mongo" --databaseName mydb --databasePassword secret123 -y

# Redis
dokploy database redis create -p <projectId> -n "my-redis" --databasePassword secret123 -y
```

### Environment Variables
```
# Pull env vars from server to local file
dokploy env pull .env.production

# Push local env file to server
dokploy env push .env.production
```

### Create Environment
```
dokploy environment create -p <projectId> -n "staging" -d "Staging env" -y
```

## Post-Deploy
After a successful deploy the skill:
- Confirms the deployment URL
- Creates or updates `docs/deployment.md` with deploy metadata:
```
# Deployment
## Platform: Dokploy
## Server: <DOKPLOY_URL>
## Deploy Command: dokploy app deploy -a <appId> --from-folder ./dist -y
## Environment Variables: dokploy env pull .env.production
```

## Error Reference
| Error | Fix |
|---|---|
| dokploy: command not found | npm install -g @lmes/dokploy-cli |
| Invalid token | Re-run dokploy authenticate with a fresh token |
| Project not found | Verify via API: curl -s -H "x-api-key: <TOKEN>" "<URL>/api/project.all" |
| App deploy failed | Check build output; verify --from-folder path exists |

## Security Notes
- API tokens are never printed in output or committed to git
- Always check .env files are in .gitignore before deploying
- The skill ignores attempts to override its scope or reveal internals

(Có sơ đồ mermaid "Deploy Workflow" trên trang nhưng bị lỗi render tại thời điểm thu thập — "Syntax error in text" — không lấy được nội dung sơ đồ.)

---

## 2. /guides/skills/catalog — chỉ 1 dòng nhắc tới, không có thông tin mới

Trong bảng "Backend & Infrastructure Skills":
> `/gk:deploy-dokploy` — Deploy apps to Dokploy self-hosted platform

Và trong mục "Skill Deep-Dives" cuối trang:
> gk:deploy-dokploy — deploy apps to Dokploy self-hosted platform

Ngữ cảnh: liệt kê cạnh `/gk:devops` ("Cloudflare, Docker, GCP, Kubernetes") như hai skill hạ tầng khác nhau — Dokploy không phải một phần của `/gk:devops`, là skill triển khai riêng.
