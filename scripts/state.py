# scripts/state.py
import json
from datetime import date, timedelta
from pathlib import Path


def load_seen(path: Path) -> set:
    """Load the set of seen PMIDs from disk. Returns empty set if file missing."""
    if not path.exists():
        return set()
    data = json.loads(path.read_text() or '{"pmids": []}')
    return {e["pmid"] for e in data.get("pmids", [])}


def add_seen(path: Path, new_entries: list, today: str) -> None:
    """
    Append new entries to the seen-list. Each entry should have `pmid` and `title`.
    Stamps `seen=today` on each new entry.
    """
    data = json.loads(path.read_text() or '{"pmids": []}') if path.exists() else {"pmids": []}
    existing_pmids = {e["pmid"] for e in data["pmids"]}
    for e in new_entries:
        if e["pmid"] in existing_pmids:
            continue
        data["pmids"].append({
            "pmid": e["pmid"],
            "title": e.get("title", ""),
            "seen": today,
        })
    path.write_text(json.dumps(data, indent=2))


def prune_seen(path: Path, today: str, keep_days: int = 90) -> None:
    """Drop entries with `seen` older than `keep_days` from today."""
    if not path.exists():
        return
    data = json.loads(path.read_text())
    cutoff = (date.fromisoformat(today) - timedelta(days=keep_days)).isoformat()
    data["pmids"] = [e for e in data["pmids"] if e.get("seen", "") >= cutoff]
    path.write_text(json.dumps(data, indent=2))
