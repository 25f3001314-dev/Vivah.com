# -*- coding: utf-8 -*-
"""
Vedic Astrology Constants
This file contains traditional mappings and constants for Avakahada Chakra calculations.
These are used as a fallback when libraries cannot directly compute name-to-nakshatra.
"""

# Barahadi (Barahkhadi) - Traditional syllable to Nakshatra mapping
# This is the classical Hindi naming convention used in Vedic astrology
# Source: Traditional Jyotish texts - Brihat Samhita references
BARAHADI_TO_NAKSHATRA = {
    # क्वार्टर (Ka-line)
    "क": ("Krittika", "Mesh", 3, 1),
    "का": ("Krittika", "Mesh", 3, 1),
    "कि": ("Ardra", "Mithun", 6, 3),
    "की": ("Mrigashira", "Mithun", 5, 3),
    "कु": ("Ardra", "Mithun", 6, 3),
    "कू": ("Ardra", "Mithun", 6, 3),
    "के": ("Punarvasu", "Mithun", 7, 3),
    "को": ("Punarvasu", "Mithun", 7, 3),
    
    # ख-line
    "ख": ("Ashlesha", "Kark", 9, 4),
    "खा": ("Ashlesha", "Kark", 9, 4),
    "खि": ("Shravana", "Makar", 22, 10),
    "खी": ("Shravana", "Makar", 22, 10),
    "खु": ("Shravana", "Makar", 22, 10),
    "खू": ("Shravana", "Makar", 22, 10),
    "खे": ("Shravana", "Makar", 22, 10),
    "खो": ("Shravana", "Makar", 22, 10),
    
    # ग-line
    "ग": ("Ashlesha", "Kark", 9, 4),
    "गा": ("Dhanishtha", "Makar", 23, 10),
    "गि": ("Dhanishtha", "Kumbh", 23, 11),
    "गी": ("Dhanishtha", "Kumbh", 23, 11),
    "गु": ("Dhanishtha", "Kumbh", 23, 11),
    "गू": ("Dhanishtha", "Kumbh", 23, 11),
    "गे": ("Dhanishtha", "Kumbh", 23, 11),
    "गो": ("Shatabhisha", "Kumbh", 24, 11),
    
    # घ-line
    "घ": ("Ardra", "Mithun", 6, 3),
    
    # च-line
    "च": ("Ashwini", "Mesh", 1, 1),
    "चा": ("Revati", "Meen", 27, 12),
    "चि": ("Ashwini", "Mesh", 1, 1),
    "ची": ("Revati", "Meen", 27, 12),
    "चु": ("Ashwini", "Mesh", 1, 1),
    "चू": ("Ashwini", "Mesh", 1, 1),
    "चे": ("Ashwini", "Mesh", 1, 1),
    "चो": ("Ashwini", "Mesh", 1, 1),
    
    # छ-line
    "छ": ("Ardra", "Mithun", 6, 3),
    
    # ज-line
    "ज": ("Uttara Ashadha", "Makar", 21, 10),
    "जा": ("Uttara Ashadha", "Makar", 21, 10),
    "जि": ("Ashlesha", "Kark", 9, 4),
    "जी": ("Uttara Ashadha", "Makar", 21, 10),
    "जु": ("Uttara Ashadha", "Makar", 21, 10),
    "जू": ("Uttara Ashadha", "Makar", 21, 10),
    "जे": ("Ashlesha", "Kark", 9, 4),
    "जो": ("Ashlesha", "Kark", 9, 4),
    
    # झ-line
    "झ": ("Uttara Bhadrapada", "Meen", 26, 12),
    
    # ञ-line
    "ञ": ("Uttara Bhadrapada", "Meen", 26, 12),
    
    # ट-line
    "ट": ("Purva Phalguni", "Simha", 11, 5),
    "टा": ("Purva Phalguni", "Simha", 11, 5),
    "टि": ("Purva Phalguni", "Simha", 11, 5),
    "टी": ("Purva Phalguni", "Simha", 11, 5),
    "टु": ("Purva Phalguni", "Simha", 11, 5),
    "टू": ("Purva Phalguni", "Simha", 11, 5),
    "टे": ("Uttara Phalguni", "Simha", 12, 5),
    "टो": ("Uttara Phalguni", "Kanya", 12, 6),
    
    # ठ-line
    "ठ": ("Hasta", "Kanya", 13, 6),
    
    # ड-line
    "ड": ("Pushya", "Kark", 8, 4),
    "डा": ("Pushya", "Kark", 8, 4),
    "डि": ("Ashlesha", "Kark", 9, 4),
    "डी": ("Ashlesha", "Kark", 9, 4),
    "डु": ("Ashlesha", "Kark", 9, 4),
    "डू": ("Ashlesha", "Kark", 9, 4),
    "डे": ("Pushya", "Kark", 8, 4),
    "डो": ("Ashlesha", "Kark", 9, 4),
    
    # ढ-line
    "ढ": ("Purva Ashadha", "Dhanu", 20, 9),
    
    # त-line
    "त": ("Swati", "Tula", 15, 7),
    "ता": ("Swati", "Tula", 15, 7),
    "ति": ("Vishakha", "Tula", 16, 7),
    "ती": ("Vishakha", "Tula", 16, 7),
    "तु": ("Vishakha", "Tula", 16, 7),
    "तू": ("Vishakha", "Tula", 16, 7),
    "ते": ("Vishakha", "Tula", 16, 7),
    "तो": ("Vishakha", "Vrishchik", 16, 8),
    
    # थ-line
    "थ": ("Uttara Bhadrapada", "Meen", 26, 12),
    
    # द-line
    "द": ("Purva Bhadrapada", "Meen", 25, 12),
    "दा": ("Purva Bhadrapada", "Meen", 25, 12),
    "दि": ("Purva Bhadrapada", "Meen", 25, 12),
    "दी": ("Purva Bhadrapada", "Meen", 25, 12),
    "दु": ("Uttara Bhadrapada", "Meen", 26, 12),
    "दू": ("Uttara Bhadrapada", "Meen", 26, 12),
    "दे": ("Revati", "Meen", 27, 12),
    "दो": ("Revati", "Meen", 27, 12),
    
    # ध-line
    "ध": ("Purva Ashadha", "Dhanu", 20, 9),
    
    # न-line
    "न": ("Anuradha", "Vrishchik", 17, 8),
    "ना": ("Anuradha", "Vrishchik", 17, 8),
    "नि": ("Anuradha", "Vrishchik", 17, 8),
    "नी": ("Anuradha", "Vrishchik", 17, 8),
    "नु": ("Anuradha", "Vrishchik", 17, 8),
    "नू": ("Anuradha", "Vrishchik", 17, 8),
    "ने": ("Anuradha", "Vrishchik", 17, 8),
    "नो": ("Jyeshtha", "Vrishchik", 18, 8),
    
    # प-line
    "प": ("Uttara Phalguni", "Kanya", 12, 6),
    "पा": ("Uttara Phalguni", "Kanya", 12, 6),
    "पि": ("Uttara Phalguni", "Kanya", 12, 6),
    "पी": ("Uttara Phalguni", "Kanya", 12, 6),
    "पु": ("Hasta", "Kanya", 13, 6),
    "पू": ("Hasta", "Kanya", 13, 6),
    "पे": ("Chitra", "Kanya", 14, 6),
    "पो": ("Chitra", "Tula", 14, 7),
    
    # फ-line
    "फ": ("Purva Ashadha", "Dhanu", 20, 9),
    
    # ब-line
    "ब": ("Bharani", "Mesh", 2, 1),
    "बा": ("Bharani", "Mesh", 2, 1),
    "बि": ("Bharani", "Mesh", 2, 1),
    "बी": ("Bharani", "Mesh", 2, 1),
    "बु": ("Bharani", "Mesh", 2, 1),
    "बू": ("Bharani", "Mesh", 2, 1),
    "बे": ("Bharani", "Mesh", 2, 1),
    "बो": ("Bharani", "Mesh", 2, 1),
    
    # भ-line
    "भ": ("Mula", "Dhanu", 19, 9),
    "भा": ("Mula", "Dhanu", 19, 9),
    "भि": ("Mula", "Dhanu", 19, 9),
    "भी": ("Mula", "Dhanu", 19, 9),
    "भु": ("Purva Ashadha", "Dhanu", 20, 9),
    "भू": ("Purva Ashadha", "Dhanu", 20, 9),
    "भे": ("Uttara Ashadha", "Dhanu", 21, 9),
    "भो": ("Uttara Ashadha", "Makar", 21, 10),
    
    # म-line
    "म": ("Magha", "Simha", 10, 5),
    "मा": ("Magha", "Simha", 10, 5),
    "मि": ("Magha", "Simha", 10, 5),
    "मी": ("Magha", "Simha", 10, 5),
    "मु": ("Magha", "Simha", 10, 5),
    "मू": ("Magha", "Simha", 10, 5),
    "मे": ("Magha", "Simha", 10, 5),
    "मो": ("Purva Phalguni", "Simha", 11, 5),
    
    # य-line
    "य": ("Jyeshtha", "Vrishchik", 18, 8),
    "या": ("Jyeshtha", "Vrishchik", 18, 8),
    "यि": ("Jyeshtha", "Vrishchik", 18, 8),
    "यी": ("Jyeshtha", "Vrishchik", 18, 8),
    "यु": ("Jyeshtha", "Vrishchik", 18, 8),
    "यू": ("Jyeshtha", "Vrishchik", 18, 8),
    "ये": ("Mula", "Dhanu", 19, 9),
    "यो": ("Mula", "Dhanu", 19, 9),
    
    # र-line
    "र": ("Chitra", "Tula", 14, 7),
    "रा": ("Hasta", "Kanya", 13, 6),
    "रि": ("Chitra", "Tula", 14, 7),
    "री": ("Chitra", "Tula", 14, 7),
    "रु": ("Swati", "Tula", 15, 7),
    "रू": ("Swati", "Tula", 15, 7),
    "रे": ("Swati", "Tula", 15, 7),
    "रो": ("Swati", "Tula", 15, 7),
    
    # ल-line
    "ल": ("Uttara Bhadrapada", "Meen", 26, 12),
    "ला": ("Ashwini", "Mesh", 1, 1),
    "लि": ("Uttara Bhadrapada", "Meen", 26, 12),
    "ली": ("Bharani", "Mesh", 2, 1),
    "लु": ("Uttara Bhadrapada", "Meen", 26, 12),
    "लू": ("Bharani", "Mesh", 2, 1),
    "ले": ("Bharani", "Mesh", 2, 1),
    "लो": ("Bharani", "Mesh", 2, 1),
    
    # व-line
    "व": ("Rohini", "Vrishabh", 4, 2),
    "वा": ("Rohini", "Vrishabh", 4, 2),
    "वि": ("Vishakha", "Tula", 16, 7),
    "वी": ("Rohini", "Vrishabh", 4, 2),
    "वु": ("Rohini", "Vrishabh", 4, 2),
    "वू": ("Rohini", "Vrishabh", 4, 2),
    "वे": ("Mrigashira", "Vrishabh", 5, 2),
    "वो": ("Mrigashira", "Mithun", 5, 3),
    
    # श-line
    "श": ("Shravana", "Makar", 22, 10),
    "शा": ("Shravana", "Makar", 22, 10),
    "शि": ("Shravana", "Makar", 22, 10),
    "शी": ("Shravana", "Makar", 22, 10),
    "शु": ("Shravana", "Makar", 22, 10),
    "शू": ("Shravana", "Makar", 22, 10),
    "शे": ("Shatabhisha", "Kumbh", 24, 11),
    "शो": ("Shatabhisha", "Kumbh", 24, 11),
    
    # ष-line
    "ष": ("Hasta", "Kanya", 13, 6),
    
    # स-line
    "स": ("Shatabhisha", "Kumbh", 24, 11),
    "सा": ("Shatabhisha", "Kumbh", 24, 11),
    "सि": ("Shatabhisha", "Kumbh", 24, 11),
    "सी": ("Shatabhisha", "Kumbh", 24, 11),
    "सु": ("Shatabhisha", "Kumbh", 24, 11),
    "सू": ("Shatabhisha", "Kumbh", 24, 11),
    "से": ("Purva Bhadrapada", "Kumbh", 25, 11),
    "सो": ("Purva Bhadrapada", "Meen", 25, 12),
    
    # ह-line
    "ह": ("Punarvasu", "Kark", 7, 4),
    "हा": ("Punarvasu", "Kark", 7, 4),
    "हि": ("Hasta", "Kanya", 13, 6),
    "ही": ("Punarvasu", "Kark", 7, 4),
    "हु": ("Pushya", "Kark", 8, 4),
    "हू": ("Pushya", "Kark", 8, 4),
    "हे": ("Pushya", "Kark", 8, 4),
    "हो": ("Pushya", "Kark", 8, 4),
    
    # क्ष-line
    "क्ष": ("Krittika", "Mesh", 3, 1),
    
    # त्र-line
    "त्र": ("Anuradha", "Vrishchik", 17, 8),
    
    # ज्ञ-line
    "ज्ञ": ("Uttara Bhadrapada", "Meen", 26, 12),
    "ञ": ("Uttara Bhadrapada", "Meen", 26, 12),
    
    # Single vowels (as fallback)
    "अ": ("Krittika", "Mesh", 3, 1),
    "आ": ("Krittika", "Mesh", 3, 1),
    "इ": ("Krittika", "Vrishabh", 3, 2),
    "ई": ("Krittika", "Vrishabh", 3, 2),
    "उ": ("Krittika", "Vrishabh", 3, 2),
    "ऊ": ("Krittika", "Vrishabh", 3, 2),
    "ए": ("Krittika", "Vrishabh", 3, 2),
    "ऐ": ("Krittika", "Vrishabh", 3, 2),
    "ओ": ("Rohini", "Vrishabh", 4, 2),
    "औ": ("Rohini", "Vrishabh", 4, 2),
}

