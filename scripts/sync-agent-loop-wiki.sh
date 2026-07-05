#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WIKI_REMOTE="${WIKI_REMOTE:-https://github.com/xihaopark/MySkills.wiki.git}"
WIKI_DIR="${WIKI_DIR:-/tmp/MySkills.wiki}"

if ! git ls-remote "$WIKI_REMOTE" HEAD >/dev/null 2>&1; then
  cat >&2 <<'EOF'
GitHub Wiki repository is not initialized yet.

Open https://github.com/xihaopark/MySkills/wiki in a signed-in browser,
click "Create the first page", save any initial Home page, then rerun this script.
EOF
  exit 2
fi

rm -rf "$WIKI_DIR"
git clone "$WIKI_REMOTE" "$WIKI_DIR"

cp "$REPO_ROOT"/docs/agent-loop-systems/Home.md "$WIKI_DIR"/Home.md
cp "$REPO_ROOT"/docs/agent-loop-systems/_Sidebar.md "$WIKI_DIR"/_Sidebar.md
cp "$REPO_ROOT"/docs/agent-loop-systems/Agent-Loop-Systems-*.md "$WIKI_DIR"/
cp "$REPO_ROOT"/docs/agent-loop-systems/Scientific-Workflow-Agent-Design-Questions.md "$WIKI_DIR"/
cp "$REPO_ROOT"/docs/agent-loop-systems/Claude-Science-Full-Reference-ZH.md "$WIKI_DIR"/

git -C "$WIKI_DIR" add .
if git -C "$WIKI_DIR" diff --cached --quiet; then
  echo "Wiki already up to date."
  exit 0
fi

git -C "$WIKI_DIR" commit -m "Sync agent loop systems wiki"
git -C "$WIKI_DIR" push
echo "Published: https://github.com/xihaopark/MySkills/wiki"

