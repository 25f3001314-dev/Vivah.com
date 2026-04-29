from v1.astrology.koots import calculate_yoni


def test_same_yoni_opposite_gender_scores_4():
    assert calculate_yoni("Ashwini", "Shatabhisha") == 4.0


def test_same_yoni_same_gender_scores_3():
    assert calculate_yoni("Ashwini", "Ashwini") == 3.0


def test_worst_enemy_scores_0():
    assert calculate_yoni("Ashwini", "Hasta") == 0.0


def test_friend_pair_scores_3():
    assert calculate_yoni("Ashwini", "Bharani") == 3.0


def test_symmetry_property():
    pairs = [
        ("Ashwini", "Hasta"),
        ("Ashwini", "Bharani"),
        ("Punarvasu", "Mrigashira"),
        ("Purva Ashadha", "Uttara Ashadha"),
    ]
    for a, b in pairs:
        assert calculate_yoni(a, b) == calculate_yoni(b, a)
