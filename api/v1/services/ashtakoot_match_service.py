# -*- coding: utf-8 -*-
"""Attribute-based Ashtakoot Milan service.

This module keeps the scoring rules isolated from HTTP concerns. It accepts
precomputed astrology attributes for the boy and girl, validates the required
fields, and returns a detailed 8-koot breakdown.

Missing-data policy:
- If a koot cannot be computed because a required field is missing, the service
  returns a structured error instead of guessing.
- This is intentionally strict so the caller knows exactly which attributes are
  needed.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple
import logging

from . import AshtakootCalculator

logger = logging.getLogger(__name__)


REQUIRED_FIELDS = {
    "varna": ["rashi"],
    "vashya": ["rashi"],
    "tara": ["nakshatra_number"],
    "yoni": ["nakshatra"],
    "graha_maitri": ["rashi_lord"],
    "gana": ["nakshatra"],
    "bhakoot": ["rashi_number"],
    "nadi": ["nakshatra_number"],
}

ALL_REQUIRED_FIELDS = sorted({field for fields in REQUIRED_FIELDS.values() for field in fields})


def _normalize_text(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return value


def _validate_person_attributes(person: Dict[str, Any], label: str) -> Tuple[Dict[str, Any], List[str]]:
    normalized: Dict[str, Any] = {}
    missing: List[str] = []

    for field in [
        "name",
        "first_syllable",
        "nakshatra",
        "nakshatra_number",
        "rashi",
        "rashi_number",
        "gana",
        "yoni",
        "nadi",
        "varna",
        "vashya",
        "rashi_lord",
        "nakshatra_lord",
    ]:
        value = _normalize_text(person.get(field))
        if value is None and field in ALL_REQUIRED_FIELDS:
            missing.append(f"{label}.{field}")
        normalized[field] = value

    # Coerce numeric fields defensively; explicit type checks avoid silently
    # accepting bad input that would later corrupt scoring.
    for numeric_field, allowed in (("nakshatra_number", range(1, 28)), ("rashi_number", range(1, 13))):
        value = normalized.get(numeric_field)
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int):
            missing.append(f"{label}.{numeric_field}")
            normalized[numeric_field] = None
            continue
        if value not in allowed:
            missing.append(f"{label}.{numeric_field}")

    return normalized, missing


def _ensure_required_fields(boy: Dict[str, Any], girl: Dict[str, Any]) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for label, person in (("boy", boy), ("girl", girl)):
        for koot_name, required_fields in REQUIRED_FIELDS.items():
            for field in required_fields:
                if person.get(field) is None:
                    missing.append(f"{label}.{field} ({koot_name})")
    # de-duplicate while preserving order
    unique_missing = list(dict.fromkeys(missing))
    return len(unique_missing) == 0, unique_missing


def calculate_ashtakoot_milan(boy_attributes: Dict[str, Any], girl_attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate Ashtakoot Milan using already-derived attributes.

    Returns:
        Success dict with boy/girl echoes and koot breakdown, or
        an error dict with code/message/missing_fields.
    """
    boy, boy_missing = _validate_person_attributes(boy_attributes or {}, "boy")
    girl, girl_missing = _validate_person_attributes(girl_attributes or {}, "girl")

    missing_fields = list(dict.fromkeys(boy_missing + girl_missing))
    ok, missing_required = _ensure_required_fields(boy, girl)
    missing_fields.extend([f for f in missing_required if f not in missing_fields])

    if missing_fields:
        return {
            "error": {
                "code": "MISSING_ATTRIBUTES",
                "message": "One or more required attributes are missing or invalid for Ashtakoot calculation",
                "missing_fields": missing_fields,
            }
        }

    try:
        koot_results, total = AshtakootCalculator.calculate_all_koots(boy, girl)
    except KeyError as exc:
        return {
            "error": {
                "code": "INCOMPLETE_ATTRIBUTES",
                "message": f"Scoring failed because a required attribute was unavailable: {exc}",
                "missing_fields": [str(exc)],
            }
        }
    except Exception as exc:
        logger.exception("Unexpected failure while calculating Ashtakoot")
        return {
            "error": {
                "code": "CALCULATION_ERROR",
                "message": "Unexpected error while calculating Ashtakoot Milan",
                "missing_fields": None,
            }
        }

    return {
        "success": True,
        "boy": boy,
        "girl": girl,
        "ashtakoot": {
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
        },
    }


def build_sample_response() -> Dict[str, Any]:
    """Example payload for documentation and testing."""
    return {
        "boy": {
            "name": "विराट",
            "nakshatra": "Vishakha",
            "nakshatra_number": 16,
            "rashi": "Tula",
            "rashi_number": 7,
            "gana": "Manav",
            "yoni": "Vyaghra",
            "nadi": "Adi",
            "varna": "Shudra",
            "vashya": "Manav",
            "rashi_lord": "Shukra",
            "nakshatra_lord": "Guru",
        },
        "girl": {
            "name": "काव्या",
            "nakshatra": "Krittika",
            "nakshatra_number": 3,
            "rashi": "Mesh",
            "rashi_number": 1,
            "gana": "Rakshasa",
            "yoni": "Mesha",
            "nadi": "Antya",
            "varna": "Kshatriya",
            "vashya": "Chatushpad",
            "rashi_lord": "Mangal",
            "nakshatra_lord": "Surya",
        },
        "ashtakoot": {
            "varna": 0,
            "vashya": 0,
            "tara": 0,
            "yoni": 2,
            "graha_maitri": 3,
            "gana": 0,
            "bhakoot": 7,
            "nadi": 8,
            "total": 20,
            "max": 36,
        },
    }