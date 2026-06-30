---
name: personal-collaboration-context
description: Use when the user asks about recurring collaborators, GitHub collaborator labels, private development repositories, access sharing, or how to interpret collaborator usernames in the user's projects.
---

# Personal Collaboration Context

This skill stores lightweight, reusable collaboration labels for XiHao Park's
workflows. It is not a contacts database and should not store secrets,
private contact details, tokens, or personal identifiers beyond public handles
that the user explicitly provides.

## Personal Skill Repo

When the user says "my personal skill repo" or "我的个人 skill repo", use:

```text
/Users/park/code/MySkills
https://github.com/xihaopark/MySkills.git
```

This is the stable repo for personal skills, reusable working context, and
project-independent operating preferences.

## Frequent Collaborator Labels

| Label | Meaning | Use |
| --- | --- | --- |
| `WHXisWH` | Frequent collaborator GitHub username | Use when adding or checking collaborator access for private development repos, especially shared project-development material repos. |

## Working Rules

- For private development-material repositories, collaborator access should be
  explicit and verified.
- Do not add collaborators to public/product repos unless the user asks.
- Do not store collaborator secrets, emails, tokens, or private contact details
  in this skill.
- If a collaborator handle is ambiguous, ask before granting access.