# Nakshatra Numbers (1-27)
NAKSHATRA_TO_NUMBER = {
    "Ashwini": 1,
    "Bharani": 2,
    "Krittika": 3,
    "Rohini": 4,
    "Mrigashira": 5,
    "Ardra": 6,
    "Punarvasu": 7,
    "Pushya": 8,
    "Ashlesha": 9,
    "Magha": 10,
    "Purva Phalguni": 11,
    "Uttara Phalguni": 12,
    "Hasta": 13,
    "Chitra": 14,
    "Swati": 15,
    "Vishakha": 16,
    "Anuradha": 17,
    "Jyeshtha": 18,
    "Mula": 19,
    "Purva Ashadha": 20,
    "Uttara Ashadha": 21,
    "Shravana": 22,
    "Dhanishtha": 23,
    "Shatabhisha": 24,
    "Purva Bhadrapada": 25,
    "Uttara Bhadrapada": 26,
    "Revati": 27,
}

# Rashi Numbers (1-12)
RASHI_TO_NUMBER = {
    "Mesh": 1,
    "Vrishabh": 2,
    "Mithun": 3,
    "Kark": 4,
    "Simha": 5,
    "Kanya": 6,
    "Tula": 7,
    "Vrishchik": 8,
    "Dhanu": 9,
    "Makar": 10,
    "Kumbh": 11,
    "Meen": 12,
}

