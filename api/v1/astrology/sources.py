# -*- coding: utf-8 -*-
"""Verified source resolution for name -> astrology attributes.

Source order: jyotisha -> pyjhora -> barahadi.
"""

from __future__ import annotations

import importlib
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..utils import extract_first_syllable, get_nakshatra_from_syllable
from ..utils.constants import NAKSHATRA_TO_NUMBER

logger = logging.getLogger(__name__)

Provider = Callable[[str], Optional[Dict[str, Any]]]


def _barahadi_provider(name: str) -> Optional[Dict[str, Any]]:
    first_syllable = extract_first_syllable(name)
    if not first_syllable:
        return None
    mapping = get_nakshatra_from_syllable(first_syllable)
    if not mapping:
        return None
    nakshatra, rashi, nak_num, rashi_num = mapping
    return {
        "first_syllable": first_syllable,
        "nakshatra": nakshatra,
        "nakshatra_number": nak_num,
        "rashi": rashi,
        "rashi_number": rashi_num,
        "pada": None,
    }


def _verify_jyotisha() -> Optional[Provider]:
    try:
        mod = importlib.import_module("jyotisha.panchaanga.temporal.names")
    except Exception:
        return None

    fn = getattr(mod, "get_nakshatra_from_name", None)
    if not callable(fn):
        return None

    try:
        probe = fn(name="राम")
    except Exception:
        return None

    if not probe or not isinstance(probe, tuple):
        return None

    def provider(name: str) -> Optional[Dict[str, Any]]:
        try:
            value = fn(name=name)
        except Exception:
            return None
        if not value or not isinstance(value, tuple):
            return None
        nakshatra = value[0]
        pada = value[1] if len(value) > 1 and isinstance(value[1], int) else None
        nak_num = NAKSHATRA_TO_NUMBER.get(nakshatra)
        if not nak_num:
            return None
        return {
            "first_syllable": None,
            "nakshatra": nakshatra,
            "nakshatra_number": nak_num,
            "rashi": None,
            "rashi_number": None,
            "pada": pada,
        }

    return provider


def _verify_pyjhora() -> Optional[Provider]:
    for module_name in ("pyjhora", "PyJHora", "jhora", "jyotisha_jhora"):
        try:
            mod = importlib.import_module(module_name)
        except Exception:
            continue

        fn = getattr(mod, "get_nakshatra_from_name", None)
        if not callable(fn):
            continue

        try:
            probe = fn("राम")
        except Exception:
            continue

        if not probe:
            continue

        def provider(name: str, func: Callable[..., Any] = fn) -> Optional[Dict[str, Any]]:
            try:
                value = func(name)
            except Exception:
                return None
            if not value or not isinstance(value, tuple):
                return None
            nakshatra = value[0]
            pada = value[1] if len(value) > 1 and isinstance(value[1], int) else None
            nak_num = NAKSHATRA_TO_NUMBER.get(nakshatra)
            if not nak_num:
                return None
            return {
                "first_syllable": None,
                "nakshatra": nakshatra,
                "nakshatra_number": nak_num,
                "rashi": None,
                "rashi_number": None,
                "pada": pada,
            }

        return provider

    return None


class SourceResolver:
    """Runtime-verified provider chain with stable source tagging."""

    def __init__(self) -> None:
        self._providers: List[Tuple[str, Provider]] = []

        jyotisha_provider = _verify_jyotisha()
        if jyotisha_provider:
            self._providers.append(("jyotisha", jyotisha_provider))
        else:
            logger.debug("jyotisha provider disabled by probe")

        pyjhora_provider = _verify_pyjhora()
        if pyjhora_provider:
            self._providers.append(("pyjhora", pyjhora_provider))
        else:
            logger.debug("pyjhora provider disabled by probe")

        self._providers.append(("barahadi", _barahadi_provider))

    def resolve(self, name: str) -> Tuple[Dict[str, Any], str]:
        for tag, provider in self._providers:
            try:
                result = provider(name)
            except Exception:
                logger.warning("provider %s failed", tag, exc_info=True)
                continue
            if result:
                return result, tag
        raise ValueError(f"Could not resolve astrology profile for '{name}'")


resolver = SourceResolver()
