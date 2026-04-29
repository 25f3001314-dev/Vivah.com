# -*- coding: utf-8 -*-
"""
Ashtakoot Milan Service
Core business logic for Vedic matchmaking and compatibility calculations.

This service:
1. Extracts first syllable from names
2. Maps syllables to Nakshatra and Rashi using open-source libraries or traditional mappings
3. Calculates all 8 Koots (matching criteria)
4. Generates compatibility scores and recommendations
"""

from typing import Optional, Tuple, Dict, Any
import logging

from ..utils import (
    normalize_devanagari,
    extract_first_syllable,
    get_nakshatra_from_syllable,
    validate_name,
)
from ..utils.constants import (
    NAKSHATRA_TO_NUMBER,
    RASHI_TO_NUMBER,
    RASHI_LORDS,
    NAKSHATRA_LORDS,
    NAKSHATRA_GANA,
    NAKSHATRA_YONI,
    RASHI_VARNA,
    RASHI_VASHYA,
    NAKSHATRA_NADI,
    VARNA_RANK,
)

logger = logging.getLogger(__name__)
# Prefer an encapsulated adapter for external astrology libraries (PyJHora-like)
from .pyjhora_adapter import adapter as pyjhora_adapter

# Legacy: try to import `jyotisha` if available. The adapter will be checked first
try:
    from jyotisha.panchaanga.temporal.names import get_nakshatra_from_name  # type: ignore
    JYOTISHA_AVAILABLE = True
except Exception:
    JYOTISHA_AVAILABLE = False
    logger.debug("jyotisha not available; adapter will be used if present")


