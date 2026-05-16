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
