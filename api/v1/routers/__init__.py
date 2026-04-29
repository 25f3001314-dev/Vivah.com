# -*- coding: utf-8 -*-
"""
Matchmaking API Routes
FastAPI endpoints for Vedic matchmaking and Ashtakoot Milan calculations.
"""

from fastapi import APIRouter, HTTPException
import logging

from ..services import perform_ashtakoot_milan
from ..schemas import (
    MatchmakingRequest,
    AshtakootResult,
    KootScore,
    PersonData,
    NakshatraData,
    ErrorResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/matchmaking", tags=["Matchmaking"])


@router.post(
    "/ashtakoot",
    response_model=AshtakootResult,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Calculate Ashtakoot Milan",
    description="Calculate 8 Koot compatibility and generate matching score between two people based on their names.",
)
async def calculate_ashtakoot(request: MatchmakingRequest):
    """
    Calculate Ashtakoot Milan (8-Koot matching) between boy and girl.
    
    This endpoint:
    1. Extracts first syllable from each name
    2. Determines Nakshatra and Rashi for each person
    3. Calculates all 8 Koots (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi)
    4. Generates compatibility score and interpretation
    
    **Parameters:**
    - `boy_name`: Boy's name in Devanagari script (required)
    - `girl_name`: Girl's name in Devanagari script (required)
    
    **Response includes:**
    - Individual Koot scores (0-8 for each)
    - Total compatibility score (0-36)
    - Compatibility percentage
    - Overall status (Excellent/Good/Average/Poor)
    - Any doshas (defects) and recommendations
    
    **Example:**
    ```json
    {
        "boy_name": "राहुल",
        "girl_name": "प्रिया"
    }
    ```
    
    **References:**
    - Library Used: jyotisha (with Barahadi fallback)
    - Traditional System: Ashtakoot Milan from Vedic Astrology
    """
    try:
        # Perform the matching calculation
        result = perform_ashtakoot_milan(request.boy_name, request.girl_name)

        # Check if there was an error
        if "error" in result:
            logger.error(f"Matchmaking error: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])

        # Build Koot scores for response
        koot_scores = []
        for koot_name, koot_num, score, max_score in result["koot_results"]:
            status = "auspicious" if score >= (max_score * 0.7) else ("neutral" if score > 0 else "inauspicious")
            koot_scores.append(
                KootScore(
                    koot_name=koot_name,
                    koot_number=koot_num,
                    score=score,
                    max_score=max_score,
                    status=status,
                )
            )

        # Build person profiles for response
        boy_nakshatra_data = NakshatraData(
            nakshatra_name=result["boy_profile"]["nakshatra"],
            nakshatra_number=result["boy_profile"]["nakshatra_number"],
            rashi_name=result["boy_profile"]["rashi"],
            rashi_number=result["boy_profile"]["rashi_number"],
            gana=result["boy_profile"]["gana"],
            yoni=result["boy_profile"]["yoni"],
            yoni_gender=result["boy_profile"]["yoni_gender"],
            varna=result["boy_profile"]["varna"],
            vashya=result["boy_profile"]["vashya"],
            nadi=result["boy_profile"]["nadi"],
            rashi_lord=result["boy_profile"]["rashi_lord"],
            nakshatra_lord=result["boy_profile"]["nakshatra_lord"],
        )

        girl_nakshatra_data = NakshatraData(
            nakshatra_name=result["girl_profile"]["nakshatra"],
            nakshatra_number=result["girl_profile"]["nakshatra_number"],
            rashi_name=result["girl_profile"]["rashi"],
            rashi_number=result["girl_profile"]["rashi_number"],
            gana=result["girl_profile"]["gana"],
            yoni=result["girl_profile"]["yoni"],
            yoni_gender=result["girl_profile"]["yoni_gender"],
            varna=result["girl_profile"]["varna"],
            vashya=result["girl_profile"]["vashya"],
            nadi=result["girl_profile"]["nadi"],
            rashi_lord=result["girl_profile"]["rashi_lord"],
            nakshatra_lord=result["girl_profile"]["nakshatra_lord"],
        )

        boy_data = PersonData(
            name=result["boy_profile"]["name"],
            first_syllable=result["boy_profile"]["first_syllable"],
            nakshatra_data=boy_nakshatra_data,
            source=result["boy_profile"]["source"],
        )

        girl_data = PersonData(
            name=result["girl_profile"]["name"],
            first_syllable=result["girl_profile"]["first_syllable"],
            nakshatra_data=girl_nakshatra_data,
            source=result["girl_profile"]["source"],
        )

        # Build final response
        return AshtakootResult(
            boy_profile=boy_data,
            girl_profile=girl_data,
            koot_scores=koot_scores,
            total_score=result["total_score"],
            compatibility_percentage=result["compatibility_percentage"],
            result_status=result["result_status"],
            doshas=result["doshas"],
            recommendations=result["recommendations"],
            result_interpretation=result["result_interpretation"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ashtakoot calculation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during calculation")


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the matchmaking service is running and dependencies are available.",
)
async def health_check():
    """
    Health check endpoint to verify service status and available libraries.
    """
    try:
        from jyotisha import __version__ as jyotisha_version
        jyotisha_available = True
    except ImportError:
        jyotisha_available = False
        jyotisha_version = "not installed"

    return {
        "status": "healthy",
        "version": "1.0.0",
        "libraries": {
            "jyotisha": f"{jyotisha_version if jyotisha_available else 'not available (using Barahadi fallback)'}",
            "fastapi": "enabled",
        },
        "features": {
            "ashtakoot_milan": True,
            "barahadi_fallback": True,
            "jyotisha_support": jyotisha_available,
        },
    }
