# scripts/search.py
import time
import logging
from scripts.pubmed import esearch, efetch_papers
from scripts.models import QueryBucket, Paper

log = logging.getLogger(__name__)


def run_all_queries(
    buckets: list[QueryBucket],
    days: int,
    seen_pmids: set[str],
) -> tuple[list[Paper], dict[str, int]]:
    """
    Run each bucket's query, merge results, dedup by PMID, filter against seen_pmids.

    Returns:
        (papers, per_bucket_count)
        - papers: deduplicated Paper objects, ready for scoring
        - per_bucket_count: {bucket_key: raw_pmid_count} for transparency in the digest header
    """
    all_pmids: set[str] = set()
    per_bucket: dict[str, int] = {}

    for bucket in buckets:
        try:
            pmids = _esearch_with_retry(bucket.query, days)
            per_bucket[bucket.key] = len(pmids)
            all_pmids.update(pmids)
        except Exception as e:
            log.warning("Bucket %s failed: %s", bucket.key, e)
            per_bucket[bucket.key] = 0

    new_pmids = sorted(all_pmids - seen_pmids)
    if not new_pmids:
        return [], per_bucket

    papers = efetch_papers(new_pmids)
    return papers, per_bucket


def _esearch_with_retry(query: str, days: int, retries: int = 1):
    """Single retry with 30s backoff per the spec's transient-error policy.

    Returns: list of PMIDs (strings).
    """
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return esearch(query, days=days)
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(30)
    raise last_exc
