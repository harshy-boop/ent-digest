# ENT / Airway / Face Daily Digest

Scheduled Claude Code routine that surfaces, scores, and curates new ENT, airway,
and facial-surgery papers from PubMed each morning.

Live digest: https://harshy-boop.github.io/ent-digest/

## Layout

- `scripts/` — Python helpers (PubMed client, state, renderer, orchestrator)
- `templates/` — Jinja2 HTML templates for the digest and reading list
- `tests/` — pytest unit tests for the helpers
- `digests/` — daily HTML output, one file per day
- `failures/` — failure logs, only present when a run errors
- `seen_pmids.json` — rolling dedup state (last ~90 days), routine-managed
- `reading-list.md` — user-curated TODO list, Project-managed (NOT routine-managed)
- `reading-list.html` — rendered view of `reading-list.md`
- `routine-prompt.md` — the self-contained prompt the remote agent runs each day
- `reading-list-system-prompt.md` — system prompt for the Claude.ai Reading List Project

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Operations

### Daily flow
- 06:00 ET: routine runs automatically.
- Output appears at `https://claude.ai/code/routines/<routine-id>` and at
  `https://harshy-boop.github.io/ent-digest/`.
- Copy PMIDs into the **ENT Reading List** Claude project to bookmark.

### On failure
- You'll get a push notification ("ENT Digest Failed — open Claude Code").
- Open `failures/<date>.md` in the repo for the troubleshooting prompt.
- Paste that prompt into a fresh Claude Code session — it's self-contained.

### To pause the routine
- Open `https://claude.ai/code/routines/<routine-id>`, toggle Enabled off.

### To change behavior
- Bucket queries: `scripts/buckets.py` → commit + push (live next run).
- Scoring rubric: `scripts/rubric.md` → also update the inlined copy in
  `routine-prompt.md`, commit + push.
- Visual design: `templates/digest.html.j2` → commit + push.
- Schedule: re-invoke `/schedule` → "update" → adjust cron.
