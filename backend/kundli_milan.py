# -*- coding: utf-8 -*-
"""
NAAM SE VIVAH — Backend logic
Naam ke pehle akshar se Rashi/Nakshatra nikalna + Ashtakoot Milan

Fixed small bugs:
- corrected Tara scoring logic
- normalized Nakshatra/Yoni key (`Mula`) to match other mappings

Run as: `python3 backend/kundli_milan.py`
"""

# ─────────────────────────────────────────────
# (Code provided by user, lightly cleaned and bug-fixed)
# ─────────────────────────────────────────────

from datetime import datetime, timedelta
import unicodedata
from jyotisha.panchaanga.temporal.names import get_chandra_nakshatra_from_name, get_nakshatra_from_name
from jyotisha.panchaanga.temporal import get_nakshatra_data


try:
    import panchanga.astronomy as p_astro
    import panchanga.horoscope as p_horo
    import panchanga.lunar as p_lunar

    PANCHANGA_AVAILABLE = True
except Exception:
    PANCHANGA_AVAILABLE = False

RASHI_NUMBER = {
    "Mesh (Aries)":         1,
    "Vrishabh (Taurus)":    2,
    "Mithun (Gemini)":      3,
    "Kark (Cancer)":        4,
    "Simha (Leo)":          5,
    "Kanya (Virgo)":        6,
    "Tula (Libra)":         7,
    "Vrishchik (Scorpio)":  8,
    "Dhanu (Sagittarius)":  9,
    "Makar (Capricorn)":   10,
    "Kumbh (Aquarius)":    11,
    "Meen (Pisces)":       12,
}

NAKSHATRA_NUMBER = {
    "Ashwini": 1, "Bharani": 2, "Krittika": 3, "Rohini": 4,
    "Mrigashira": 5, "Ardra": 6, "Punarvasu": 7, "Pushya": 8,
    "Ashlesha": 9, "Magha": 10, "Purva Phalguni": 11, "Uttara Phalguni": 12,
    "Hasta": 13, "Chitra": 14, "Swati": 15, "Vishakha": 16,
    "Anuradha": 17, "Jyeshtha": 18, "Mula": 19, "Purva Ashadha": 20,
    "Uttara Ashadha": 21, "Shravana": 22, "Dhanishtha": 23,
    "Shatabhisha": 24, "Purva Bhadrapada": 25, "Uttara Bhadrapada": 26,
    "Revati": 27,
}

NAKSHATRA_LORDS_ORDER = [
    "Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budh"
]

RASHI_BY_NUMBER = {
    1: "Mesh (Aries)",
    2: "Vrishabh (Taurus)",
    3: "Mithun (Gemini)",
    4: "Kark (Cancer)",
    5: "Simha (Leo)",
    6: "Kanya (Virgo)",
    7: "Tula (Libra)",
    8: "Vrishchik (Scorpio)",
    9: "Dhanu (Sagittarius)",
    10: "Makar (Capricorn)",
    11: "Kumbh (Aquarius)",
    12: "Meen (Pisces)",
}

RASHI_LORD_BY_NAME = {
    "Mesh (Aries)": "Mangal",
    "Vrishabh (Taurus)": "Shukra",
    "Mithun (Gemini)": "Budh",
    "Kark (Cancer)": "Chandra",
    "Simha (Leo)": "Surya",
    "Kanya (Virgo)": "Budh",
    "Tula (Libra)": "Shukra",
    "Vrishchik (Scorpio)": "Mangal",
    "Dhanu (Sagittarius)": "Guru",
    "Makar (Capricorn)": "Shani",
    "Kumbh (Aquarius)": "Shani",
    "Meen (Pisces)": "Guru",
}