# Rashi Lords (Ruling Planets)
RASHI_LORDS = {
    "Mesh": "Mangal",
    "Vrishabh": "Shukra",
    "Mithun": "Budh",
    "Kark": "Chandra",
    "Simha": "Surya",
    "Kanya": "Budh",
    "Tula": "Shukra",
    "Vrishchik": "Mangal",
    "Dhanu": "Guru",
    "Makar": "Shani",
    "Kumbh": "Shani",
    "Meen": "Guru",
}

# Nakshatra Lords (Planetary rulers - Vimshottari Dasha order)
NAKSHATRA_LORDS = {
    1: "Ketu",     # Ashwini
    2: "Shukra",   # Bharani
    3: "Surya",    # Krittika
    4: "Chandra",  # Rohini
    5: "Mangal",   # Mrigashira
    6: "Rahu",     # Ardra
    7: "Guru",     # Punarvasu
    8: "Shani",    # Pushya
    9: "Budh",     # Ashlesha
    10: "Ketu",    # Magha
    11: "Shukra",  # Purva Phalguni
    12: "Surya",   # Uttara Phalguni
    13: "Chandra", # Hasta
    14: "Mangal",  # Chitra
    15: "Rahu",    # Swati
    16: "Guru",    # Vishakha
    17: "Shani",   # Anuradha
    18: "Budh",    # Jyeshtha
    19: "Ketu",    # Mula
    20: "Shukra",  # Purva Ashadha
    21: "Surya",   # Uttara Ashadha
    22: "Chandra", # Shravana
    23: "Mangal",  # Dhanishtha
    24: "Rahu",    # Shatabhisha
    25: "Guru",    # Purva Bhadrapada
    26: "Shani",   # Uttara Bhadrapada
    27: "Budh",    # Revati
}

