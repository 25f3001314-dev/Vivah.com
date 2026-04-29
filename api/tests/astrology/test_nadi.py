from v1.astrology.koots import calculate_nadi
from v1.services import perform_ashtakoot_milan


BASE = {"nakshatra_number": 7, "nakshatra": "Punarvasu", "rashi": "Kark"}


def test_different_nadi_scores_8():
    boy = {"nakshatra_number": 7, "nakshatra": "Punarvasu", "rashi": "Kark"}
    girl = {"nakshatra_number": 8, "nakshatra": "Pushya", "rashi": "Kark"}
    assert calculate_nadi(boy, girl) == 8.0


def test_same_nakshatra_same_pada_scores_0():
    boy = dict(BASE, pada=1)
    girl = dict(BASE, pada=1)
    assert calculate_nadi(boy, girl) == 0.0


def test_same_nakshatra_different_pada_scores_8():
    boy = dict(BASE, pada=1)
    girl = dict(BASE, pada=2)
    assert calculate_nadi(boy, girl) == 8.0


def test_same_rashi_different_nakshatra_scores_8():
    boy = {"nakshatra_number": 7, "nakshatra": "Punarvasu", "rashi": "Kark"}
    girl = {"nakshatra_number": 10, "nakshatra": "Magha", "rashi": "Kark"}
    assert calculate_nadi(boy, girl) == 8.0


def test_missing_pada_assumes_different_and_scores_8():
    boy = dict(BASE)
    girl = dict(BASE)
    assert calculate_nadi(boy, girl) == 8.0


def test_hariom_komal_nadi_scores_8_with_missing_pada():
    result = perform_ashtakoot_milan("हरीओम", "कोमल")
    assert "error" not in result
    assert result["koot_results"][7][2] == 8.0


def test_nadi_symmetry():
    boy = {"nakshatra_number": 7, "nakshatra": "Punarvasu", "rashi": "Kark", "pada": 1}
    girl = {"nakshatra_number": 7, "nakshatra": "Punarvasu", "rashi": "Kark", "pada": 2}
    assert calculate_nadi(boy, girl) == calculate_nadi(girl, boy)
