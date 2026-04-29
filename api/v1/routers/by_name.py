# -*- coding: utf-8 -*-
"""Route for matchmaking by name."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from ..services.by_name import (
    compare_ashtakoot,
    generate_avakahada_attributes,
    get_first_syllable,
)

router = APIRouter(prefix="/match", tags=["Matchmaking"])


def _validation_error(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message,
            },
        },
    )


@router.post("/by-name")
async def match_by_name(request: Request):
    try:
        payload = await request.json()
    except Exception:
        return _validation_error("boy_name and girl_name are required")

    if not isinstance(payload, dict):
        return _validation_error("boy_name and girl_name are required")

    boy_name = payload.get("boy_name")
    girl_name = payload.get("girl_name")

    if not isinstance(boy_name, str) or not isinstance(girl_name, str):
        return _validation_error("boy_name and girl_name are required")

    boy_name = boy_name.strip()
    girl_name = girl_name.strip()

    if not boy_name or not girl_name:
        return _validation_error("boy_name and girl_name are required")

    try:
        boy_first_syllable = get_first_syllable(boy_name)
        girl_first_syllable = get_first_syllable(girl_name)

        boy_profile = generate_avakahada_attributes(boy_name)
        girl_profile = generate_avakahada_attributes(girl_name)

        ashtakoot = compare_ashtakoot(boy_profile, girl_profile)
    except ValueError as exc:
        return _validation_error(str(exc))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return {
        "success": True,
        "input": {
            "boy_name": boy_name,
            "girl_name": girl_name,
        },
        "boy": {
            "first_syllable": boy_first_syllable,
            "nakshatra": boy_profile["nakshatra"],
            "rashi": boy_profile["rashi"],
            "gana": boy_profile["gana"],
            "yoni": boy_profile["yoni"],
            "nadi": boy_profile["nadi"],
            "varna": boy_profile["varna"],
            "vashya": boy_profile["vashya"],
        },
        "girl": {
            "first_syllable": girl_first_syllable,
            "nakshatra": girl_profile["nakshatra"],
            "rashi": girl_profile["rashi"],
            "gana": girl_profile["gana"],
            "yoni": girl_profile["yoni"],
            "nadi": girl_profile["nadi"],
            "varna": girl_profile["varna"],
            "vashya": girl_profile["vashya"],
        },
        "ashtakoot": ashtakoot,
    }