PANCHANGA_NAKSHATRA_MAP = {
    "Asvini": "Ashwini",
    "Bharani": "Bharani",
    "Krttika": "Krittika",
    "Rohini": "Rohini",
    "Mrgasira": "Mrigashira",
    "Ardra": "Ardra",
    "Punarvasu": "Punarvasu",
    "Pusya": "Pushya",
    "Aslesa": "Ashlesha",
    "Magha": "Magha",
    "P-phalguni": "Purva Phalguni",
    "U-phalguni": "Uttara Phalguni",
    "Hasta": "Hasta",
    "Citra": "Chitra",
    "Svati": "Swati",
    "Visakha": "Vishakha",
    "Anuradha": "Anuradha",
    "Jyestha": "Jyeshtha",
    "Mula": "Mula",
    "P-asadha": "Purva Ashadha",
    "U-asadha": "Uttara Ashadha",
    "Sravana": "Shravana",
    "Dhanistha": "Dhanishtha",
    "Satabhisaj": "Shatabhisha",
    "P-bhadrapada": "Purva Bhadrapada",
    "U-bhadrapada": "Uttara Bhadrapada",
    "Revati": "Revati",
}

def _parse_timezone_offset(offset_text: str) -> timedelta:
    text = (offset_text or "+00:00").strip()
    if text in {"Z", "+00:00", "-00:00"}:
        return timedelta(0)
    sign = 1
    if text.startswith("-"):
        sign = -1
        text = text[1:]
    elif text.startswith("+"):
        text = text[1:]
    hours_text, _, minutes_text = text.partition(":")
    hours = int(hours_text or 0)
    minutes = int(minutes_text or 0)
    return sign * timedelta(hours=hours, minutes=minutes)

def _build_vedic_birth_info(birth_data: dict) -> dict:
    if not PANCHANGA_AVAILABLE:
        return {"error": "Panchanga library available nahi hai"}

    date_text = (birth_data or {}).get("date", "").strip()
    time_text = (birth_data or {}).get("time", "").strip()
    tz_text = (birth_data or {}).get("timezone", "+00:00").strip()

    if not date_text or not time_text:
        return {"error": "Birth date aur birth time chahiye"}

    try:
        local_dt = datetime.fromisoformat(f"{date_text}T{time_text}")
    except ValueError:
        return {"error": "Birth date/time format galat hai"}

    try:
        utc_dt = local_dt - _parse_timezone_offset(tz_text)
    except Exception:
        return {"error": "Timezone offset format galat hai"}

    julian_day = p_horo.modern_date_to_julian_day(utc_dt.year, utc_dt.month, utc_dt.day)
    ahargana = p_horo.julian_day_to_ahargana(julian_day)
    ahargana = ahargana + utc_dt.hour / 24 + utc_dt.minute / 1440 + utc_dt.second / 86400

    true_lunar_longitude = p_astro.get_true_lunar_longitude(ahargana)
    true_solar_longitude = p_astro.get_true_solar_longitude(ahargana)
    nakshatra_code = p_lunar.get_naksatra_name(true_lunar_longitude)
    nakshatra = PANCHANGA_NAKSHATRA_MAP.get(nakshatra_code, nakshatra_code)
    rashi_number = int(true_lunar_longitude // 30) % 12 + 1
    rashi = RASHI_BY_NUMBER[rashi_number]

    return {
        "source": "panchanga",
        "rashi": rashi,
        "rashi_number": rashi_number,
        "rashi_lord": RASHI_LORD_BY_NAME[rashi],
        "nakshatra": nakshatra,
        "nakshatra_number": NAKSHATRA_NUMBER.get(nakshatra, 0),
        "true_lunar_longitude": round(true_lunar_longitude, 4),
        "true_solar_longitude": round(true_solar_longitude, 4),
    }

# Hindi/Devanagari labels (with English numerals)
KOOT_NAMES_HI = {
    "Varna (1)": "वर्ण (1)",
    "Vashya (2)": "वश्य (2)",
    "Tara (3)": "तारा (3)",
    "Yoni (4)": "योनि (4)",
    "Graha Maitri (5)": "ग्रह मैत्री (5)",
    "Gana (6)": "गण (6)",
    "Bhakoot (7)": "भाकूट (7)",
    "Nadi (8)": "नाड़ी (8)",
}

# VARNA
VARNA = {
    "Mesh (Aries)":        "Kshatriya",
    "Vrishabh (Taurus)":   "Vaishya",
    "Mithun (Gemini)":     "Shudra",
    "Kark (Cancer)":       "Brahmin",
    "Simha (Leo)":         "Kshatriya",
    "Kanya (Virgo)":       "Vaishya",
    "Tula (Libra)":        "Shudra",
    "Vrishchik (Scorpio)": "Brahmin",
    "Dhanu (Sagittarius)": "Kshatriya",
    "Makar (Capricorn)":   "Vaishya",
    "Kumbh (Aquarius)":    "Shudra",
    "Meen (Pisces)":       "Brahmin",
}
VARNA_RANK = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}

