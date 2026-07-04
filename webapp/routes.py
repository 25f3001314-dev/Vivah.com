from flask import Blueprint, render_template, request, jsonify

from api.v1.services.by_name import generate_avakahada_attributes, compare_ashtakoot
from .i18n import translate_to_hindi, build_result_text

bp = Blueprint('webapp', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/api/milan', methods=['POST'])
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
            "राशि": translate_to_hindi(boy_profile.get("rashi")),
            "नक्षत्र": translate_to_hindi(boy_profile.get("nakshatra")),
            "गण": translate_to_hindi(boy_profile.get("gana")),
            "योनि": translate_to_hindi(boy_profile.get("yoni")),
            "राशि_स्वामी": translate_to_hindi(boy_profile.get("rashi_lord")),
            "नाड़ी": translate_to_hindi(boy_profile.get("nadi")),
            "पद": boy_profile.get("pada"),
            "स्रोत": boy_profile.get("source", "barahadi"),
        },
        "girl": {
            "नाम": girl_name,
            "राशि": translate_to_hindi(girl_profile.get("rashi")),
            "नक्षत्र": translate_to_hindi(girl_profile.get("nakshatra")),
            "गण": translate_to_hindi(girl_profile.get("gana")),
            "योनि": translate_to_hindi(girl_profile.get("yoni")),
            "राशि_स्वामी": translate_to_hindi(girl_profile.get("rashi_lord")),
            "नाड़ी": translate_to_hindi(girl_profile.get("nadi")),
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
        "result": build_result_text(total),
        "doshas": [
            "नाड़ी दोष: एक ही नाड़ी है - स्वास्थ्य संबंधित समस्या हो सकती है" if asht.get("nadi") == 0 else None,
            "भाकूट दोष: 6-8 या 2-12 राशि - रिश्ते में तनाव हो सकता है" if asht.get("bhakoot") == 0 else None,
            "गण दोष: स्वभाव असंगति" if asht.get("gana") == 0 else None,
        ],
    }
    result["doshas"] = [d for d in result["doshas"] if d] or ["कोई बड़ा दोष नहीं मिला"]
    return jsonify(result)
