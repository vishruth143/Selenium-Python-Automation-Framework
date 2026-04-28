# **"Locator Auto-Healer" Agent with Claude CLI**

## **Use Case:**
Create an agent which will analyze the logs for any failures due to locators for UI Tests and fix it automatically and create a PR within the git repository.

## **Building a "Locator Auto-Healer" Agent with Claude CLI**
1. Watches your test run logs
2. Detects locator failures (NoSuchElementException, TimeoutException)
3. Asks Claude to suggest a new locator by reading the page object + the failing HTML
4. Patches the page object file
5. Opens a Pull Request on GitHub with the fix

## 🗺️ The Big Picture (read once, then forget)
```
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

## ✅ Step 2 — Prerequisites Checklist
Before writing any code, please install/verify these on your Windows machine. 
Run each in PowerShell:
### 1.1 — Claude CLI
```powershell
claude --version    
```
If missing, install:
```powershell
npm install -g @anthropic-ai/claude-code
claude login
```

### 1.2 — GitHub CLI (used to open the PR)
```powershell
gh --version
```
If missing: download from https://cli.github.com/ then:
```powershell
gh auth login
```

### 1.3 — Git remote is set
```powershell
cd C:\Selenium-Python-Automation-Framework
git remote -v
git status
```
We need a remote named origin pointing to GitHub.

### 1.4 — Verify test_execution.log exists
```powershellpip
Test-Path output\logs\test_execution.log
```

## ✅ Step 2 — Create the healer folder skeleton + config
We'll create a self-contained workspace for the agent under scripts/healer/. 
Nothing here will interfere with your existing framework.

### 2.1 — Create the folder & empty files
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

### 2.2 — What each file will do
```
| File                      | Purpose                                                  |
|---------------------------|----------------------------------------------------------|
| `config.py`               | Constants: log path, pages dir, branch name              |
| `parse_failures.py`       | Read log → extract locator failures                      |
| `heal.py`                 | Call Claude CLI with page-object + failure context       |
| `patcher.py`              | Replace old locator tuple with Claude's suggestion       |
| `open_pr.py`              | git branch + commit + `gh pr create`                     |
| `run_healer.py`           | Orchestrator that runs all the above                     |
| `prompts/heal_locator.md` | Prompt template sent to Claude                           |
```
#### 2.2.1 — Fill in config.py
Add `scripts\healer\config.py` and verify using the below command:
```powershell
   python -c "from scripts.healer.config import APP_TO_SCOPE, PR_BODY, BRANCH_PREFIX; print(APP_TO_SCOPE); print(BRANCH_PREFIX)"
```
#### 2.2.2 — Fill in parse_failures.py
Add `scripts\healer\parse_failures.py` and verify using:
```powershell
   python -m scripts.healer.parse_failures
   Get-Content output\healer\failures.json
```
#### 2.2.3 — Fill in heal_locator.md and heal.py
```powershell
python -m scripts.healer.heal
Get-Content output\healer\suggestions.json
```
#### 2.2.3 — Fill in patcher.py
```powershell
python -m scripts.healer.patcher --dry-run
python -m scripts.healer.patcher
Get-Content tests\ui\pta\pages\login_page.py -TotalCount 15
Get-Content output\healer\patch_report.json
```
#### 2.2.3 — Fill in open_pr.py and run_healer.py
```powershell
python -m scripts.healer.open_pr --dry-run
python -m scripts.healer.open_pr
python -m scripts.healer.run_healer