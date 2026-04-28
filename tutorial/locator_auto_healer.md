# Locator Auto-Healer Agent with Claude CLI

> An AI-powered agent that automatically detects, fixes, and raises a PR for broken UI test locators.

---

## 📌 Use Case

Build an agent that:

- Analyzes UI test logs for **locator-related failures**
- Suggests and applies a fix automatically
- Opens a **Pull Request** on GitHub with the patch

---

## 🤖 What the Agent Does

1. Watches your test run logs
2. Detects locator failures (`NoSuchElementException`, `TimeoutException`)
3. Asks **Claude** to suggest a new locator using the page object + failing HTML
4. Patches the page object file
5. Opens a **Pull Request** on GitHub with the fix

---

## 🗺️ The Big Picture

> Read once, then forget — the orchestrator wires it all together.

```text
                      pytest run                                (Step 1)
                          │
                          ▼
              output/logs/test_execution.log                    (Step 2)
                          │
                          ▼
            scripts/healer/parse_failures.py                    (Step 3)
                          │
                          ▼
            scripts/healer/heal.py  ── calls ──► Claude CLI     (Step 4)
                          │
                          ▼
            patches tests/ui/<app>/pages/*.py                   (Step 5)
                          │
                          ▼
            git checkout -b fix/heal-locators
            git commit + gh pr create                           (Step 6)
```

---

## ✅ Step 1 — Prerequisites Checklist

Before writing any code, install/verify these on your Windows machine.
Run each command in **PowerShell**.

### 1.1 Claude CLI

```powershell
claude --version
```

If missing, install:

```powershell
npm install -g @anthropic-ai/claude-code
claude login
```

### 1.2 GitHub CLI (used to open the PR)

```powershell
gh --version
```

If missing — download from <https://cli.github.com/> then:

```powershell
gh auth login
```

### 1.3 Git remote is set

```powershell
cd C:\Selenium-Python-Automation-Framework
git remote -v
git status
```

> A remote named `origin` pointing to GitHub is required.

### 1.4 Verify `test_execution.log` exists

```powershell
Test-Path output\logs\test_execution.log
```

---

## ✅ Step 2 — Create the Healer Skeleton + Config

Create a self-contained workspace under `scripts/healer/`.
Nothing here will interfere with your existing framework.

### 2.1 Create folders & empty files

```powershell
cd C:\Selenium-Python-Automation-Framework

# Create folders
New-Item -ItemType Directory -Force -Path scripts\healer | Out-Null
New-Item -ItemType Directory -Force -Path scripts\healer\prompts | Out-Null
New-Item -ItemType Directory -Force -Path output\healer | Out-Null

# Create empty files we'll fill in next steps
New-Item -ItemType File -Force -Path scripts\healer\__init__.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\config.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\parse_failures.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\heal.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\patcher.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\open_pr.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\run_healer.py | Out-Null
New-Item -ItemType File -Force -Path scripts\healer\prompts\heal_locator.md | Out-Null
```

### 2.2 What Each File Does

| File                        | Purpose                                              |
| --------------------------- | ---------------------------------------------------- |
| `config.py`                 | Constants: log path, pages dir, branch name         |
| `parse_failures.py`         | Read log → extract locator failures                 |
| `heal.py`                   | Call Claude CLI with page-object + failure context  |
| `patcher.py`                | Replace old locator tuple with Claude's suggestion  |
| `open_pr.py`                | `git` branch + commit + `gh pr create`              |
| `run_healer.py`             | Orchestrator that runs all the above                |
| `prompts/heal_locator.md`   | Prompt template sent to Claude                      |

---

### 2.2.1 Fill in `config.py`

Add `scripts\healer\config.py`, then verify:

```powershell
python -c "from scripts.healer.config import APP_TO_SCOPE, PR_BODY, BRANCH_PREFIX; print(APP_TO_SCOPE); print(BRANCH_PREFIX)"
```

### 2.2.2 Fill in `parse_failures.py`

Add `scripts\healer\parse_failures.py`, then verify:

```powershell
python -m scripts.healer.parse_failures
Get-Content output\healer\failures.json
```

### 2.2.3 Fill in `heal_locator.md` and `heal.py`

```powershell
python -m scripts.healer.heal
Get-Content output\healer\suggestions.json
```

### 2.2.4 Fill in `patcher.py`

```powershell
python -m scripts.healer.patcher --dry-run
python -m scripts.healer.patcher
Get-Content tests\ui\pta\pages\login_page.py -TotalCount 15
Get-Content output\healer\patch_report.json
```

### 2.2.5 Fill in `open_pr.py` and `run_healer.py`

```powershell
python -m scripts.healer.open_pr --dry-run
python -m scripts.healer.open_pr
python -m scripts.healer.run_healer
```

---

## ✅ Step 3 — Run the Healer Agent

Once all the pieces are in place, run the entire healer agent with:

```powershell
python -m scripts.healer.run_healer
```

This executes all steps in sequence:

1. Parse the logs for locator failures
2. Call Claude CLI to get healing suggestions
3. Patch the page object files with new locators
4. Open a Pull Request on GitHub with the changes

---

## 🎉 Conclusion

Congratulations! You've built a **Locator Auto-Healer** agent that can
automatically fix locator issues in your UI tests by leveraging Claude's
language understanding.

This agent will:

- ⏱️ Save time
- 🧪 Reduce test flakiness
- 🔁 Proactively heal locator failures as they occur

### 🚀 Next Steps / Enhancements

- Add more sophisticated failure detection
- Support multiple locator strategies (CSS, XPath, ID, etc.)
- Integrate with **CI/CD pipelines** for fully automated healing on test failures

