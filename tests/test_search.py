# tests/test_search.py
from unittest.mock import patch
from scripts.search import run_all_queries
from scripts.models import Paper, QueryBucket


def _paper(pmid: str, title: str = "T") -> Paper:
    return Paper(pmid=pmid, title=title, authors=[], senior_author=None,
                 senior_affiliation=None, journal="J", journal_impact_factor=None,
                 pub_types=[], mesh_terms=[], abstract="", doi=None, edat="2026-05-15")


def test_run_all_queries_dedupes_across_buckets():
    buckets = [
        QueryBucket(key="a", label="A", query="q1"),
        QueryBucket(key="b", label="B", query="q2"),
    ]
    # Bucket a returns PMIDs [1, 2]; bucket b returns [2, 3]. Combined = [1, 2, 3].
    with patch("scripts.search.esearch", side_effect=[["1", "2"], ["2", "3"]]) as mock_es, \
         patch("scripts.search.efetch_papers", return_value=[_paper("1"), _paper("2"), _paper("3")]):
        results, per_bucket = run_all_queries(buckets, days=7, seen_pmids=set())
    assert {p.pmid for p in results} == {"1", "2", "3"}
    assert per_bucket["a"] == 2
    assert per_bucket["b"] == 2
    assert mock_es.call_count == 2


def test_run_all_queries_filters_seen_pmids():
    buckets = [QueryBucket(key="a", label="A", query="q1")]
    with patch("scripts.search.esearch", return_value=["1", "2", "3"]), \
         patch("scripts.search.efetch_papers", return_value=[_paper("2"), _paper("3")]):
        results, _ = run_all_queries(buckets, days=7, seen_pmids={"1"})
    assert {p.pmid for p in results} == {"2", "3"}


def test_run_all_queries_continues_on_bucket_failure():
    buckets = [
        QueryBucket(key="a", label="A", query="q1"),
        QueryBucket(key="b", label="B", query="q2"),
    ]
    # esearch raises twice for bucket a (initial + retry), then succeeds for bucket b
    with patch("scripts.search.esearch", side_effect=[Exception("API down"), Exception("API down"), ["3"]]), \
         patch("scripts.search.efetch_papers", return_value=[_paper("3")]), \
         patch("scripts.search.time.sleep"):
        results, per_bucket = run_all_queries(buckets, days=7, seen_pmids=set())
    assert {p.pmid for p in results} == {"3"}
    assert per_bucket["a"] == 0  # failed bucket recorded as zero
    assert per_bucket["b"] == 1
