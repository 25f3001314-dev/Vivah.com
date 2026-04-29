# -*- coding: utf-8 -*-
"""
Utility functions for Vedic astrology calculations
- Syllable extraction from Devanagari names
- Text processing and normalization
"""

import unicodedata
from typing import Optional, Tuple
from .constants import BARAHADI_TO_NAKSHATRA


def normalize_devanagari(text: str) -> str:
    """
    Normalize Devanagari Unicode text (NFC decomposition handling).
    Ensures consistent representation across different encodings.
    
    Args:
        text: Input string in Devanagari or English
    
    Returns:
        Normalized string
    """
    if not text:
        return ""
    return unicodedata.normalize('NFC', text.strip())


def extract_first_syllable(name: str) -> Optional[str]:
    """
    Robust extraction of the first pronounceable Devanagari syllable (akshar).

    Algorithm (practical, not a full phonetic parser):
    - Normalize Unicode (NFC) and strip whitespace
    - Validate input
    - Parse an initial consonant cluster joined by virama (U+094D), if present
    - Include an immediately following dependent vowel sign (matra) or diacritic
    - If the name starts with an independent vowel, return that vowel

    Limitations (practical notes):
    - This is a heuristic; Sanskrit phonetics and exceptional orthography can be
      more complex than handled here. It handles the common cases such as
      conjuncts (e.g., 'प्र', 'ध्र'), matras (e.g., 'ि', 'ा', 'े'), and simple
      vowel initials. It does not perform full syllabification for rare
      orthographic edge-cases or script anomalies.

    Args:
        name: Input string in Devanagari script

    Returns:
        First syllable string, or None when extraction fails

    Raises:
        ValueError: when input is empty or not valid text
    """
    if name is None:
        raise ValueError("Name cannot be None")

    name = normalize_devanagari(name)
    if not isinstance(name, str) or len(name.strip()) == 0:
        raise ValueError("Name must be a non-empty string")

    s = name.strip()
    if len(s) == 0:
        raise ValueError("Name cannot be empty or whitespace only")

    # Unicode codepoints useful for Devanagari parsing
    VIRAMA = "\u094D"  # halant
    NUKTA = "\u093C"

    # Independent vowels (letters that represent vowels by themselves)
    INDEP_VOWELS = [chr(cp) for cp in range(0x0904, 0x0915)]

    # Consonants range (क..ह, plus extended consonants)
    CONSONANT_START = 0x0915
    CONSONANT_END = 0x0939

    # Dependent vowel signs (matras) and special vowel signs
    MATRA_START = 0x093E
    MATRA_END = 0x094C
    ADDITIONAL_MATRAS = {"\u0962", "\u0963"}

    # Diacritics often following a syllable
    DIACRITICS = {"\u0901", "\u0902", "\u0903"}  # candrabindu, anusvara, visarga

    def is_consonant(ch: str) -> bool:
        if not ch:
            return False
        o = ord(ch)
        return CONSONANT_START <= o <= CONSONANT_END

    def is_indep_vowel(ch: str) -> bool:
        return ch in INDEP_VOWELS

    def is_matra(ch: str) -> bool:
        return MATRA_START <= ord(ch) <= MATRA_END or ch in ADDITIONAL_MATRAS

    # If starts with independent vowel, return it (may be followed by diacritics)
    first = s[0]
    if is_indep_vowel(first):
        # Include trailing diacritics if any
        idx = 1
        while idx < len(s) and s[idx] in DIACRITICS:
            idx += 1
        return s[:idx]

    # Otherwise, expect a consonant or consonant cluster
    if not is_consonant(first):
        # Not a consonant or vowel — give up (could be punctuation etc.)
        return None

    i = 0
    syllable_chars = []

    # Consume initial consonant
    syllable_chars.append(s[i])
    i += 1

    # Handle possible nukta following consonant
    if i < len(s) and s[i] == NUKTA:
        syllable_chars.append(s[i])
        i += 1

    # Consume conjuncts of form (virama + consonant(+nukta))*
    while i + 1 < len(s) and s[i] == VIRAMA and is_consonant(s[i + 1]):
        # append virama and following consonant
        syllable_chars.append(s[i])
        syllable_chars.append(s[i + 1])
        i += 2
        # optional nukta after that consonant
        if i < len(s) and s[i] == NUKTA:
            syllable_chars.append(s[i])
            i += 1

    # After cluster, include a dependent vowel sign (matra) if present
    if i < len(s) and is_matra(s[i]):
        syllable_chars.append(s[i])
        i += 1
        # include possible vowel diacritics after matra (rare)
        while i < len(s) and s[i] in DIACRITICS:
            syllable_chars.append(s[i])
            i += 1
        return "".join(syllable_chars)

    # If no matra, return the consonant cluster itself (inherent 'a')
    # but include trailing diacritics if present
    while i < len(s) and s[i] in DIACRITICS:
        syllable_chars.append(s[i])
        i += 1

    return "".join(syllable_chars)


def get_nakshatra_from_syllable(syllable: str) -> Optional[Tuple[str, str, int, int]]:
    """
    Map syllable to Nakshatra using traditional Barahadi system.
    This is the FALLBACK mapping used when jyotisha library is unavailable.
    
    Args:
        syllable: First syllable (akshar) of the name
    
    Returns:
        Tuple of (Nakshatra, Rashi, Nakshatra_Number, Rashi_Number) or None
    """
    if not syllable:
        return None
    
    syllable = normalize_devanagari(syllable)
    return BARAHADI_TO_NAKSHATRA.get(syllable)


def is_devanagari(text: str) -> bool:
    """
    Check if text contains Devanagari characters.
    
    Args:
        text: Input string
    
    Returns:
        True if text contains Devanagari, False otherwise
    """
    if not text:
        return False
    
    # Devanagari Unicode range: U+0900 to U+097F
    for char in text:
        code_point = ord(char)
        if 0x0900 <= code_point <= 0x097F:
            return True
    
    return False


def transliterate_to_devanagari(text: str) -> Optional[str]:
    """
    Simple transliteration helper (placeholder for future enhancement).
    Currently just returns the input if it's already in Devanagari.
    
    Args:
        text: Input string (English or Devanagari)
    
    Returns:
        Devanagari string or None if conversion not possible
    """
    # For now, check if already Devanagari
    if is_devanagari(text):
        return normalize_devanagari(text)
    
    # TODO: Implement IAST/HK to Devanagari transliteration for English names
    # This would require a transliteration library or mapping
    return None


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a name is suitable for processing.
    
    Args:
        name: Input name string
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Name cannot be empty"
    
    if len(name.strip()) == 0:
        return False, "Name cannot be whitespace only"
    
    normalized = normalize_devanagari(name)
    
    if not normalized:
        return False, "Name normalization failed"
    
    if not is_devanagari(normalized):
        return False, "Name must be in Devanagari script"
    
    return True, None
