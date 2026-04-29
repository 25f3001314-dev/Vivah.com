# -*- coding: utf-8 -*-
"""Pure Ashtakoot scoring functions and calculator facade."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..utils.constants import NAKSHATRA_GANA, NAKSHATRA_NADI, NAKSHATRA_YONI, RASHI_VARNA, RASHI_VASHYA, VARNA_RANK
from .tables import (
    GANA_SCORE,
    GRAHA_RELATION,
    GRAHA_SCORE,
    NADI_DOSHA_CANCELLATION,
    TARA_AUSPICIOUS,
    VASHYA_COMPAT,
    YONI_FRIEND_PAIRS,
    YONI_MILD_ENEMY_PAIRS,
    YONI_SCORES,
    YONI_WORST_ENEMY_PAIRS,
)


def calculate_varna(boy_rashi: str, girl_rashi: str) -> float:
    boy_rank = VARNA_RANK.get(RASHI_VARNA.get(boy_rashi, ""), 0)
    girl_rank = VARNA_RANK.get(RASHI_VARNA.get(girl_rashi, ""), 0)
    return 1.0 if boy_rank >= girl_rank else 0.0


def calculate_vashya(boy_rashi: str, girl_rashi: str) -> float:
    boy_vashya = RASHI_VASHYA.get(boy_rashi)
    girl_vashya = RASHI_VASHYA.get(girl_rashi)
    if not boy_vashya or not girl_vashya:
        return 0.0
    if boy_vashya == girl_vashya:
        return 2.0
    if girl_vashya in VASHYA_COMPAT.get(boy_vashya, set()):
        return 1.0
    return 0.0


def calculate_tara(boy_nak_num: int, girl_nak_num: int) -> float:
    boy_nak_num = int(boy_nak_num)
    girl_nak_num = int(girl_nak_num)
    if not (1 <= boy_nak_num <= 27 and 1 <= girl_nak_num <= 27):
        raise ValueError("nakshatra_number must be between 1 and 27")
    diff = (girl_nak_num - boy_nak_num) % 27
    if diff == 0:
        diff = 27
    tara = ((diff - 1) % 9) + 1
    return 3.0 if tara in TARA_AUSPICIOUS else 0.0


def calculate_yoni(boy_nakshatra: str, girl_nakshatra: str) -> float:
    boy_yoni_data = NAKSHATRA_YONI.get(boy_nakshatra)
    girl_yoni_data = NAKSHATRA_YONI.get(girl_nakshatra)

    if not boy_yoni_data or not girl_yoni_data:
        return YONI_SCORES["neutral"]

    boy_yoni, boy_gender = boy_yoni_data
    girl_yoni, girl_gender = girl_yoni_data

    if boy_yoni == girl_yoni:
        if boy_gender != girl_gender:
            return YONI_SCORES["same_yoni_opposite_gender"]
        return YONI_SCORES["same_yoni_same_gender"]

    pair = frozenset({boy_yoni, girl_yoni})
    if pair in YONI_WORST_ENEMY_PAIRS:
        return YONI_SCORES["worst_enemy"]
    if pair in YONI_MILD_ENEMY_PAIRS:
        return YONI_SCORES["mild_enemy"]
    if pair in YONI_FRIEND_PAIRS:
        return YONI_SCORES["friend"]
    return YONI_SCORES["neutral"]


def _graha_relation(planet_a: str, planet_b: str) -> str:
    mapping = GRAHA_RELATION.get(planet_a, {})
    if planet_b in mapping.get("Mitra", set()):
        return "Mitra"
    if planet_b in mapping.get("Shatru", set()):
        return "Shatru"
    return "Sam"


def calculate_graha_maitri(boy_rl: str, girl_rl: str) -> float:
    rel_1 = _graha_relation(boy_rl, girl_rl)
    rel_2 = _graha_relation(girl_rl, boy_rl)
    return GRAHA_SCORE.get(tuple(sorted((rel_1, rel_2))), 0.0)


def calculate_gana(boy_nakshatra: str, girl_nakshatra: str) -> float:
    boy_gana = NAKSHATRA_GANA.get(boy_nakshatra)
    girl_gana = NAKSHATRA_GANA.get(girl_nakshatra)
    if not boy_gana or not girl_gana:
        return 0.0
    return GANA_SCORE.get(tuple(sorted((boy_gana, girl_gana))), 0.0)


def calculate_bhakoot(boy_rashi_num: int, girl_rashi_num: int) -> float:
    boy_rashi_num = int(boy_rashi_num)
    girl_rashi_num = int(girl_rashi_num)
    if not (1 <= boy_rashi_num <= 12 and 1 <= girl_rashi_num <= 12):
        raise ValueError("rashi_number must be between 1 and 12")

    # Keep explicit forbidden sign-pairs and also apply 6-8 house relation.
    sign_pair = frozenset({boy_rashi_num, girl_rashi_num})
    if sign_pair in {frozenset({2, 12}), frozenset({4, 10}), frozenset({6, 8})}:
        return 0.0

    d1 = ((girl_rashi_num - boy_rashi_num) % 12) + 1
    d2 = ((boy_rashi_num - girl_rashi_num) % 12) + 1
    if frozenset({d1, d2}) == frozenset({6, 8}):
        return 0.0
    return 7.0


def _nadi_name(person: Dict[str, Any]) -> str:
    return NAKSHATRA_NADI.get(int(person["nakshatra_number"]), "Adi")


def _same_nakshatra_nadi_score(boy: Dict[str, Any], girl: Dict[str, Any]) -> float:
    cfg = NADI_DOSHA_CANCELLATION
    boy_pada = boy.get("pada")
    girl_pada = girl.get("pada")

    if boy_pada is None or girl_pada is None:
        behavior = cfg.get("missing_pada_behavior", "skip_rule")
        if behavior == "assume_same":
            return 8.0 if cfg.get("same_nakshatra_same_pada") else 0.0
        if behavior == "assume_different":
            return 8.0 if cfg.get("same_nakshatra_different_pada") else 0.0
        return 0.0

    if boy_pada == girl_pada:
        return 8.0 if cfg.get("same_nakshatra_same_pada") else 0.0
    return 8.0 if cfg.get("same_nakshatra_different_pada") else 0.0


def calculate_nadi(boy: Dict[str, Any], girl: Dict[str, Any]) -> float:
    if _nadi_name(boy) != _nadi_name(girl):
        return 8.0

    cfg = NADI_DOSHA_CANCELLATION

    if boy.get("nakshatra") and boy.get("nakshatra") == girl.get("nakshatra"):
        return _same_nakshatra_nadi_score(boy, girl)

    if boy.get("rashi") and boy.get("rashi") == girl.get("rashi"):
        return 8.0 if cfg.get("same_rashi_different_nakshatra") else 0.0

    if cfg.get("exception_nakshatras_enabled"):
        exceptions = cfg.get("exception_nakshatras", set())
        if boy.get("nakshatra") in exceptions and girl.get("nakshatra") in exceptions:
            return 8.0

    return 0.0


class AshtakootCalculator:
    """Facade over all 8 pure koot scoring functions."""

    KOOTS = [
        ("Varna", 1),
        ("Vashya", 2),
        ("Tara", 3),
        ("Yoni", 4),
        ("Graha Maitri", 5),
        ("Gana", 6),
        ("Bhakoot", 7),
        ("Nadi", 8),
    ]

    calculate_varna = staticmethod(calculate_varna)
    calculate_vashya = staticmethod(calculate_vashya)
    calculate_tara = staticmethod(calculate_tara)
    calculate_yoni = staticmethod(calculate_yoni)
    calculate_graha_maitri = staticmethod(calculate_graha_maitri)
    calculate_gana = staticmethod(calculate_gana)
    calculate_bhakoot = staticmethod(calculate_bhakoot)
    calculate_nadi = staticmethod(calculate_nadi)

    @classmethod
    def calculate_all_koots(cls, boy_profile: Dict[str, Any], girl_profile: Dict[str, Any]) -> Tuple[List[Tuple[str, int, float, float]], float]:
        koot_results: List[Tuple[str, int, float, float]] = []
        total = 0.0

        score = cls.calculate_varna(boy_profile["rashi"], girl_profile["rashi"])
        koot_results.append(("Varna", 1, score, 1.0))
        total += score

        score = cls.calculate_vashya(boy_profile["rashi"], girl_profile["rashi"])
        koot_results.append(("Vashya", 2, score, 2.0))
        total += score

        score = cls.calculate_tara(boy_profile["nakshatra_number"], girl_profile["nakshatra_number"])
        koot_results.append(("Tara", 3, score, 3.0))
        total += score

        score = cls.calculate_yoni(boy_profile["nakshatra"], girl_profile["nakshatra"])
        koot_results.append(("Yoni", 4, score, 4.0))
        total += score

        score = cls.calculate_graha_maitri(boy_profile["rashi_lord"], girl_profile["rashi_lord"])
        koot_results.append(("Graha Maitri", 5, score, 5.0))
        total += score

        score = cls.calculate_gana(boy_profile["nakshatra"], girl_profile["nakshatra"])
        koot_results.append(("Gana", 6, score, 6.0))
        total += score

        score = cls.calculate_bhakoot(boy_profile["rashi_number"], girl_profile["rashi_number"])
        koot_results.append(("Bhakoot", 7, score, 7.0))
        total += score

        score = cls.calculate_nadi(boy_profile, girl_profile)
        koot_results.append(("Nadi", 8, score, 8.0))
        total += score

        return koot_results, total