def calc_varna(rashi1, rashi2):
    v1 = VARNA_RANK.get(VARNA.get(rashi1, ""), 0)
    v2 = VARNA_RANK.get(VARNA.get(rashi2, ""), 0)
    return 1 if v1 >= v2 else 0

# VASHYA
VASHYA = {
    "Mesh (Aries)":        "Chatushpad",
    "Vrishabh (Taurus)":   "Chatushpad",
    "Mithun (Gemini)":     "Manav",
    "Kark (Cancer)":       "Jalachara",
    "Simha (Leo)":         "Vanchar",
    "Kanya (Virgo)":       "Manav",
    "Tula (Libra)":        "Manav",
    "Vrishchik (Scorpio)": "Keeta",
    "Dhanu (Sagittarius)": "Chatushpad",
    "Makar (Capricorn)":   "Chatushpad",
    "Kumbh (Aquarius)":    "Manav",
    "Meen (Pisces)":       "Jalachara",
}
VASHYA_COMPAT = {
    "Chatushpad": ["Chatushpad", "Manav"],
    "Manav":      ["Manav", "Jalachara", "Vanchar"],
    "Jalachara":  ["Jalachara", "Manav"],
    "Vanchar":    ["Vanchar", "Chatushpad"],
    "Keeta":      ["Keeta", "Jalachara"],
}

def calc_vashya(rashi1, rashi2):
    v1 = VASHYA.get(rashi1, "")
    v2 = VASHYA.get(rashi2, "")
    if v1 == v2:
        return 2
    if v2 in VASHYA_COMPAT.get(v1, []):
        return 1
    return 0

# TARA (fixed scoring)
def calc_tara(nakshatra1_num, nakshatra2_num):
    diff = (nakshatra2_num - nakshatra1_num) % 27
    if diff == 0:
        diff = 27
    tara = ((diff - 1) % 9) + 1
    # According to given note: 2,4,6,8,9 are shubh (auspicious)
    auspicious = {2, 4, 6, 8, 9}
    if tara in auspicious:
        return 3
    return 0

# YONI (normalized key names)
YONI = {
    "Ashwini": ("Ashwa", "M"),    "Shatabhisha": ("Ashwa", "F"),
    "Bharani": ("Gaja", "M"),     "Revati": ("Gaja", "F"),
    "Pushya":  ("Mesha", "M"),    "Krittika": ("Mesha", "F"),
    "Rohini":  ("Sarpa", "M"),    "Mrigashira": ("Sarpa", "F"),
    "Ardra": ("Shwan", "F"),
    "Ashlesha": ("Marjara", "M"),  "Punarvasu": ("Marjara", "F"),
    "Magha":   ("Mushaka", "M"),  "Purva Phalguni": ("Mushaka", "F"),
    "Uttara Phalguni": ("Gau", "M"), "Uttara Bhadrapada": ("Gau", "F"),
    "Swati":   ("Mahisha", "M"),  "Hasta": ("Mahisha", "F"),
    "Vishakha": ("Vyaghra", "M"),  "Chitra": ("Vyaghra", "F"),
    "Jyeshtha": ("Mriga", "M"),    "Anuradha": ("Mriga", "F"),
    "Purva Ashadha": ("Vanara", "M"), "Shravana": ("Vanara", "F"),
    "Purva Bhadrapada": ("Simha","M"), "Dhanishtha": ("Simha","F"),
    "Uttara Ashadha": ("Nakula","M"),  "Mula": ("Nakula","F"),
}

