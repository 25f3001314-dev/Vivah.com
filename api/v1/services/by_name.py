# -*- coding: utf-8 -*-
"""Service helpers for name-based matchmaking."""

from __future__ import annotations

from typing import Any, Dict

from ..utils import extract_first_syllable
from . import AshtakootCalculator, PersonAstrologyProfile


def get_first_syllable(name: str) -> str:
    syllable = extract_first_syllable(name)
    if not syllable:
        raise ValueError("Could not extract first syllable from the provided name")
    return syllable


def generate_avakahada_attributes(name: str) -> Dict[str, Any]:
    profile = PersonAstrologyProfile(name)
    result = profile.extract_profile()
    if "error" in result:
        raise ValueError(result["error"])
    return {
        "name": result["name"],
        "first_syllable": result["first_syllable"],
        "nakshatra": result["nakshatra"],
        "nakshatra_number": result["nakshatra_number"],
        "rashi": result["rashi"],
        "rashi_number": result["rashi_number"],
        "gana": result["gana"],
        "yoni": result["yoni"],
        "yoni_gender": result["yoni_gender"],
        "nadi": result["nadi"],
        "varna": result["varna"],
        "vashya": result["vashya"],
        "rashi_lord": result["rashi_lord"],
        "nakshatra_lord": result["nakshatra_lord"],
        "source": result["source"],
        "profile": result,
    }


def compare_ashtakoot(boy_profile: Dict[str, Any], girl_profile: Dict[str, Any]) -> Dict[str, Any]:
    koot_results, total = AshtakootCalculator.calculate_all_koots(boy_profile, girl_profile)
    return {
        "varna": koot_results[0][2],
        "vashya": koot_results[1][2],
        "tara": koot_results[2][2],
        "yoni": koot_results[3][2],
        "graha_maitri": koot_results[4][2],
        "gana": koot_results[5][2],
        "bhakoot": koot_results[6][2],
        "nadi": koot_results[7][2],
        "total": round(total, 1),
        "max": 36,
    }