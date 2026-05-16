# tests/test_pubmed.py
from pathlib import Path
from unittest.mock import patch, Mock
from scripts.pubmed import esearch, efetch_papers


FIXTURES = Path(__file__).parent / "fixtures"


def _mock_response(text: str) -> Mock:
    m = Mock()
    m.status_code = 200
    m.text = text
    m.raise_for_status = Mock()
    return m


def test_esearch_returns_pmid_list():
    fixture = (FIXTURES / "esearch_sample.xml").read_text()
    with patch("scripts.pubmed.requests.get", return_value=_mock_response(fixture)):
        pmids = esearch(query="cholesteatoma", days=7)
    assert isinstance(pmids, list)
    assert all(p.isdigit() for p in pmids)
    assert len(pmids) > 0


def test_efetch_papers_parses_metadata():
    fixture = (FIXTURES / "efetch_sample.xml").read_text()
    with patch("scripts.pubmed.requests.get", return_value=_mock_response(fixture)):
        # Use any PMID — the mock returns the fixture regardless
        papers = efetch_papers(["12345"])
    assert len(papers) == 1
    p = papers[0]
    assert p.pmid  # non-empty
    assert p.title  # non-empty
    assert p.journal  # non-empty
    assert isinstance(p.authors, list)


import pytest


@pytest.mark.live
def test_esearch_live_smoke():
    """Hits the real PubMed API. Run with: pytest -m live"""
    pmids = esearch(query="cholesteatoma", days=14, retmax=5)
    assert len(pmids) > 0
    papers = efetch_papers(pmids[:2])
    assert len(papers) == 2
    assert papers[0].title
