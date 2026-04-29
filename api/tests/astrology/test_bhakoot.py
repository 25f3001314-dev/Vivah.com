import pytest

from v1.astrology.koots import calculate_bhakoot


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 1, 7.0),
        (1, 7, 7.0),
        (3, 11, 7.0),
        (5, 9, 7.0),
        (2, 12, 0.0),
        (4, 10, 0.0),
        (6, 8, 0.0),
        (1, 6, 0.0),
    ],
)
def test_bhakoot_pairs(a, b, expected):
    assert calculate_bhakoot(a, b) == expected
