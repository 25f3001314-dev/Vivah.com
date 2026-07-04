HINDI_TRANSLATIONS = {
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

    "Surya": "सूर्य",
    "Chandra": "चंद्र",
    "Mangal": "मंगल",
    "Budh": "बुध",
    "Guru": "गुरु",
    "Shukra": "शुक्र",
    "Shani": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",

    "Deva": "देव",
    "Manav": "मानव",
    "Rakshasa": "राक्षस",

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

    "Adi": "आदि",
    "Madhya": "मध्य",
    "Antya": "अन्त्य",

    "Brahmin": "ब्राह्मण",
    "Kshatriya": "क्षत्रिय",
    "Vaishya": "वैश्य",
    "Shudra": "शूद्र",

    "Chatushpad": "चतुष्पद",
    "Jalachara": "जलचर",
    "Vanchar": "वनचर",
    "Keeta": "कीट",
}


def translate_to_hindi(text: str):
    if not text:
        return text
    return HINDI_TRANSLATIONS.get(text, text)


def build_result_text(total: float) -> str:
    if total >= 32:
        return "उत्तम (बहुत अच्छा) - विवाह शुभ है"
    if total >= 24:
        return "मध्यम (अच्छा) - विवाह हो सकता है"
    if total >= 18:
        return "साधारण (औसत) - सोच समझ कर फैसला करें"
    return "अधिक दोष (कमजोर) - विवाह अनुकूल नहीं"
