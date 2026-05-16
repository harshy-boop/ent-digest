# tests/test_render.py
from pathlib import Path
from scripts.render import render_digest


def _sample_digest():
    return {
        "digest_date_long": "Friday, May 15, 2026",
        "edat_from": "May 8",
        "edat_to": "May 15",
        "buckets_run": 9,
        "surfaced_count": 52,
        "made_cut_count": 14,
        "must_read_count": 1,
        "run_time_et": "06:03 ET",
        "must_read": [{
            "pmid": "12345678",
            "title": "Test RCT",
            "authors_display": "Smith JA, Chen R",
            "senior_author": "Jones MK",
            "senior_affiliation": "MEEI",
            "journal": "N Engl J Med",
            "journal_impact_factor": 158.5,
            "score": 5,
            "badges": ["Multicenter RCT", "n = 412"],
            "novel_technique": False,
            "summary_sections": [
                {"label": "BACKGROUND", "text": "background text."},
                {"label": "METHODS", "text": "methods text."},
                {"label": "RESULTS", "text": "results text."},
                {"label": "LIMITATIONS", "text": "limits text."},
                {"label": "CLINICAL TAKEAWAY", "text": "takeaway text."},
            ],
            "rationale": "Large RCT.",
            "doi": "10.1056/xx",
        }],
        "noted": [{
            "pmid": "99887766",
            "title": "Test cohort",
            "journal": "Otol HNS",
            "score": 3,
            "badges": ["Cohort", "n = 156"],
            "summary": "summary text.",
        }],
        "digest_json": '{"sample": true}',
        "policy_updates": [],
    }


def test_render_produces_valid_html_with_key_elements():
    html = render_digest(_sample_digest())
    assert "<!DOCTYPE html>" in html
    assert "Friday, May 15, 2026" in html
    assert "Test RCT" in html
    assert "12345678" in html
    assert 'data-score="5"' in html
    assert "Novel Technique" not in html  # novel_technique=False
    assert "copy-pmid" in html
    assert 'id="digest-data"' in html


def test_render_includes_novel_technique_badge_when_set():
    digest = _sample_digest()
    digest["must_read"][0]["novel_technique"] = True
    html = render_digest(digest)
    assert "Novel Technique" in html


def test_render_handles_empty_must_read():
    digest = _sample_digest()
    digest["must_read"] = []
    digest["must_read_count"] = 0
    html = render_digest(digest)
    assert "Test RCT" not in html
    assert "Friday, May 15, 2026" in html  # rest of the page still renders


def test_render_includes_policy_section_when_items_present():
    digest = _sample_digest()
    digest["policy_updates"] = [
        {
            "source": "CMS",
            "tier": "CRITICAL",
            "title": "CMS finalizes coverage update for hypoglossal nerve stimulation",
            "summary": "Final NCD expands HGNS coverage to patients with AHI 15-65 (previously 15-50). Effective Q3 2026.",
            "url": "https://www.cms.gov/newsroom/press-releases/example",
            "date": "2026-05-14",
        },
        {
            "source": "AAO-HNS",
            "tier": "NOTABLE",
            "title": "Updated clinical practice guideline on benign paroxysmal positional vertigo",
            "summary": "Society releases revised BPPV guideline; key change: simplified Dix-Hallpike interpretation criteria.",
            "url": "https://www.entnet.org/news/example",
            "date": "2026-05-12",
        },
    ]
    html = render_digest(digest)
    assert "Policy &amp; Practice Updates" in html or "Policy &#38; Practice Updates" in html
    assert "CMS finalizes coverage update" in html
    assert "CRITICAL" in html
    assert "NOTABLE" in html


def test_render_omits_policy_section_when_empty():
    digest = _sample_digest()
    digest["policy_updates"] = []
    html = render_digest(digest)
    assert "No new policy updates this week" in html


from scripts.render import render_reading_list


def test_reading_list_renders_unread_and_read_sections():
    data = {
        "unread": [
            {"pmid": "1", "title": "Paper A", "journal": "JAMA", "score": 5, "added": "2026-05-15"},
        ],
        "read": [
            {"pmid": "2", "title": "Paper B", "journal": "NEJM", "score": 4, "added": "2026-05-10", "read": "2026-05-13"},
        ],
        "updated": "Friday, May 15, 2026",
    }
    html = render_reading_list(data)
    assert "Paper A" in html
    assert "Paper B" in html
    assert "PMID 1" in html
    assert "read 2026-05-13" in html
