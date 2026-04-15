---
name: commit-message
description: Create a commit message for the changes done following the "Conventional Commit Message Reference" section as mentioned in the README.md file of this project. 
  Use when user asks to create a commit message for the changes done in the project.
---
 1. Run `git status` and `git diff --cached` to understand what is staged.
 2. Read README.md's "Conventional Commit Message Reference" section for the format rules.
 3. Draft a commit message following the format.
 4. Present it to the user and ask for confirmation.
 5. If confirmed, run `git add` and `git commit` with the message.


