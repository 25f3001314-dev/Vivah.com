# -*- coding: utf-8 -*-
"""Rule tables for Ashtakoot Milan.

All tradition-specific defaults live here to keep scoring functions pure.
"""

from __future__ import annotations

# Bhakoot: only these three rashi-distance pairs are inauspicious.
BHAKOOT_FORBIDDEN_PAIRS = frozenset(
    {
        frozenset({2, 12}),
        frozenset({4, 10}),
        frozenset({6, 8}),
    }
)

# Nadi shipped defaults.
NADI_DOSHA_CANCELLATION = {
    "same_nakshatra_same_pada": False,
    "same_nakshatra_different_pada": True,
    "same_rashi_different_nakshatra": True,
    "exception_nakshatras_enabled": False,
    "exception_nakshatras": frozenset(),
    "missing_pada_behavior": "assume_different",
}

# Yoni shipped defaults.
YONI_SCORES = {
    "same_yoni_opposite_gender": 4.0,
    "same_yoni_same_gender": 3.0,
    "friend": 3.0,
    "neutral": 2.0,
    "mild_enemy": 1.0,
    "worst_enemy": 0.0,
}

YONI_WORST_ENEMY_PAIRS = frozenset(
    {
        frozenset({"Ashwa", "Mahisha"}),
        frozenset({"Gaja", "Simha"}),
        frozenset({"Mesha", "Vanara"}),
        frozenset({"Sarpa", "Nakula"}),
        frozenset({"Shwan", "Mriga"}),
        frozenset({"Marjara", "Mushaka"}),
    }
)

YONI_FRIEND_PAIRS = frozenset(
    {
        frozenset({"Ashwa", "Gaja"}),
        frozenset({"Mesha", "Gau"}),
        frozenset({"Marjara", "Simha"}),
        frozenset({"Vanara", "Nakula"}),
    }
)

YONI_MILD_ENEMY_PAIRS = frozenset()

TARA_AUSPICIOUS = frozenset({2, 4, 6, 8, 9})

VASHYA_COMPAT = {
    "Chatushpad": {"Chatushpad", "Manav"},
    "Manav": {"Manav", "Jalachara", "Vanchar"},
    "Jalachara": {"Jalachara", "Manav"},
    "Vanchar": {"Vanchar", "Chatushpad"},
    "Keeta": {"Keeta", "Jalachara"},
}

GRAHA_RELATION = {
    "Surya": {"Mitra": {"Chandra", "Mangal", "Guru"}, "Shatru": {"Shukra", "Shani"}, "Sam": {"Budh"}},
    "Chandra": {"Mitra": {"Surya", "Budh"}, "Shatru": set(), "Sam": {"Mangal", "Guru", "Shukra", "Shani"}},
    "Mangal": {"Mitra": {"Surya", "Chandra", "Guru"}, "Shatru": {"Budh"}, "Sam": {"Shukra", "Shani"}},
    "Budh": {"Mitra": {"Surya", "Shukra"}, "Shatru": {"Chandra"}, "Sam": {"Mangal", "Guru", "Shani"}},
    "Guru": {"Mitra": {"Surya", "Chandra", "Mangal"}, "Shatru": {"Budh", "Shukra"}, "Sam": {"Shani"}},
    "Shukra": {"Mitra": {"Budh", "Shani"}, "Shatru": {"Surya", "Chandra"}, "Sam": {"Mangal", "Guru"}},
    "Shani": {"Mitra": {"Budh", "Shukra"}, "Shatru": {"Surya", "Chandra", "Mangal"}, "Sam": {"Guru"}},
    "Rahu": {"Mitra": {"Shukra", "Shani"}, "Shatru": {"Surya", "Chandra", "Mangal"}, "Sam": {"Guru", "Budh"}},
    "Ketu": {"Mitra": {"Mangal", "Shukra", "Shani"}, "Shatru": {"Surya", "Chandra"}, "Sam": {"Guru", "Budh"}},
}

# Commutative key: tuple(sorted((rel_a, rel_b))).
GRAHA_SCORE = {
    ("Mitra", "Mitra"): 5.0,
    ("Mitra", "Sam"): 4.0,
    ("Sam", "Sam"): 3.0,
    ("Mitra", "Shatru"): 1.0,
    ("Sam", "Shatru"): 0.5,
    ("Shatru", "Shatru"): 0.0,
}

# Commutative key: tuple(sorted((gana_a, gana_b))).
GANA_SCORE = {
    ("Deva", "Deva"): 6.0,
    ("Manav", "Manav"): 6.0,
    ("Rakshasa", "Rakshasa"): 6.0,
    ("Deva", "Manav"): 5.0,
    ("Manav", "Rakshasa"): 0.0,
    ("Deva", "Rakshasa"): 1.0,
}
