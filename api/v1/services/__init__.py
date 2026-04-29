# -*- coding: utf-8 -*-
"""Service compatibility layer for Ashtakoot Milan.

This module keeps legacy imports stable while delegating core logic to
`v1.astrology`.
"""

from __future__ import annotations

from typing import Any, Dict

from ..astrology import AshtakootCalculator, PersonAstrologyProfile


def perform_ashtakoot_milan(boy_name: str, girl_name: str) -> Dict[str, Any]:
    """Perform complete Ashtakoot Milan matching.

    Public response shape is preserved for existing API consumers.
    """
    boy_profile_obj = PersonAstrologyProfile(boy_name)
    boy_profile = boy_profile_obj.extract_profile()
    if "error" in boy_profile:
        return {"error": f"Boy's profile: {boy_profile['error']}"}

    girl_profile_obj = PersonAstrologyProfile(girl_name)
    girl_profile = girl_profile_obj.extract_profile()
    if "error" in girl_profile:
        return {"error": f"Girl's profile: {girl_profile['error']}"}

    koot_results, total_score = AshtakootCalculator.calculate_all_koots(boy_profile, girl_profile)
    compatibility_percentage = (total_score / 36.0) * 100.0

    if total_score >= 32:
        result_status = "Excellent"
        result_interpretation = "अत्यंत शुभ विवाह - विवाह अत्यंत शुभ है"
    elif total_score >= 24:
        result_status = "Good"
        result_interpretation = "शुभ विवाह - विवाह किया जा सकता है"
    elif total_score >= 18:
        result_status = "Average"
        result_interpretation = "औसत संगति - सोच समझकर निर्णय लें"
    else:
        result_status = "Poor"
        result_interpretation = "अशुभ विवाह - विवाह अनुकूल नहीं है"

    doshas = []
    if koot_results[7][2] == 0:
        doshas.append("नाड़ी दोष - स्वास्थ्य संबंधी समस्या हो सकती है")
    if koot_results[6][2] == 0:
        doshas.append("भाकूट दोष - वैवाहिक जीवन में कठिनाई हो सकती है")
    if koot_results[5][2] == 0:
        doshas.append("गण दोष - स्वभाव में असंगति हो सकती है")

    recommendations = []
    if total_score < 18:
        recommendations.append("योग्य पंडित से परामर्श लें")
    if any("नाड़ी दोष" in d for d in doshas):
        recommendations.append("नाड़ी दोष के निवारण के लिए उपाय करें")

    return {
        "boy_name": boy_name,
        "girl_name": girl_name,
        "boy_profile": boy_profile,
        "girl_profile": girl_profile,
        "koot_results": koot_results,
        "total_score": round(total_score, 1),
        "compatibility_percentage": round(compatibility_percentage, 1),
        "result_status": result_status,
        "result_interpretation": result_interpretation,
        "doshas": doshas,
        "recommendations": recommendations,
    }


__all__ = [
    "AshtakootCalculator",
    "PersonAstrologyProfile",
    "perform_ashtakoot_milan",
]
