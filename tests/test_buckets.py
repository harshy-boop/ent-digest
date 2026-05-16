from scripts.buckets import BUCKETS


def test_ten_buckets_defined():
    assert len(BUCKETS) == 10


def test_bucket_keys_unique():
    keys = [b.key for b in BUCKETS]
    assert len(keys) == len(set(keys))


def test_each_bucket_has_nonempty_label_and_query():
    for b in BUCKETS:
        assert b.label
        assert b.query
        assert b.key


def test_expected_subspecialties_covered():
    keys = {b.key for b in BUCKETS}
    expected = {
        "otology", "rhinology", "laryngology", "airway",
        "sleep", "oncology", "facial_plastic", "pediatric", "crossover", "policy",
    }
    assert keys == expected
