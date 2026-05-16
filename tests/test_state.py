import json
from datetime import date, timedelta
from scripts.state import load_seen, add_seen, prune_seen


def test_load_seen_returns_set_of_pmids(tmp_path):
    p = tmp_path / "seen.json"
    p.write_text(json.dumps({"pmids": [
        {"pmid": "1", "seen": "2026-05-01", "title": "A"},
        {"pmid": "2", "seen": "2026-05-02", "title": "B"},
    ]}))
    assert load_seen(p) == {"1", "2"}


def test_load_seen_empty_file_returns_empty_set(tmp_path):
    p = tmp_path / "seen.json"
    p.write_text(json.dumps({"pmids": []}))
    assert load_seen(p) == set()


def test_add_seen_appends_new_entries(tmp_path):
    p = tmp_path / "seen.json"
    p.write_text(json.dumps({"pmids": [
        {"pmid": "1", "seen": "2026-05-01", "title": "A"},
    ]}))
    add_seen(p, [{"pmid": "2", "title": "B"}, {"pmid": "3", "title": "C"}], today="2026-05-15")
    data = json.loads(p.read_text())
    pmids = {e["pmid"] for e in data["pmids"]}
    assert pmids == {"1", "2", "3"}
    new_entries = [e for e in data["pmids"] if e["pmid"] in {"2", "3"}]
    assert all(e["seen"] == "2026-05-15" for e in new_entries)


def test_prune_seen_drops_entries_older_than_window(tmp_path):
    p = tmp_path / "seen.json"
    today = date(2026, 5, 15)
    old = (today - timedelta(days=100)).isoformat()
    recent = (today - timedelta(days=30)).isoformat()
    p.write_text(json.dumps({"pmids": [
        {"pmid": "old", "seen": old, "title": "old"},
        {"pmid": "recent", "seen": recent, "title": "recent"},
    ]}))
    prune_seen(p, today=today.isoformat(), keep_days=90)
    data = json.loads(p.read_text())
    pmids = {e["pmid"] for e in data["pmids"]}
    assert pmids == {"recent"}
