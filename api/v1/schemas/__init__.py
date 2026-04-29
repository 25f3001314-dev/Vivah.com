# -*- coding: utf-8 -*-
"""
Pydantic schemas for request and response validation.
Defines data models for the Vedic matchmaking API.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class PersonInput(BaseModel):
    """Person's name input for Ashtakoot matching."""
    name: str = Field(..., min_length=1, description="Person's name in Devanagari script")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "विराट"
            }
        }


class MatchmakingRequest(BaseModel):
    """Request model for Ashtakoot matching."""
    boy_name: str = Field(..., min_length=1, description="Boy's name in Devanagari")
    girl_name: str = Field(..., min_length=1, description="Girl's name in Devanagari")

    class Config:
        json_schema_extra = {
            "example": {
                "boy_name": "राहुल",
                "girl_name": "प्रिया"
            }
        }


class NakshatraData(BaseModel):
    """Nakshatra and related astrological attributes."""
    nakshatra_name: str = Field(..., description="Name of the Nakshatra (27 lunar mansions)")
    nakshatra_number: int = Field(..., ge=1, le=27, description="Nakshatra number 1-27")
    rashi_name: str = Field(..., description="Moon sign (Rashi) in Hindi")
    rashi_number: int = Field(..., ge=1, le=12, description="Rashi number 1-12")
    gana: str = Field(..., description="Temperament: Deva, Manav, or Rakshasa")
    yoni: str = Field(..., description="Animal nature")
    yoni_gender: str = Field(..., description="Yoni gender: M (Male) or F (Female)")
    varna: str = Field(..., description="Varna/Class: Brahmin, Kshatriya, Vaishya, Shudra")
    vashya: str = Field(..., description="Dominion type: Manav, Chatushpad, Jalachara, etc.")
    nadi: str = Field(..., description="Nerve energy: Adi, Madhya, or Antya")
    rashi_lord: str = Field(..., description="Ruling planet of Rashi")
    nakshatra_lord: str = Field(..., description="Ruling planet of Nakshatra")


class PersonData(BaseModel):
    """Complete astrological profile of a person."""
    name: str = Field(..., description="Person's name")
    first_syllable: str = Field(..., description="First pronounceable syllable of the name")
    nakshatra_data: NakshatraData
    source: str = Field(..., description="Data source: 'barahadi' for fallback, 'jyotisha' for library")


class KootScore(BaseModel):
    """Individual Koot matching score."""
    koot_name: str = Field(..., description="Name of the Koot")
    koot_number: int = Field(..., ge=1, le=8, description="Koot number 1-8")
    score: float = Field(..., ge=0, le=8, description="Score obtained out of 8")
    max_score: float = Field(default=8, description="Maximum possible score")
    status: str = Field(..., description="Status: auspicious, neutral, or inauspicious")


class AshtakootResult(BaseModel):
    """Ashtakoot Milan matching result."""
    boy_profile: PersonData
    girl_profile: PersonData
    koot_scores: List[KootScore] = Field(..., description="Individual scores for all 8 Koots")
    total_score: float = Field(..., ge=0, le=36, description="Total matching score out of 36")
    compatibility_percentage: float = Field(..., ge=0, le=100, description="Compatibility percentage")
    result_status: str = Field(..., description="Overall status: Excellent, Good, Average, Poor")
    doshas: List[str] = Field(default_factory=list, description="List of identified doshas/defects")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations based on matching")
    result_interpretation: str = Field(..., description="Detailed explanation of the result")

    class Config:
        json_schema_extra = {
            "example": {
                "total_score": 28.5,
                "compatibility_percentage": 79.2,
                "result_status": "Good"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid name",
                "detail": "Boy's name must be in Devanagari script",
                "status_code": 400
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy", description="Service status")
    version: str = Field(..., description="API version")
    libraries: Dict[str, str] = Field(..., description="Available libraries and their status")


class PersonAttributesInput(BaseModel):
    """Astrology attributes supplied directly for Ashtakoot Milan.

    All fields are optional at the transport layer so the API can return a
    graceful 400 error when required attributes are missing. The scoring service
    validates which fields are needed for each koot.
    """

    name: Optional[str] = Field(default=None, description="Optional name, if available")
    first_syllable: Optional[str] = Field(default=None, description="Optional first syllable")
    nakshatra: Optional[str] = Field(default=None, description="Nakshatra name")
    nakshatra_number: Optional[int] = Field(default=None, ge=1, le=27, description="Nakshatra number 1-27")
    rashi: Optional[str] = Field(default=None, description="Rashi/Moon sign name")
    rashi_number: Optional[int] = Field(default=None, ge=1, le=12, description="Rashi number 1-12")
    gana: Optional[str] = Field(default=None, description="Gana/temperament")
    yoni: Optional[str] = Field(default=None, description="Yoni/animal nature")
    nadi: Optional[str] = Field(default=None, description="Nadi type")
    varna: Optional[str] = Field(default=None, description="Varna/class")
    vashya: Optional[str] = Field(default=None, description="Vashya/dominion type")
    rashi_lord: Optional[str] = Field(default=None, description="Planetary lord of the Rashi")
    nakshatra_lord: Optional[str] = Field(default=None, description="Planetary lord of the Nakshatra")


class AshtakootBreakdown(BaseModel):
    """8-koot result breakdown."""

    varna: float = Field(..., description="Varna score")
    vashya: float = Field(..., description="Vashya score")
    tara: float = Field(..., description="Tara score")
    yoni: float = Field(..., description="Yoni score")
    graha_maitri: float = Field(..., description="Graha Maitri score")
    gana: float = Field(..., description="Gana score")
    bhakoot: float = Field(..., description="Bhakoot score")
    nadi: float = Field(..., description="Nadi score")
    total: float = Field(..., ge=0, le=36, description="Total score out of 36")
    max: float = Field(default=36, description="Maximum possible score")


class AshtakootMatchRequest(BaseModel):
    """Request body for attribute-based Ashtakoot Milan."""

    boy: Optional[PersonAttributesInput] = Field(default=None)
    girl: Optional[PersonAttributesInput] = Field(default=None)


class AshtakootMatchResponse(BaseModel):
    """Success response for attribute-based Ashtakoot Milan."""

    success: bool = Field(default=True)
    boy: PersonAttributesInput
    girl: PersonAttributesInput
    ashtakoot: AshtakootBreakdown


class AshtakootErrorDetail(BaseModel):
    """Structured error details for attribute-based matching."""

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    missing_fields: Optional[List[str]] = Field(default=None, description="Missing required fields")


class AshtakootErrorResponse(BaseModel):
    """Error response for attribute-based Ashtakoot Milan."""

    success: bool = Field(default=False)
    error: AshtakootErrorDetail
