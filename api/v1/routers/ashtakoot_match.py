# -*- coding: utf-8 -*-
"""Attribute-based Ashtakoot Milan route."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..schemas import (
    AshtakootErrorResponse,
    AshtakootMatchRequest,
    AshtakootMatchResponse,
)
from ..services.ashtakoot_match_service import calculate_ashtakoot_milan

router = APIRouter(prefix="/ashtakoot", tags=["Ashtakoot"])


def _error_response(payload: dict) -> JSONResponse:
    return JSONResponse(status_code=400, content={"success": False, "error": payload["error"]})


@router.post(
    "/match",
    response_model=AshtakootMatchResponse,
    responses={400: {"model": AshtakootErrorResponse}, 500: {"model": AshtakootErrorResponse}},
    summary="Calculate Ashtakoot Milan from attributes",
    description="Calculates the 8-koot compatibility score from precomputed boy/girl attributes.",
)
async def match_ashtakoot(request: AshtakootMatchRequest):
    try:
        boy_payload = request.boy.model_dump() if request.boy else {}
        girl_payload = request.girl.model_dump() if request.girl else {}

        result = calculate_ashtakoot_milan(boy_payload, girl_payload)
        if "error" in result:
            return _error_response(result)

        return result
    except HTTPException:
        raise
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected error during Ashtakoot calculation",
                    "missing_fields": None,
                },
            },
        )