YONI_ENEMIES = {
    ("Ashwa","Mahisha"), ("Gaja","Simha"), ("Mesha","Vanara"),
    ("Sarpa","Nakula"),  ("Shwan","Mriga"), ("Marjara","Mushaka"),
    ("Mahisha","Ashwa"), ("Simha","Gaja"),  ("Vanara","Mesha"),
    ("Nakula","Sarpa"),  ("Mriga","Shwan"), ("Mushaka","Marjara"),
}

def calc_yoni(nakshatra1, nakshatra2):
    y1, g1 = YONI.get(nakshatra1, ("Unknown","M"))
    y2, g2 = YONI.get(nakshatra2, ("Unknown","F"))
    if y1 == y2:
        if g1 != g2:
            return 4
        else:
            return 3
    if (y1, y2) in YONI_ENEMIES or (y2, y1) in YONI_ENEMIES:
        return 0
    return 2

# GRAHA MAITRI
GRAHA_MAITRI = {
    "Surya":   {"Mitra": ["Chandra","Mangal","Guru"],  "Shatru": ["Shukra","Shani"], "Sam": ["Budh"]},
    "Chandra": {"Mitra": ["Surya","Budh"],              "Shatru": [],                 "Sam": ["Mangal","Guru","Shukra","Shani"]},
    "Mangal":  {"Mitra": ["Surya","Chandra","Guru"],   "Shatru": ["Budh"],            "Sam": ["Shukra","Shani"]},
    "Budh":    {"Mitra": ["Surya","Shukra"],            "Shatru": ["Chandra"],         "Sam": ["Mangal","Guru","Shani"]},
    "Guru":    {"Mitra": ["Surya","Chandra","Mangal"], "Shatru": ["Budh","Shukra"],   "Sam": ["Shani"]},
    "Shukra":  {"Mitra": ["Budh","Shani"],              "Shatru": ["Surya","Chandra"], "Sam": ["Mangal","Guru"]},
    "Shani":   {"Mitra": ["Budh","Shukra"],             "Shatru": ["Surya","Chandra","Mangal"], "Sam": ["Guru"]},
    "Rahu":    {"Mitra": ["Shukra","Shani"],            "Shatru": ["Surya","Chandra","Mangal"], "Sam": ["Guru","Budh"]},
    "Ketu":    {"Mitra": ["Mangal","Shukra","Shani"],  "Shatru": ["Surya","Chandra"], "Sam": ["Guru","Budh"]},
}

def relation(lord, other):
    info = GRAHA_MAITRI.get(lord, {})
    if other in info.get("Mitra", []):  return "Mitra"
    if other in info.get("Shatru", []): return "Shatru"
    return "Sam"

def calc_graha_maitri(rashi_lord1, rashi_lord2):
    r12 = relation(rashi_lord1, rashi_lord2)
    r21 = relation(rashi_lord2, rashi_lord1)
    combo = (r12, r21)
    if combo == ("Mitra","Mitra"):      return 5
    if "Mitra" in combo and "Sam" in combo: return 4
    if combo == ("Sam","Sam"):           return 3
    if "Shatru" in combo and "Mitra" in combo: return 1
    if "Shatru" in combo and "Sam" in combo:   return 0.5
    if combo == ("Shatru","Shatru"):    return 0
    return 2

# GANA
GANA = {
    "Ashwini":"Deva", "Mrigashira":"Deva", "Punarvasu":"Deva",
    "Pushya":"Deva",  "Hasta":"Deva",      "Swati":"Deva",
    "Anuradha":"Deva","Shravana":"Deva",   "Revati":"Deva",
    "Bharani":"Manav","Rohini":"Manav",    "Ardra":"Manav",
    "Purva Phalguni":"Manav","Uttara Phalguni":"Manav","Uttara Ashadha":"Manav",
    "Vishakha":"Manav","Purva Ashadha":"Manav","Uttara Bhadrapada":"Manav",
    "Krittika":"Rakshasa","Ashlesha":"Rakshasa","Magha":"Rakshasa",
    "Chitra":"Rakshasa","Jyeshtha":"Rakshasa",
    "Mula":"Rakshasa","Purva Bhadrapada":"Rakshasa","Dhanishtha":"Rakshasa",
    "Shatabhisha":"Rakshasa",
}
GANA_SCORE = {
    ("Deva","Deva"): 6, ("Manav","Manav"): 6, ("Rakshasa","Rakshasa"): 6,
    ("Deva","Manav"): 5, ("Manav","Deva"): 5,
    ("Manav","Rakshasa"): 0, ("Rakshasa","Manav"): 0,
    ("Deva","Rakshasa"): 1, ("Rakshasa","Deva"): 1,
}

