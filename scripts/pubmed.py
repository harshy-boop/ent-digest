# scripts/pubmed.py
import time
import requests
import xml.etree.ElementTree as ET
from typing import Optional
from scripts.models import Paper

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "ent-digest-routine (https://github.com/harshy-boop/ent-digest)"


def esearch(query: str, days: int = 7, retmax: int = 200) -> list[str]:
    """Return list of PMIDs matching `query`, with EDAT in the last `days` days."""
    params = {
        "db": "pubmed",
        "term": query,
        "datetype": "edat",
        "reldate": str(days),
        "retmax": str(retmax),
        "retmode": "xml",
    }
    r = requests.get(f"{EUTILS_BASE}/esearch.fcgi", params=params,
                     headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    return [id_el.text for id_el in root.findall(".//IdList/Id") if id_el.text]


def efetch_papers(pmids: list[str]) -> list[Paper]:
    """Fetch full metadata for the given PMIDs. Returns Paper list in input order."""
    if not pmids:
        return []
    # PubMed allows up to 200 IDs per request; we batch to be safe.
    out: list[Paper] = []
    for i in range(0, len(pmids), 100):
        batch = pmids[i:i + 100]
        params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "rettype": "xml",
        }
        r = requests.get(f"{EUTILS_BASE}/efetch.fcgi", params=params,
                         headers={"User-Agent": USER_AGENT}, timeout=60)
        r.raise_for_status()
        out.extend(_parse_efetch_xml(r.text))
        if i + 100 < len(pmids):
            time.sleep(0.4)  # NCBI rate limit: ~3 req/sec unauthenticated
    return out


def _parse_efetch_xml(xml_text: str) -> list[Paper]:
    root = ET.fromstring(xml_text)
    papers: list[Paper] = []
    for article in root.findall(".//PubmedArticle"):
        pmid = _text(article, ".//PMID")
        if not pmid:
            continue
        title = _text(article, ".//ArticleTitle") or ""
        journal = _text(article, ".//Journal/Title") or _text(article, ".//Journal/ISOAbbreviation") or ""
        abstract = " ".join(
            (el.text or "") for el in article.findall(".//Abstract/AbstractText")
        ).strip()
        author_els = article.findall(".//AuthorList/Author")
        authors = [_format_author(a) for a in author_els if _format_author(a)]
        senior_author, senior_affiliation = _senior_author_info(author_els)
        pub_types = [el.text for el in article.findall(".//PublicationTypeList/PublicationType") if el.text]
        mesh_terms = [el.text for el in article.findall(".//MeshHeadingList/MeshHeading/DescriptorName") if el.text]
        doi = next(
            (el.text for el in article.findall(".//ArticleId") if el.get("IdType") == "doi"),
            None,
        )
        edat = _edat(article)
        papers.append(Paper(
            pmid=pmid,
            title=title,
            authors=authors,
            senior_author=senior_author,
            senior_affiliation=senior_affiliation,
            journal=journal,
            journal_impact_factor=None,  # populated separately in the renderer if needed
            pub_types=pub_types,
            mesh_terms=mesh_terms,
            abstract=abstract,
            doi=doi,
            edat=edat,
        ))
    return papers


def _text(node, xpath: str) -> Optional[str]:
    el = node.find(xpath)
    return el.text if el is not None and el.text else None


def _format_author(author_el) -> Optional[str]:
    last = _text(author_el, "LastName")
    initials = _text(author_el, "Initials")
    if last and initials:
        return f"{last} {initials}"
    return last or _text(author_el, "CollectiveName")


def _senior_author_info(author_els) -> tuple[Optional[str], Optional[str]]:
    """Senior author convention: last individual author with an affiliation."""
    if not author_els:
        return None, None
    last_author = author_els[-1]
    name = _format_author(last_author)
    aff = _text(last_author, "AffiliationInfo/Affiliation")
    return name, aff


def _edat(article) -> str:
    """Extract Entrez Date as YYYY-MM-DD."""
    el = article.find(".//PubmedData/History/PubMedPubDate[@PubStatus='entrez']")
    if el is None:
        return ""
    y = _text(el, "Year") or ""
    m = (_text(el, "Month") or "").zfill(2)
    d = (_text(el, "Day") or "").zfill(2)
    return f"{y}-{m}-{d}" if y and m and d else ""
