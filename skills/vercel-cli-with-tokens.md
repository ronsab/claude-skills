---
name: vercel-cli-with-tokens
description: Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login — e.g. "deploy to vercel", "set up vercel", "add environment variables to vercel".
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel CLI with Tokens

Deploy and manage projects on Vercel using the CLI with token-based authentication, without relying on `vercel login`.

## Step 1: Locate the Vercel Token

Work through these scenarios in order:

### A) `VERCEL_TOKEN` is already set in the environment

```bash
printenv VERCEL_TOKEN
```

If this returns a value, you're ready. Skip to Step 2.

### B) Token is in a `.env` file under `VERCEL_TOKEN`

```bash
grep '^VERCEL_TOKEN=' .env 2>/dev/null
```

If found, export it:

```bash
export VERCEL_TOKEN=$(grep '^VERCEL_TOKEN=' .env | cut -d= -f2-)
```

### C) Token is in a `.env` file under a different name

```bash
grep -i 'vercel' .env 2>/dev/null
```

Then export as `VERCEL_TOKEN`:

```bash
export VERCEL_TOKEN=$(grep '^<VARIABLE_NAME>=' .env | cut -d= -f2-)
```

### D) No token found — ask the user

If none of the above yield a token, ask the user to provide one from vercel.com/account/tokens.

---

**Important:** Once `VERCEL_TOKEN` is exported, the CLI reads it natively — **do not pass it as a `--token` flag**.

```bash
# Bad — token visible in shell history
vercel deploy --token "vca_abc123"

# Good — CLI reads VERCEL_TOKEN from environment
export VERCEL_TOKEN="vca_abc123"
vercel deploy
```

## Step 2: Locate the Project and Team

```bash
printenv VERCEL_PROJECT_ID
printenv VERCEL_ORG_ID
grep -i 'vercel' .env 2>/dev/null
```

If you have both `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`, export them:

```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```

Note: `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` must be set together.

## CLI Setup

```bash
npm install -g vercel
vercel --version
```

## Deploying a Project

### Quick Deploy (have project ID)

```bash
vercel deploy -y --no-wait
vercel deploy --scope <team-slug> -y --no-wait
vercel deploy --prod --scope <team-slug> -y --no-wait  # production only when explicitly asked
vercel inspect <deployment-url>  # check status
```

### Full Deploy Flow (need to link first)

#### Check state
```bash
git remote get-url origin 2>/dev/null
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

#### Link the project
```bash
vercel link --repo --scope <team-slug> -y   # if git remote exists
vercel link --scope <team-slug> -y           # if no git remote
vercel link --project <project-name> --scope <team-slug> -y  # by name
```

#### Deploy after linking

**A) Git Push (preferred — has git remote)**
1. Ask the user before pushing. Never push without explicit approval.
2. Commit and push:
   ```bash
   git add .
   git commit -m "deploy: <description>"
   git push
   ```
3. Get URL: `sleep 5 && vercel ls --format json --scope <team-slug>`

**B) CLI Deploy (no git remote)**
```bash
vercel deploy --scope <team-slug> -y --no-wait
vercel inspect <deployment-url>
```

## Managing Environment Variables

```bash
echo "value" | vercel env add VAR_NAME --scope <team-slug>
echo "value" | vercel env add VAR_NAME production --scope <team-slug>
vercel env ls --scope <team-slug>
vercel env pull --scope <team-slug>
vercel env rm VAR_NAME --scope <team-slug> -y
```

## Inspecting Deployments

```bash
vercel ls --format json --scope <team-slug>
vercel inspect <deployment-url>
vercel inspect <deployment-url> --logs
vercel logs <deployment-url>
```

## Managing Domains

```bash
vercel domains ls --scope <team-slug>
vercel domains add <domain> --scope <team-slug>
```

## Working Agreement

- **Never pass `VERCEL_TOKEN` as a `--token` flag.**
- **Check the environment for tokens before asking the user.**
- **Default to preview deployments.**
- **Ask before pushing to git.**
- **Do not modify `.vercel/` files directly.**
- **Do not curl/fetch deployed URLs to verify.**
- **Use `--format json`** when structured output helps.
- **Use `-y`** on commands that prompt for confirmation.

## Troubleshooting

### Token not found
```bash
printenv | grep -i vercel
grep -i vercel .env 2>/dev/null
```

### Authentication error
Verify: `vercel whoami` — if it fails, ask the user for a fresh token.

### Wrong team
```bash
vercel whoami --scope <team-slug>
```

### Build failure
```bash
vercel inspect <deployment-url> --logs
```

### CLI not installed
```bash
npm install -g vercel
```
