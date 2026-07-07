---
name: personal-collaboration-context
description: Use when the user asks about recurring collaborators, GitHub collaborator labels, private development repositories, access sharing, or how to interpret collaborator usernames in the user's projects.
---

# Personal Collaboration Context

This skill stores lightweight, reusable collaboration labels for XiHao Park's
workflows. It is not a general contacts database. Store only public GitHub
profile emails or emails explicitly provided/confirmed by the user.

## Personal Skill Repo

When the user says "my personal skill repo" or "我的个人 skill repo", use:

```text
/Users/park/code/MySkills
https://github.com/xihaopark/MySkills.git
```

This is the stable repo for personal skills, reusable working context, and
project-independent operating preferences.

## Frequent Collaborator Labels

| Label | Name | Public email | Evidence | Use |
| --- | --- | --- | --- | --- |
| `WHXisWH` | Hongxi Wang | whx12110405@gmail.com | Frequent collaborator named by the user; GitHub collaborator on `xihaopark/AZ`; pending `write` invitation on `xihaopark/AZ_dev` as of 2026-06-30. | Use when adding or checking collaborator access for private development repos, especially shared project-development material repos. |

## GitHub Collaborator Candidates

These handles came from GitHub API checks on core/recent `xihaopark/*`
repositories. Treat them as candidates for context, not as a complete contact
list. Collaborator evidence is stronger than one-off contributor evidence.

| GitHub handle | Name | Public email | Evidence |
| --- | --- | --- | --- |
| `chenzRG` | 未公开 | 未公开 | Collaborator on `AZ`, `CancerKG`, `KEGG_KG`, `Pipeline_Analysis_Agent_Framework`; contributor on `AZ`. |
| `yangziwei96` | Ziwei Yang | 未公开 | Collaborator on `AZ`, `CancerKG`, `Pipeline_Analysis_Agent_Framework`. |
| `zywang-j` | Zhangyu Wang | 未公开 | Collaborator on `KEGG_KG`, `zhangyu_KG`. |
| `LngW` | 未公开 | 未公开 | Collaborator and contributor on `Pipeline_Analysis_Agent_Framework`. |
| `waiting-yoo` | 未公开 | 未公开 | Collaborator on `Bio_Agent_Workflows`. |
| `Rononon241226` | Wang Xuan | 未公开 | Collaborator on `CancerKG`. |
| `Atham-He` | 未公开 | 2541207010@qq.com | Collaborator on `Bio_Agent_Workflows`; email is public on GitHub profile. |
| `HarukaMa` | Haruka | mrx@hcc.im | Contributor on `Bio_Agent_Workflows` and `RBioBench`; email is public on GitHub profile. |

## Public Email Contributor Candidates

These accounts are not confirmed as frequent collaborators from the scoped API
check. Keep them as lower-confidence GitHub context unless the user confirms a
working relationship.

| GitHub handle | Name | Public email | Evidence |
| --- | --- | --- | --- |
| `zhangh12` | Han Zhang | zhangh.ustc@gmail.com | Contributor on `pharma-skills`. |
| `quuu` | Andrew Qu | andrew.qu@vercel.com | Contributor on `skills`. |
| `nanxstats` | Nan Xiao | hello@nanx.me | Contributor on `pharma-skills`. |
| `mattpic-ant` | Matt Piccolella | mattpic@anthropic.com | Contributor on `skills`. |
| `klazuka` | Keith Lazuka | klazuka@gmail.com | Contributor on `skills`. |
| `kencheeto` | Kenshiro Nakagawa | kencheeto@gmail.com | Contributor on `skills`. |
| `jeffreyad` | Jeff Dickinson | jeffowf@gmail.com | Contributor on `pharma-skills`. |
| `ericharmeling` | Eric Harmeling | eric.harmeling@outlook.com | Contributor on `skills`. |
| `elong0527` | yilong zhang | elong0527@gmail.com | Contributor on `pharma-skills`. |
| `efchea1` | Emmanuel Fle Chea | emmanuelf.chea@gmail.com | Contributor on `pharma-skills`. |

## Working Rules

- For private development-material repositories, collaborator access should be
  explicit and verified.
- Do not add collaborators to public/product repos unless the user asks.
- Do not harvest or store emails from git commit metadata. Only store public
  GitHub profile emails or user-confirmed emails.
- Do not store collaborator secrets, tokens, private contact details, or
  personal identifiers unrelated to collaboration routing in this skill.
- If a collaborator handle is ambiguous, ask before granting access.