class PersonAstrologyProfile:
    """Represents the astrological profile of a person based on their name."""

    def __init__(self, name: str):
        self.name = normalize_devanagari(name)
        self.first_syllable: Optional[str] = None
        self.nakshatra: Optional[str] = None
        self.rashi: Optional[str] = None
        self.nakshatra_number: Optional[int] = None
        self.rashi_number: Optional[int] = None
        self.gana: Optional[str] = None
        self.yoni: Optional[Tuple[str, str]] = None
        self.varna: Optional[str] = None
        self.vashya: Optional[str] = None
        self.nadi: Optional[str] = None
        self.rashi_lord: Optional[str] = None
        self.nakshatra_lord: Optional[str] = None
        self.source: str = "unknown"

    def extract_profile(self) -> Dict[str, Any]:
        """
        Extract complete astrological profile from the person's name.
        
        Returns:
            Dictionary with profile data or error key
        """
        # Validate name
        is_valid, error = validate_name(self.name)
        if not is_valid:
            return {"error": error}

        # Extract first syllable
        self.first_syllable = extract_first_syllable(self.name)
        if not self.first_syllable:
            return {"error": f"Could not extract syllable from '{self.name}'"}

        # Try external adapter (PyJHora-like) first.
        # Adapter-provided fields: nakshatra name and (if supported) pada/personalized mapping.
        if pyjhora_adapter and getattr(pyjhora_adapter, "available", False):
            try:
                # Adapter may support name->nakshatra directly
                if getattr(pyjhora_adapter, "supports_name_to_nakshatra", False):
                    try:
                        result = self._extract_using_adapter()
                        if result and "error" not in result:
                            self.source = "pyjhora"
                            return result
                    except Exception:
                        logger.warning("pyjhora adapter failed; trying jyotisha fallback", exc_info=True)

                # If adapter lacks name->nakshatra but we have jyotisha, try it next
                if JYOTISHA_AVAILABLE:
                    try:
                        result = self._extract_using_jyotisha()
                        if result and "error" not in result:
                            self.source = "jyotisha"
                            return result
                    except Exception:
                        logger.warning("jyotisha failed after adapter; falling back to Barahadi", exc_info=True)

            except Exception:
                logger.warning("Adapter flow failed; falling back to Barahadi", exc_info=True)
        else:
            # No adapter; try legacy jyotisha if installed
            if JYOTISHA_AVAILABLE:
                try:
                    result = self._extract_using_jyotisha()
                    if result and "error" not in result:
                        self.source = "jyotisha"
                        return result
                except Exception:
                    logger.warning("jyotisha error: falling back to Barahadi", exc_info=True)

        # Fallback to Barahadi traditional mapping
        result = self._extract_using_barahadi()
        if result and "error" not in result:
            self.source = "barahadi"
        return result

    def _extract_using_jyotisha(self) -> Optional[Dict[str, Any]]:
        """
        Extract Nakshatra using jyotisha library.
        This library provides accurate astronomical calculations.
        
        Reference: https://github.com/V1Europe/jyotisha
        """
        try:
            # Legacy: jyotisha's get_nakshatra_from_name returns (nakshatra_name, pada)
            result = get_nakshatra_from_name(name=self.name)

            if not result:
                return None

            nakshatra_name, pada = result

            # Map to our internal format
            self.nakshatra = nakshatra_name
            self.nakshatra_number = NAKSHATRA_TO_NUMBER.get(nakshatra_name)

            if not self.nakshatra_number:
                logger.error(f"Unknown Nakshatra: {nakshatra_name}")
                return None

            # Get Rashi from Nakshatra using our mappings
            # (Rashi is not directly from jyotisha for names, calculated from nakshatra)
            self._derive_rashi_and_attributes()

            return self._build_profile_dict()
        
        except Exception as e:
            logger.error(f"jyotisha extraction error: {e}")
            return None

    def _extract_using_adapter(self) -> Optional[Dict[str, Any]]:
        """Use the PyJHora adapter (if available) to extract nakshatra from name.

        Fields derived via adapter: `nakshatra` and possibly `nakshatra_number`/`pada`.
        Remaining attributes (rashi, gana, yoni, varna, vashya, nadi) are derived
        using our internal mappings/fallbacks based on the adapter's nakshatra.
        """
        try:
            # Adapter may return (nakshatra_name, pada) or similar
            result = pyjhora_adapter.get_nakshatra_from_name(self.name)
            if not result:
                return None

            # Adapter contracts may vary; accept (name, pada) or (name, number)
            nakshatra_name = None
            nak_number = None
            if isinstance(result, tuple) and len(result) >= 1:
                nakshatra_name = result[0]
                if len(result) >= 2 and isinstance(result[1], int):
                    nak_number = result[1]

            if not nakshatra_name:
                return None

            self.nakshatra = nakshatra_name
            # Try to map to our internal number; if adapter provided number use it
            if nak_number:
                self.nakshatra_number = nak_number
            else:
                self.nakshatra_number = NAKSHATRA_TO_NUMBER.get(nakshatra_name)

            if not self.nakshatra_number:
                logger.warning(f"Adapter returned nakshatra '{nakshatra_name}' but mapping to number failed")

            # Derive the rest using our mapping layer
            self._derive_attributes()
            return self._build_profile_dict()
        except Exception as e:
            logger.warning(f"Adapter extraction failed: {e}", exc_info=True)
            return None

    def _extract_using_barahadi(self) -> Dict[str, Any]:
        """
        Extract Nakshatra using traditional Barahadi (syllable) mapping.
        This is the fallback method based on classical Jyotish systems.
        
        Reference: Traditional Barahadi syllable-to-Rashi mapping
        """
        syllable_data = get_nakshatra_from_syllable(self.first_syllable)
        
        if not syllable_data:
            return {"error": f"Syllable '{self.first_syllable}' not found in Barahadi mapping"}
        
        # Unpack syllable data: (Nakshatra, Rashi, Nakshatra_Number, Rashi_Number)
        self.nakshatra, self.rashi, self.nakshatra_number, self.rashi_number = syllable_data
        
        # Derive all other attributes
        self._derive_attributes()
        
        return self._build_profile_dict()

    def _derive_rashi_and_attributes(self):
        """Derive Rashi and related attributes when using jyotisha library."""
        # For now, use a simplified formula based on Nakshatra number
        # Each Rashi contains approximately 2.25 Nakshatras
        rashi_num = ((self.nakshatra_number - 1) // 2) + 1
        self.rashi_number = min(rashi_num, 12)
        
        # Map Rashi number to name
        rashi_map = {
            1: "Mesh", 2: "Vrishabh", 3: "Mithun", 4: "Kark", 5: "Simha", 6: "Kanya",
            7: "Tula", 8: "Vrishchik", 9: "Dhanu", 10: "Makar", 11: "Kumbh", 12: "Meen"
        }
        self.rashi = rashi_map.get(self.rashi_number, "Unknown")
        
        self._derive_attributes()

    def _derive_attributes(self):
        """Derive Gana, Yoni, Varna, Vashya, Nadi from Nakshatra and Rashi."""
        # Gana (Temperament) - from Nakshatra
        self.gana = NAKSHATRA_GANA.get(self.nakshatra, "Manav")
        
        # Yoni (Animal nature) - from Nakshatra
        yoni_tuple = NAKSHATRA_YONI.get(self.nakshatra, ("Unknown", "M"))
        self.yoni = yoni_tuple
        
        # Varna (Class) - from Rashi
        self.varna = RASHI_VARNA.get(self.rashi, "Shudra")
        
        # Vashya (Dominion) - from Rashi
        self.vashya = RASHI_VASHYA.get(self.rashi, "Manav")
        
        # Nadi (Nerve energy) - from Nakshatra
        self.nadi = NAKSHATRA_NADI.get(self.nakshatra_number, "Adi")
        
        # Rashi Lord (Planet) - from Rashi
        self.rashi_lord = RASHI_LORDS.get(self.rashi, "Unknown")
        
        # Nakshatra Lord (Planet) - from Nakshatra number
        self.nakshatra_lord = NAKSHATRA_LORDS.get(self.nakshatra_number, "Unknown")

    def _build_profile_dict(self) -> Dict[str, Any]:
        """Build the complete profile as a dictionary."""
        if not self.nakshatra or not self.rashi:
            return {"error": "Failed to determine Nakshatra/Rashi"}

        return {
            "name": self.name,
            "first_syllable": self.first_syllable,
            "nakshatra": self.nakshatra,
            "nakshatra_number": self.nakshatra_number,
            "rashi": self.rashi,
            "rashi_number": self.rashi_number,
            "gana": self.gana,
            "yoni": self.yoni[0] if self.yoni else "Unknown",
            "yoni_gender": self.yoni[1] if self.yoni else "M",
            "varna": self.varna,
            "vashya": self.vashya,
            "nadi": self.nadi,
            "rashi_lord": self.rashi_lord,
            "nakshatra_lord": self.nakshatra_lord,
            "first_syllable": self.first_syllable,
            "source": self.source,
        }


class AshtakootCalculator:
    """Calculates the 8 Koots (compatibility criteria) for Ashtakoot Milan."""

    # Koot names and their respective functions
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

    @staticmethod
    def calculate_varna(boy_rashi: str, girl_rashi: str) -> float:
        """
        Varna Koot (1 point max)
        Boy's Varna should be equal or higher than girl's.
        """
        boy_varna = RASHI_VARNA.get(boy_rashi, "Shudra")
        girl_varna = RASHI_VARNA.get(girl_rashi, "Shudra")
        
        boy_rank = VARNA_RANK.get(boy_varna, 0)
        girl_rank = VARNA_RANK.get(girl_varna, 0)
        
        return 1.0 if boy_rank >= girl_rank else 0.0

    @staticmethod
    def calculate_vashya(boy_rashi: str, girl_rashi: str) -> float:
        """
        Vashya Koot (2 points max)
        Checks dominion compatibility between Rashis.
        """
        boy_vashya = RASHI_VASHYA.get(boy_rashi, "Manav")
        girl_vashya = RASHI_VASHYA.get(girl_rashi, "Manav")
        
        if boy_vashya == girl_vashya:
            return 2.0
        
        # Compatibility matrix
        vashya_compat = {
            "Chatushpad": ["Chatushpad", "Manav"],
            "Manav": ["Manav", "Jalachara", "Vanchar"],
            "Jalachara": ["Jalachara", "Manav"],
            "Vanchar": ["Vanchar", "Chatushpad"],
            "Keeta": ["Keeta", "Jalachara"],
        }
        
        if girl_vashya in vashya_compat.get(boy_vashya, []):
            return 1.0
        
        return 0.0

    @staticmethod
    def calculate_tara(boy_nak_num: int, girl_nak_num: int) -> float:
        """
        Tara Koot (3 points max)
        Based on Nakshatra positions. 
        Auspicious Taras: 2, 4, 6, 8, 9
        """
        diff = (girl_nak_num - boy_nak_num) % 27
        if diff == 0:
            diff = 27
        tara = ((diff - 1) % 9) + 1
        
        auspicious_taras = {2, 4, 6, 8, 9}
        return 3.0 if tara in auspicious_taras else 0.0

    @staticmethod
    def calculate_yoni(boy_nakshatra: str, girl_nakshatra: str) -> float:
        """
        Yoni Koot (4 points max)
        Compatibility based on animal nature.
        """
        boy_yoni_data = NAKSHATRA_YONI.get(boy_nakshatra, ("Unknown", "M"))
        girl_yoni_data = NAKSHATRA_YONI.get(girl_nakshatra, ("Unknown", "F"))
        
        boy_yoni, boy_gender = boy_yoni_data
        girl_yoni, girl_gender = girl_yoni_data
        
        if boy_yoni == girl_yoni:
            if boy_gender != girl_gender:
                return 4.0  # Same Yoni, opposite gender
            else:
                return 3.0  # Same Yoni, same gender
        
        # Yoni enemies
        yoni_enemies = {
            ("Ashwa", "Mahisha"), ("Gaja", "Simha"), ("Mesha", "Vanara"),
            ("Sarpa", "Nakula"), ("Shwan", "Mriga"), ("Marjara", "Mushaka"),
            ("Mahisha", "Ashwa"), ("Simha", "Gaja"), ("Vanara", "Mesha"),
            ("Nakula", "Sarpa"), ("Mriga", "Shwan"), ("Mushaka", "Marjara"),
        }
        
        if (boy_yoni, girl_yoni) in yoni_enemies or (girl_yoni, boy_yoni) in yoni_enemies:
            return 0.0
        
        return 2.0

    @staticmethod
    def calculate_graha_maitri(boy_rl: str, girl_rl: str) -> float:
        """
        Graha Maitri Koot (5 points max)
        Compatibility between planetary lords.
        """
        # Planetary friendship matrix
        graha_maitri = {
            "Surya": {"Mitra": ["Chandra", "Mangal", "Guru"], "Shatru": ["Shukra", "Shani"], "Sam": ["Budh"]},
            "Chandra": {"Mitra": ["Surya", "Budh"], "Shatru": [], "Sam": ["Mangal", "Guru", "Shukra", "Shani"]},
            "Mangal": {"Mitra": ["Surya", "Chandra", "Guru"], "Shatru": ["Budh"], "Sam": ["Shukra", "Shani"]},
            "Budh": {"Mitra": ["Surya", "Shukra"], "Shatru": ["Chandra"], "Sam": ["Mangal", "Guru", "Shani"]},
            "Guru": {"Mitra": ["Surya", "Chandra", "Mangal"], "Shatru": ["Budh", "Shukra"], "Sam": ["Shani"]},
            "Shukra": {"Mitra": ["Budh", "Shani"], "Shatru": ["Surya", "Chandra"], "Sam": ["Mangal", "Guru"]},
            "Shani": {"Mitra": ["Budh", "Shukra"], "Shatru": ["Surya", "Chandra", "Mangal"], "Sam": ["Guru"]},
            "Rahu": {"Mitra": ["Shukra", "Shani"], "Shatru": ["Surya", "Chandra", "Mangal"], "Sam": ["Guru", "Budh"]},
            "Ketu": {"Mitra": ["Mangal", "Shukra", "Shani"], "Shatru": ["Surya", "Chandra"], "Sam": ["Guru", "Budh"]},
        }

        def get_relation(lord1: str, lord2: str) -> str:
            relations = graha_maitri.get(lord1, {})
            if lord2 in relations.get("Mitra", []):
                return "Mitra"
            if lord2 in relations.get("Shatru", []):
                return "Shatru"
            return "Sam"

        r_boy_girl = get_relation(boy_rl, girl_rl)
        r_girl_boy = get_relation(girl_rl, boy_rl)
        
        if r_boy_girl == "Mitra" and r_girl_boy == "Mitra":
            return 5.0
        if ("Mitra" in [r_boy_girl, r_girl_boy]) and ("Sam" in [r_boy_girl, r_girl_boy]):
            return 4.0
        if r_boy_girl == "Sam" and r_girl_boy == "Sam":
            return 3.0
        if ("Shatru" in [r_boy_girl, r_girl_boy]) and ("Mitra" in [r_boy_girl, r_girl_boy]):
            return 1.0
        if ("Shatru" in [r_boy_girl, r_girl_boy]) and ("Sam" in [r_boy_girl, r_girl_boy]):
            return 0.5
        if r_boy_girl == "Shatru" and r_girl_boy == "Shatru":
            return 0.0
        
        return 2.0

    @staticmethod
    def calculate_gana(boy_nakshatra: str, girl_nakshatra: str) -> float:
        """
        Gana Koot (6 points max)
        Compatibility based on temperament (Deva, Manav, Rakshasa).
        """
        boy_gana = NAKSHATRA_GANA.get(boy_nakshatra, "Manav")
        girl_gana = NAKSHATRA_GANA.get(girl_nakshatra, "Manav")
        
        gana_scores = {
            ("Deva", "Deva"): 6.0, ("Manav", "Manav"): 6.0, ("Rakshasa", "Rakshasa"): 6.0,
            ("Deva", "Manav"): 5.0, ("Manav", "Deva"): 5.0,
            ("Manav", "Rakshasa"): 0.0, ("Rakshasa", "Manav"): 0.0,
            ("Deva", "Rakshasa"): 1.0, ("Rakshasa", "Deva"): 1.0,
        }
        
        return gana_scores.get((boy_gana, girl_gana), 0.0)

    @staticmethod
    def calculate_bhakoot(boy_rashi_num: int, girl_rashi_num: int) -> float:
        """
        Bhakoot Koot (7 points max)
        Compatibility based on Rashi positions.
        Inauspicious positions: 2-12, 3-11, 4-10, 6
        """
        diff1 = ((girl_rashi_num - boy_rashi_num) % 12) + 1
        diff2 = ((boy_rashi_num - girl_rashi_num) % 12) + 1
        
        # Check inauspicious positions
        for d in [diff1, diff2]:
            if d in [2, 12, 3, 11, 4, 10, 6]:
                return 0.0
        
        # Auspicious positions
        if (diff1 in [5, 9] and diff2 in [5, 9]) or diff1 == 1 or diff2 == 1:
            return 7.0
        
        return 7.0

    @staticmethod
    def calculate_nadi(boy_nakshatra_num: int, girl_nakshatra_num: int) -> float:
        """
        Nadi Koot (8 points max)
        Same Nadi is considered inauspicious.
        """
        boy_nadi = NAKSHATRA_NADI.get(boy_nakshatra_num, "Adi")
        girl_nadi = NAKSHATRA_NADI.get(girl_nakshatra_num, "Adi")
        
        return 0.0 if boy_nadi == girl_nadi else 8.0

    @classmethod
    def calculate_all_koots(
        cls,
        boy_profile: Dict[str, Any],
        girl_profile: Dict[str, Any],
    ) -> Tuple[list, float]:
        """
        Calculate all 8 Koots.
        
        Returns:
            (list of koot scores, total score)
        """
        koot_results = []
        total = 0.0

        # Varna
        score = cls.calculate_varna(boy_profile["rashi"], girl_profile["rashi"])
        koot_results.append(("Varna", 1, score, 1.0))
        total += score

        # Vashya
        score = cls.calculate_vashya(boy_profile["rashi"], girl_profile["rashi"])
        koot_results.append(("Vashya", 2, score, 2.0))
        total += score

        # Tara
        score = cls.calculate_tara(boy_profile["nakshatra_number"], girl_profile["nakshatra_number"])
        koot_results.append(("Tara", 3, score, 3.0))
        total += score

        # Yoni
        score = cls.calculate_yoni(boy_profile["nakshatra"], girl_profile["nakshatra"])
        koot_results.append(("Yoni", 4, score, 4.0))
        total += score

        # Graha Maitri
        score = cls.calculate_graha_maitri(boy_profile["rashi_lord"], girl_profile["rashi_lord"])
        koot_results.append(("Graha Maitri", 5, score, 5.0))
        total += score

        # Gana
        score = cls.calculate_gana(boy_profile["nakshatra"], girl_profile["nakshatra"])
        koot_results.append(("Gana", 6, score, 6.0))
        total += score

        # Bhakoot
        score = cls.calculate_bhakoot(boy_profile["rashi_number"], girl_profile["rashi_number"])
        koot_results.append(("Bhakoot", 7, score, 7.0))
        total += score

        # Nadi
        score = cls.calculate_nadi(boy_profile["nakshatra_number"], girl_profile["nakshatra_number"])
        koot_results.append(("Nadi", 8, score, 8.0))
        total += score

        return koot_results, total


def perform_ashtakoot_milan(boy_name: str, girl_name: str) -> Dict[str, Any]:
    """
    Perform complete Ashtakoot Milan matching.
    
    Args:
        boy_name: Boy's name in Devanagari
        girl_name: Girl's name in Devanagari
    
    Returns:
        Dictionary with matching results or error
    """
    # Extract profiles
    boy_profile_obj = PersonAstrologyProfile(boy_name)
    boy_profile = boy_profile_obj.extract_profile()
    
    if "error" in boy_profile:
        return {"error": f"Boy's profile: {boy_profile['error']}"}

    girl_profile_obj = PersonAstrologyProfile(girl_name)
    girl_profile = girl_profile_obj.extract_profile()
    
    if "error" in girl_profile:
        return {"error": f"Girl's profile: {girl_profile['error']}"}

    # Calculate Koots
    koot_results, total_score = AshtakootCalculator.calculate_all_koots(boy_profile, girl_profile)

    # Compatibility percentage
    compatibility_percentage = (total_score / 36) * 100

    # Result status
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

    # Check doshas
    doshas = []
    if koot_results[7][2] == 0:  # Nadi = 0
        doshas.append("नाड़ी दोष - स्वास्थ्य संबंधी समस्या हो सकती है")
    if koot_results[6][2] == 0:  # Bhakoot = 0
        doshas.append("भाकूट दोष - वैवाहिक जीवन में कठिनाई हो सकती है")
    if koot_results[5][2] == 0:  # Gana = 0
        doshas.append("गण दोष - स्वभाव में असंगति हो सकती है")

    recommendations = []
    if total_score < 18:
        recommendations.append("योग्य पंडित से परामर्श लें")
    if "नाड़ी दोष" in doshas:
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