# Gana (Temperament) - Based on Nakshatra
NAKSHATRA_GANA = {
    "Ashwini": "Deva",
    "Bharani": "Manav",
    "Krittika": "Rakshasa",
    "Rohini": "Manav",
    "Mrigashira": "Deva",
    "Ardra": "Manav",
    "Punarvasu": "Deva",
    "Pushya": "Deva",
    "Ashlesha": "Rakshasa",
    "Magha": "Rakshasa",
    "Purva Phalguni": "Manav",
    "Uttara Phalguni": "Manav",
    "Hasta": "Deva",
    "Chitra": "Rakshasa",
    "Swati": "Deva",
    "Vishakha": "Manav",
    "Anuradha": "Deva",
    "Jyeshtha": "Rakshasa",
    "Mula": "Rakshasa",
    "Purva Ashadha": "Manav",
    "Uttara Ashadha": "Manav",
    "Shravana": "Deva",
    "Dhanishtha": "Rakshasa",
    "Shatabhisha": "Rakshasa",
    "Purva Bhadrapada": "Rakshasa",
    "Uttara Bhadrapada": "Manav",
    "Revati": "Deva",
}

# Yoni (Animal nature) - Based on Nakshatra
NAKSHATRA_YONI = {
    "Ashwini": ("Ashwa", "M"),      # Horse - Male
    "Bharani": ("Gaja", "M"),       # Elephant - Male
    "Krittika": ("Mesha", "F"),     # Ram - Female
    "Rohini": ("Sarpa", "M"),       # Serpent - Male
    "Mrigashira": ("Sarpa", "F"),   # Serpent - Female
    "Ardra": ("Shwan", "F"),        # Dog - Female
    "Punarvasu": ("Marjara", "F"),  # Cat - Female
    "Pushya": ("Mesha", "M"),       # Ram - Male
    "Ashlesha": ("Marjara", "M"),   # Cat - Male
    "Magha": ("Mushaka", "M"),      # Mouse - Male
    "Purva Phalguni": ("Mushaka", "F"), # Mouse - Female
    "Uttara Phalguni": ("Gau", "M"),    # Cow - Male
    "Hasta": ("Mahisha", "F"),      # Buffalo - Female
    "Chitra": ("Vyaghra", "F"),     # Tiger - Female
    "Swati": ("Mahisha", "M"),      # Buffalo - Male
    "Vishakha": ("Vyaghra", "M"),   # Tiger - Male
    "Anuradha": ("Mriga", "F"),     # Deer - Female
    "Jyeshtha": ("Mriga", "M"),     # Deer - Male
    "Mula": ("Nakula", "F"),        # Mongoose - Female
    "Purva Ashadha": ("Vanara", "M"), # Monkey - Male
    "Uttara Ashadha": ("Nakula", "M"), # Mongoose - Male
    "Shravana": ("Vanara", "F"),    # Monkey - Female
    "Dhanishtha": ("Simha", "F"),   # Lion - Female
    "Shatabhisha": ("Ashwa", "F"),  # Horse - Female
    "Purva Bhadrapada": ("Simha", "M"), # Lion - Male
    "Uttara Bhadrapada": ("Gau", "F"),  # Cow - Female
    "Revati": ("Gaja", "F"),        # Elephant - Female
}

