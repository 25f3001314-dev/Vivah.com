# -*- coding: utf-8 -*-
"""Profile derivation for name-based astrology attributes."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..utils import normalize_devanagari, validate_name
from ..utils.constants import (
    NAKSHATRA_GANA,
    NAKSHATRA_LORDS,
    NAKSHATRA_NADI,
    NAKSHATRA_YONI,
    RASHI_LORDS,
    RASHI_TO_NUMBER,
    RASHI_VARNA,
    RASHI_VASHYA,
)
from .sources import resolver


RASHI_BY_NUMBER = {v: k for k, v in RASHI_TO_NUMBER.items()}


def _derive_rashi_from_nakshatra_number(nakshatra_number: int) -> Optional[str]:
    if not (1 <= nakshatra_number <= 27):
        return None
    rashi_num = min(((nakshatra_number - 1) // 2) + 1, 12)
    return RASHI_BY_NUMBER.get(rashi_num)


class PersonAstrologyProfile:
    """Derive complete person profile using the best available source."""

    def __init__(self, name: str):
        self.name = normalize_devanagari(name)

    def extract_profile(self) -> Dict[str, Any]:
        is_valid, error = validate_name(self.name)
        if not is_valid:
            return {"error": error}

        try:
            base, source = resolver.resolve(self.name)
        except ValueError as exc:
            return {"error": str(exc)}

        nakshatra = base.get("nakshatra")
        nakshatra_number = base.get("nakshatra_number")
        if not nakshatra or not nakshatra_number:
            return {"error": "Failed to determine Nakshatra from the name"}

        rashi = base.get("rashi")
        rashi_number = base.get("rashi_number")

        if not rashi:
            rashi = _derive_rashi_from_nakshatra_number(int(nakshatra_number))
        if not rashi:
            return {"error": "Failed to determine Rashi"}

        if not rashi_number:
            rashi_number = RASHI_TO_NUMBER.get(rashi)

        yoni_tuple = NAKSHATRA_YONI.get(nakshatra, ("Unknown", "M"))

        return {
            "name": self.name,
            "first_syllable": base.get("first_syllable"),
            "nakshatra": nakshatra,
            "nakshatra_number": int(nakshatra_number),
            "pada": base.get("pada"),
            "rashi": rashi,
            "rashi_number": int(rashi_number) if rashi_number else None,
            "gana": NAKSHATRA_GANA.get(nakshatra, "Manav"),
            "yoni": yoni_tuple[0],
            "yoni_gender": yoni_tuple[1],
            "varna": RASHI_VARNA.get(rashi, "Shudra"),
            "vashya": RASHI_VASHYA.get(rashi, "Manav"),
            "nadi": NAKSHATRA_NADI.get(int(nakshatra_number), "Adi"),
            "rashi_lord": RASHI_LORDS.get(rashi, "Unknown"),
            "nakshatra_lord": NAKSHATRA_LORDS.get(int(nakshatra_number), "Unknown"),
            "source": source,
        }
