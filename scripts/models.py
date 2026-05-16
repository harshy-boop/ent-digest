# scripts/models.py
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Paper:
    pmid: str
    title: str
    authors: list[str]
    senior_author: Optional[str]
    senior_affiliation: Optional[str]
    journal: str
    journal_impact_factor: Optional[float]
    pub_types: list[str]
    mesh_terms: list[str]
    abstract: str
    doi: Optional[str]
    edat: str  # ISO date, e.g., "2026-05-15"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Paper":
        return cls(**d)


@dataclass
class QueryBucket:
    key: str    # short identifier, e.g., "otology"
    label: str  # display label, e.g., "Otology / Neurotology"
    query: str  # PubMed E-utilities query string