# Varna (Class/Caste) - Based on Rashi
RASHI_VARNA = {
    "Mesh": "Kshatriya",
    "Vrishabh": "Vaishya",
    "Mithun": "Shudra",
    "Kark": "Brahmin",
    "Simha": "Kshatriya",
    "Kanya": "Vaishya",
    "Tula": "Shudra",
    "Vrishchik": "Brahmin",
    "Dhanu": "Kshatriya",
    "Makar": "Vaishya",
    "Kumbh": "Shudra",
    "Meen": "Brahmin",
}

# Vashya (Dominion) - Based on Rashi
RASHI_VASHYA = {
    "Mesh": "Chatushpad",       # 4-legged
    "Vrishabh": "Chatushpad",   # 4-legged
    "Mithun": "Manav",          # Human
    "Kark": "Jalachara",        # Aquatic
    "Simha": "Vanchar",         # Forest creature
    "Kanya": "Manav",           # Human
    "Tula": "Manav",            # Human
    "Vrishchik": "Keeta",       # Insect
    "Dhanu": "Chatushpad",      # 4-legged
    "Makar": "Chatushpad",      # 4-legged
    "Kumbh": "Manav",           # Human
    "Meen": "Jalachara",        # Aquatic
}

# Nadi (Nerve energy) - Based on Nakshatra position mod 3
NAKSHATRA_NADI = {
    1: "Adi",     # Ashwini   - 1 mod 3 = 1
    2: "Madhya",  # Bharani   - 2 mod 3 = 2
    3: "Antya",   # Krittika  - 3 mod 3 = 0 -> Antya
    4: "Adi",     # Rohini    - 4 mod 3 = 1
    5: "Madhya",  # Mrigashira
    6: "Antya",   # Ardra
    7: "Adi",     # Punarvasu
    8: "Madhya",  # Pushya
    9: "Antya",   # Ashlesha
    10: "Adi",    # Magha
    11: "Madhya", # Purva Phalguni
    12: "Antya",  # Uttara Phalguni
    13: "Adi",    # Hasta
    14: "Madhya", # Chitra
    15: "Antya",  # Swati
    16: "Adi",    # Vishakha
    17: "Madhya", # Anuradha
    18: "Antya",  # Jyeshtha
    19: "Adi",    # Mula
    20: "Madhya", # Purva Ashadha
    21: "Antya",  # Uttara Ashadha
    22: "Adi",    # Shravana
    23: "Madhya", # Dhanishtha
    24: "Antya",  # Shatabhisha
    25: "Adi",    # Purva Bhadrapada
    26: "Madhya", # Uttara Bhadrapada
    27: "Antya",  # Revati
}

# Varna Ranking (for Varna compatibility)
VARNA_RANK = {
    "Brahmin": 4,
    "Kshatriya": 3,
    "Vaishya": 2,
    "Shudra": 1,
}
