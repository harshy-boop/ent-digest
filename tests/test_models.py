from scripts.models import Paper, QueryBucket


def test_paper_round_trips_through_dict():
    p = Paper(
        pmid="12345678",
        title="Test paper",
        authors=["Smith J", "Jones K"],
        senior_author="Jones K",
        senior_affiliation="Mass Eye and Ear",
        journal="N Engl J Med",
        journal_impact_factor=158.5,
        pub_types=["Randomized Controlled Trial"],
        mesh_terms=["Otolaryngology"],
        abstract="An abstract.",
        doi="10.1056/NEJMxx",
        edat="2026-05-15",
    )
    d = p.to_dict()
    p2 = Paper.from_dict(d)
    assert p == p2


def test_query_bucket_holds_label_and_query():
    b = QueryBucket(key="otology", label="Otology / Neurotology", query="otologic[MeSH]")
    assert b.key == "otology"
    assert b.label == "Otology / Neurotology"
    assert b.query == "otologic[MeSH]"
