import os
import sys

from flask import Flask, render_template, request, jsonify

# Add parent directory to path for API imports
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

# Change to app directory for template/static resolution
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from api.v1.services.by_name import generate_avakahada_attributes, compare_ashtakoot

app = Flask(__name__, static_folder='static', template_folder='templates')

# Hindi Translations Mapping
HINDI_TRANSLATIONS = {
    # Rashis (Zodiac Signs)
    "Mesh": "मेष",
    "Vrishabh": "वृषभ",
    "Mithun": "मिथुन",
    "Kark": "कर्क",
    "Simha": "सिंह",
    "Kanya": "कन्या",
    "Tula": "तुला",
    "Vrishchik": "वृश्चिक",
    "Dhanu": "धनु",
    "Makar": "मकर",
    "Kumbh": "कुंभ",
    "Meen": "मीन",
    
    # Nakshatras (Lunar Mansions)
    "Ashwini": "अश्विनी",
    "Bharani": "भरणी",
    "Krittika": "कृत्तिका",
    "Rohini": "रोहिणी",
    "Mrigashira": "मृगशिरा",
    "Ardra": "आर्द्रा",
    "Punarvasu": "पुनर्वसु",
    "Pushya": "पुष्य",
    "Ashlesha": "आश्लेषा",
    "Magha": "मघा",
    "Purva Phalguni": "पूर्व फाल्गुनी",
    "Uttara Phalguni": "उत्तर फाल्गुनी",
    "Hasta": "हस्त",
    "Chitra": "चित्रा",
    "Swati": "स्वाति",
    "Vishakha": "विशाखा",
    "Anuradha": "अनुराधा",
    "Jyeshtha": "ज्येष्ठा",
    "Mula": "मूल",
    "Purva Ashadha": "पूर्व आषाढ़",
    "Uttara Ashadha": "उत्तर आषाढ़",
    "Shravana": "श्रवण",
    "Dhanishtha": "धनिष्ठा",
    "Shatabhisha": "शतभिषा",
    "Purva Bhadrapada": "पूर्व भाद्रपद",
    "Uttara Bhadrapada": "उत्तर भाद्रपद",
    "Revati": "रेवती",
    
    # Grahas (Planets)
    "Surya": "सूर्य",
    "Chandra": "चंद्र",
    "Mangal": "मंगल",
    "Budh": "बुध",
    "Guru": "गुरु",
    "Shukra": "शुक्र",
    "Shani": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",
    
    # Ganas (Temperaments)
    "Deva": "देव",
    "Manav": "मानव",
    "Rakshasa": "राक्षस",
    
    # Yonis (Animal Types)
    "Ashwa": "अश्व",
    "Gaja": "गज",
    "Simha": "सिंह",
    "Sarpa": "सर्प",
    "Marjara": "मार्जार",
    "Vanara": "वानर",
    "Shwan": "श्वान",
    "Mriga": "मृग",
    "Mahisha": "महिष",
    "Gau": "गौ",
    "Mushaka": "मूषक",
    "Nakula": "नकुल",
    
    # Nadis
    "Adi": "आदि",
    "Madhya": "मध्य",
    "Antya": "अन्त्य",
    
    # Varnas (Castes)
    "Brahmin": "ब्राह्मण",
    "Kshatriya": "क्षत्रिय",
    "Vaishya": "वैश्य",
    "Shudra": "शूद्र",
    
    # Vashyas
    "Chatushpad": "चतुष्पद",
    "Jalachara": "जलचर",
    "Vanchar": "वनचर",
    "Keeta": "कीट",
}

def _translate_to_hindi(text):
    """Translate English astrological terms to Hindi."""
    if not text:
        return text
    return HINDI_TRANSLATIONS.get(text, text)


def _build_result_text(total: float) -> str:
    if total >= 32:
        return "उत्तम (बहुत अच्छा) - विवाह शुभ है"
    if total >= 24:
        return "मध्यम (अच्छा) - विवाह हो सकता है"
    if total >= 18:
        return "साधारण (औसत) - सोच समझ कर फैसला करें"
    return "अधिक दोष (कमजोर) - विवाह अनुकूल नहीं"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/milan', methods=['POST'])
def api_milan():
    data = request.get_json() or {}
    boy_payload = data.get('boy', {})
    girl_payload = data.get('girl', {})

    if isinstance(boy_payload, str):
        boy_payload = {"name": boy_payload}
    if isinstance(girl_payload, str):
        girl_payload = {"name": girl_payload}

    boy_name = boy_payload.get('name', '').strip()
    girl_name = girl_payload.get('name', '').strip()

    if not boy_name or not girl_name:
        return jsonify({"error": "दोनों नाम डालें."}), 400

    try:
        boy_profile = generate_avakahada_attributes(boy_name)
        girl_profile = generate_avakahada_attributes(girl_name)
        asht = compare_ashtakoot(boy_profile, girl_profile)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    total = float(asht["total"])
    percent = round((total / 36.0) * 100, 1)

    result = {
        "boy": {
            "नाम": boy_name,
            "राशि": _translate_to_hindi(boy_profile.get("rashi")),
            "नक्षत्र": _translate_to_hindi(boy_profile.get("nakshatra")),
            "गण": _translate_to_hindi(boy_profile.get("gana")),
            "योनि": _translate_to_hindi(boy_profile.get("yoni")),
            "राशि_स्वामी": _translate_to_hindi(boy_profile.get("rashi_lord")),
            "नाड़ी": _translate_to_hindi(boy_profile.get("nadi")),
            "पद": boy_profile.get("pada"),
            "स्रोत": boy_profile.get("source", "barahadi"),
        },
        "girl": {
            "नाम": girl_name,
            "राशि": _translate_to_hindi(girl_profile.get("rashi")),
            "नक्षत्र": _translate_to_hindi(girl_profile.get("nakshatra")),
            "गण": _translate_to_hindi(girl_profile.get("gana")),
            "योनि": _translate_to_hindi(girl_profile.get("yoni")),
            "राशि_स्वामी": _translate_to_hindi(girl_profile.get("rashi_lord")),
            "नाड़ी": _translate_to_hindi(girl_profile.get("nadi")),
            "पद": girl_profile.get("pada"),
            "स्रोत": girl_profile.get("source", "barahadi"),
        },
        "guna": {
            "वर्ण (गुण 1)": asht["varna"],
            "वश्य (गुण 2)": asht["vashya"],
            "तारा (गुण 3)": asht["tara"],
            "योनि (गुण 4)": asht["yoni"],
            "ग्रह मैत्री (गुण 5)": asht["graha_maitri"],
            "गण (गुण 6)": asht["gana"],
            "भाकूट (गुण 7)": asht["bhakoot"],
            "नाड़ी (गुण 8)": asht["nadi"],
        },
        "total_gunas": f"{total} / 36",
        "percentage": f"{percent}%",
        "result": _build_result_text(total),
        "doshas": [
            "नाड़ी दोष: एक ही नाड़ी है - स्वास्थ्य संबंधित समस्या हो सकती है" if asht["nadi"] == 0 else None,
            "भाकूट दोष: 6-8 या 2-12 राशि - रिश्ते में तनाव हो सकता है" if asht["bhakoot"] == 0 else None,
            "गण दोष: स्वभाव असंगति" if asht["gana"] == 0 else None,
        ],
    }
    result["doshas"] = [d for d in result["doshas"] if d] or ["कोई बड़ा दोष नहीं मिला"]
    return jsonify(result)


if __name__ == '__main__':
    # Run locally with debug, Vercel will handle production
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=debug_mode)