def calc_gana(nakshatra1, nakshatra2):
    g1 = GANA.get(nakshatra1, "Manav")
    g2 = GANA.get(nakshatra2, "Manav")
    return GANA_SCORE.get((g1, g2), 0)

# BHAKOOT
def calc_bhakoot(rashi1_num, rashi2_num):
    diff1 = ((rashi2_num - rashi1_num) % 12) + 1
    diff2 = ((rashi1_num - rashi2_num) % 12) + 1
    for d in [diff1, diff2]:
        if d in [2, 12, 3, 11, 4, 10]:
            return 0
    if diff1 in [5, 9] and diff2 in [5, 9]:
        return 7
    if diff1 == 1 or diff2 == 1:
        return 7
    if diff1 == 6 or diff2 == 6:
        return 0
    return 7

# NADI
NADI = {}
for i, name in enumerate(NAKSHATRA_NUMBER.keys()):
    if i % 3 == 0:   NADI[name] = "Adi"
    elif i % 3 == 1: NADI[name] = "Madhya"
    else:            NADI[name] = "Antya"

def calc_nadi(nakshatra1, nakshatra2):
    n1 = NADI.get(nakshatra1, "")
    n2 = NADI.get(nakshatra2, "")
    if n1 == n2:
        return 0
    return 8

def get_rashi_from_naam(naam: str) -> dict:
    naam_normalized = unicodedata.normalize('NFC', naam.strip())
    if not naam_normalized:
        return {"error": "Naam khali hai"}

    nakshatra_details = get_nakshatra_from_name(name=naam_normalized)

    if not nakshatra_details:
        return {"error": f"'{naam}' ke liye koi Rashi mapping nahi mili. Avakahada chakra mein pehla akshar nahi mila."}

    nakshatra_name, nakshatra_pada = nakshatra_details
    nakshatra_number = NAKSHATRA_NUMBER.get(nakshatra_name, 0)
    
    if nakshatra_number == 0:
        return {"error": f"'{nakshatra_name}' ke liye Nakshatra number nahi mila."}

    # Get Rashi and other details from Nakshatra
    nakshatra_data = get_nakshatra_data(nakshatra_number, representation="hk")
    rashi_name_en = RASHI_BY_NUMBER.get(nakshatra_data[0].get('rashi_ID', 0))
    
    if not rashi_name_en:
        return {"error": f"'{nakshatra_name}' ke liye Rashi nahi mili."}

    rashi_lord = RASHI_LORD_BY_NAME.get(rashi_name_en)
    nakshatra_lord_en = NAKSHATRA_LORDS_ORDER[(nakshatra_number - 1) % 9]

    return {
        "naam": naam,
        "prefix_matched": naam_normalized[0],
        "nakshatra": nakshatra_name,
        "rashi": rashi_name_en,
        "rashi_number": nakshatra_data[0].get('rashi_ID', 0),
        "rashi_lord": rashi_lord,
        "nakshatra_lord": nakshatra_lord_en,
        "nakshatra_number": nakshatra_number,
    }

def _resolve_person_chart(naam: str, birth_data: dict | None = None) -> dict:
    if birth_data:
        birth_info = dict(birth_data)
        birth_info["name"] = naam
        chart_info = _build_vedic_birth_info(birth_info)
        if "error" not in chart_info:
            chart_info["naam"] = naam
            chart_info["prefix_matched"] = None
            return chart_info

    name_info = get_rashi_from_naam(naam)
    if "error" not in name_info:
        name_info["source"] = "naam"
    return name_info

