---
name: commit-message
description: Create a commit message for the changes done following the "Conventional Commit Message Reference" section as mentioned in the README.md file of this project. 
  Use when user asks to create a commit message for the changes done in the project.
---
 1. Run `git add -A` to stage all changed, new, and deleted files.
 2. Run `git status` and `git diff --cached` to see the full set of staged changes.
 3. Read README.md's "Conventional Commit Message Reference" section for the format rules.
 4. Draft a commit message following the format.
 5. Present it to the user and ask for confirmation.
 6. If confirmed, run `git commit` with the message.
