# -*- coding: utf-8 -*-
"""
Vedic Matchmaking API Package
"""

__version__ = "1.0.0"
__author__ = "Vivah.com Development Team"
__description__ = "Backend API for Ashtakoot Milan (8-Koot) compatibility matching based on Vedic Astrology"

try:
	from .v1 import app
except ImportError:
	from v1 import app

__all__ = ["app"]