def naam_se_kundli_milan(naam1: str, naam2: str, boy_birth: dict | None = None, girl_birth: dict | None = None) -> dict:
    info1 = _resolve_person_chart(naam1, boy_birth)
    info2 = _resolve_person_chart(naam2, girl_birth)
    if "error" in info1:
        return {"error": f"Boy ke naam mein problem: {info1['error']}"}
    if "error" in info2:
        return {"error": f"Girl ke naam mein problem: {info2['error']}"}

    rashi1 = info1["rashi"]
    rashi2 = info2["rashi"]
    nak1   = info1["nakshatra"]
    nak2   = info2["nakshatra"]
    nak1_n = info1["nakshatra_number"]
    nak2_n = info2["nakshatra_number"]
    r1_num = info1["rashi_number"]
    r2_num = info2["rashi_number"]
    rl1    = info1["rashi_lord"]
    rl2    = info2["rashi_lord"]

    varna       = calc_varna(rashi1, rashi2)
    vashya      = calc_vashya(rashi1, rashi2)
    tara        = calc_tara(nak1_n, nak2_n)
    yoni        = calc_yoni(nak1, nak2)
    graha       = calc_graha_maitri(rl1, rl2)
    gana        = calc_gana(nak1, nak2)
    bhakoot     = calc_bhakoot(r1_num, r2_num)
    nadi        = calc_nadi(nak1, nak2)

    total = varna + vashya + tara + yoni + graha + gana + bhakoot + nadi
    total = round(total, 1)

    if total >= 32:
        result = "उत्तम (बहुत अच्छा) — विवाह शुभ है         https://vivah-com.vercel.app🟢"
    elif total >= 24:
        result = "मध्यम (अच्छा) — विवाह हो सकता है "
    elif total >= 18:
        result = "साधारण (औसत) — सोच समझ कर फैसला करें 🟡"
    else:
        result = "अधिक दोष (कमजोर) — विवाह अनुकूल नहीं "

    doshas = []
    if nadi == 0:
        doshas.append("नाड़ी दोष: एक ही नाड़ी है — स्वास्थ्य संबंधित समस्या हो सकती है")
    if bhakoot == 0:
        doshas.append("भाकूट दोष: 6-8 या 2-12 राशि — रिश्ते में तनाव हो सकता है")
    if gana == 0:
        doshas.append("गण दोष: एक देव और दूसरा राक्षस — स्वभाव असंगति")

    ashtakoot_en = {
        "Varna (1)":        varna,
        "Vashya (2)":       vashya,
        "Tara (3)":         tara,
        "Yoni (4)":         yoni,
        "Graha Maitri (5)": graha,
        "Gana (6)":         gana,
        "Bhakoot (7)":      bhakoot,
        "Nadi (8)":         nadi,
    }
    ashtakoot_hi = {KOOT_NAMES_HI[k]: v for k, v in ashtakoot_en.items()}
    
    return {
        "boy":  {"naam": naam1, "rashi": rashi1, "nakshatra": nak1, "rashi_lord": rl1, "source": info1.get("source", "naam")},
        "girl": {"naam": naam2, "rashi": rashi2, "nakshatra": nak2, "rashi_lord": rl2, "source": info2.get("source", "naam")},
        "ashtakoot": ashtakoot_hi,
        "total_gunas": f"{total} / 36",
        "result": result,
        "doshas": doshas if doshas else ["कोई बड़ा दोष नहीं मिला "],
    }

if __name__ == "__main__":
    import json
    print("=" * 55)
    print("   NAAM SE KUNDLI MILAN — Demo")
    print("=" * 55)

    result = naam_se_kundli_milan("राहुल", "प्रिया")
    print("\n Example 1: राहुल + प्रिया")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    result2 = naam_se_kundli_milan("गौरव", "सोनिया")
    print("\n Example 2: गौरव + सोनिया")
    print(json.dumps(result2, ensure_ascii=False, indent=2))

    print("\n Sirf Rashi nikalna:")
    r = get_rashi_from_naam("दीपक")
    print(json.dumps(r, ensure_ascii=False, indent=2))
