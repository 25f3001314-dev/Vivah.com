# -*- coding: utf-8 -*-
"""Adapter wrapper for the PyJHora (or similar) library.

This module attempts to import a community Jyotish library (PyJHora / pyjhora)
and exposes a small, well-defined surface that the rest of the application
can use. It performs capability detection at import time and never raises
ImportError to callers — instead `available` will be False and methods will
return `None` when the library cannot provide a value.

Design goals:
- Keep library usage encapsulated in one module
- Provide clear capability flags (name->nakshatra, rashi, etc.)
- Offer robust exception handling and do not fake unsupported features
"""

from __future__ import annotations

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class PyJHoraAdapter:
    """Detects and wraps PyJHora-like library features.

    Attributes:
        available: Whether any candidate library was imported
        supports_name_to_nakshatra: Whether name->nakshatra lookup exists
        supports_astro_calculations: Whether longitude/rashi calculations exist
    """

    def __init__(self) -> None:
        self.available = False
        self.supports_name_to_nakshatra = False
        self.supports_astro_calculations = False
        self._lib = None

        # Try candidate import names for PyJHora-like libraries
        candidates = ["pyjhora", "PyJHora", "jhora", "jyotisha_jhora"]
        for name in candidates:
            try:
                module = __import__(name)
                self._lib = module
                self.available = True
                logger.info(f"Loaded astrology library '{name}'")
                break
            except Exception:
                continue

        if not self.available:
            logger.info("No PyJHora-like library available; falling back to Barahadi mapping")
            return

        # Capability detection: check for functions commonly provided
        # by name-based helpers or panchaanga-style APIs
        try:
            # Example expected API: module.get_nakshatra_from_name(name) -> (nakshatra, pada)
            if hasattr(self._lib, "get_nakshatra_from_name"):
                self.supports_name_to_nakshatra = True
        except Exception:
            logger.debug("Failed to detect name->nakshatra capability", exc_info=True)

        try:
            # Example expected API: module.calculate_rashi_from_longitude(lon) or panchaanga helpers
            if hasattr(self._lib, "calculate_rashi_from_longitude") or hasattr(self._lib, "get_rashi_from_longitude"):
                self.supports_astro_calculations = True
        except Exception:
            logger.debug("Failed to detect astro calculation capability", exc_info=True)

    def get_nakshatra_from_name(self, name: str) -> Optional[Tuple[str, int]]:
        """Attempt to get nakshatra (name, pada) from the library using a name.

        Returns a tuple (nakshatra_name, pada) if available, otherwise None.
        """
        if not self.available or not self.supports_name_to_nakshatra:
            return None

        try:
            # Attempt a few common function names
            if hasattr(self._lib, "get_nakshatra_from_name"):
                return self._lib.get_nakshatra_from_name(name)
            if hasattr(self._lib, "nakshatra_from_name"):
                return self._lib.nakshatra_from_name(name)
        except Exception as e:
            logger.warning(f"PyJHora adapter: name->nakshatra call failed: {e}")
        return None

    def get_rashi_from_longitude(self, longitude: float) -> Optional[str]:
        """Attempt to derive Rashi name from a longitude value via the library.

        Returns the rashi name or None.
        """
        if not self.available or not self.supports_astro_calculations:
            return None

        try:
            if hasattr(self._lib, "get_rashi_from_longitude"):
                return self._lib.get_rashi_from_longitude(longitude)
            if hasattr(self._lib, "calculate_rashi_from_longitude"):
                return self._lib.calculate_rashi_from_longitude(longitude)
        except Exception as e:
            logger.warning(f"PyJHora adapter: rashi-from-longitude failed: {e}")
        return None


# Singleton instance used by services
adapter = PyJHoraAdapter()


def has_library() -> bool:
    return adapter.available


def supports_name_lookup() -> bool:
    return adapter.supports_name_to_nakshatra


def supports_astro() -> bool:
    return adapter.supports_astro_calculations
