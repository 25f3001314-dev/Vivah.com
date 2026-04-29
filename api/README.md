# Vedic Matchmaking API - Backend Documentation

## Overview

This is a complete backend API for Vedic matchmaking (Ashtakoot Milan - 8 Koot compatibility matching). The API accepts two names in Devanagari (Hindi) script and calculates detailed compatibility scores based on traditional Vedic astrology principles.

## Project Structure

```
api/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
└── v1/
    ├── __init__.py           # FastAPI app
    ├── routers/
    │   └── __init__.py       # API endpoints
    ├── services/
    │   └── __init__.py       # Business logic (Ashtakoot Calculator)
    ├── schemas/
    │   └── __init__.py       # Pydantic models for request/response
    └── utils/
        ├── __init__.py       # Utility functions (syllable extraction)
        └── constants.py      # Vedic constants and mappings
```

## Features

- ✅ **Name-based Ashtakoot Milan**: Calculate 8 Koot matching scores
- ✅ **Syllable Extraction**: Automatic extraction of first syllable (Akshar) from Devanagari names
- ✅ **Open-Source Library Support**: Uses `jyotisha` library with Barahadi fallback
- ✅ **Comprehensive Matching**: All 8 Koots calculated:
  - Varna (Class)
  - Vashya (Dominion)
  - Tara (Lunar Position)
  - Yoni (Animal Nature)
  - Graha Maitri (Planetary Friendship)
  - Gana (Temperament)
  - Bhakoot (Rashi Position)
  - Nadi (Nerve Energy)
- ✅ **Dosha Detection**: Identifies and reports doshas
- ✅ **Compatibility Percentage**: Final score out of 36 with percentage
- ✅ **Recommendations**: Provides suggestions based on results
- ✅ **UTF-8 Safe**: Full Devanagari Unicode support

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Navigate to api directory
cd /workspaces/Vivah.com/api

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Ashtakoot Milan Calculation

**Endpoint:** `POST /api/v1/matchmaking/ashtakoot`

**Request:**
```json
{
  "boy_name": "राहुल",
  "girl_name": "प्रिया"
}
```

**Response (Success - 200):**
```json
{
  "boy_profile": {
    "name": "राहुल",
    "first_syllable": "रा",
    "nakshatra_data": {
      "nakshatra_name": "Hasta",
      "nakshatra_number": 13,
      "rashi_name": "Kanya",
      "rashi_number": 6,
      "gana": "Deva",
      "yoni": "Mahisha",
      "yoni_gender": "F",
      "varna": "Vaishya",
      "vashya": "Manav",
      "nadi": "Adi",
      "rashi_lord": "Budh",
      "nakshatra_lord": "Chandra"
    },
    "source": "barahadi"
  },
  "girl_profile": {
    "name": "प्रिया",
    "first_syllable": "प्र",
    "nakshatra_data": {
      "nakshatra_name": "Purva Phalguni",
      "nakshatra_number": 11,
      "rashi_name": "Simha",
      "rashi_number": 5,
      "gana": "Manav",
      "yoni": "Mushaka",
      "yoni_gender": "F",
      "varna": "Kshatriya",
      "vashya": "Vanchar",
      "nadi": "Madhya",
      "rashi_lord": "Surya",
      "nakshatra_lord": "Shukra"
    },
    "source": "barahadi"
  },
  "koot_scores": [
    {
      "koot_name": "Varna",
      "koot_number": 1,
      "score": 1.0,
      "max_score": 1.0,
      "status": "auspicious"
    },
    {
      "koot_name": "Vashya",
      "koot_number": 2,
      "score": 1.0,
      "max_score": 2.0,
      "status": "neutral"
    },
    {
      "koot_name": "Tara",
      "koot_number": 3,
      "score": 3.0,
      "max_score": 3.0,
      "status": "auspicious"
    },
    {
      "koot_name": "Yoni",
      "koot_number": 4,
      "score": 2.0,
      "max_score": 4.0,
      "status": "neutral"
    },
    {
      "koot_name": "Graha Maitri",
      "koot_number": 5,
      "score": 3.0,
      "max_score": 5.0,
      "status": "neutral"
    },
    {
      "koot_name": "Gana",
      "koot_number": 6,
      "score": 5.0,
      "max_score": 6.0,
      "status": "auspicious"
    },
    {
      "koot_name": "Bhakoot",
      "koot_number": 7,
      "score": 7.0,
      "max_score": 7.0,
      "status": "auspicious"
    },
    {
      "koot_name": "Nadi",
      "koot_number": 8,
      "score": 8.0,
      "max_score": 8.0,
      "status": "auspicious"
    }
  ],
  "total_score": 30.0,
  "compatibility_percentage": 83.3,
  "result_status": "Excellent",
  "doshas": [],
  "recommendations": [],
  "result_interpretation": "अत्यंत शुभ विवाह - विवाह अत्यंत शुभ है"
}
```

**Response (Error - 400):**
```json
{
  "error": "Name must be in Devanagari script",
  "detail": "Boy's name must be in Devanagari script",
  "status_code": 400
}
```

### 2. Health Check

**Endpoint:** `GET /api/v1/matchmaking/health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "libraries": {
    "jyotisha": "0.4.0",
    "fastapi": "enabled"
  },
  "features": {
    "ashtakoot_milan": true,
    "barahadi_fallback": true,
    "jyotisha_support": true
  }
}
```

## Understanding the Results

### Koot Scores Explanation

1. **Varna (1 point)**: Checks if boy's caste/class is equal or higher than girl's. Score: 0 or 1
2. **Vashya (2 points)**: Checks dominion compatibility. Score: 0, 1, or 2
3. **Tara (3 points)**: Based on Nakshatra positions. Auspicious in Taras 2,4,6,8,9. Score: 0 or 3
4. **Yoni (4 points)**: Animal compatibility. Same Yoni opposite gender=4, same=3, neutral=2, enemies=0
5. **Graha Maitri (5 points)**: Planetary lord friendship. Score: 0 to 5
6. **Gana (6 points)**: Temperament compatibility. Same Gana=6, compatible=5 or 0. Score: 0-6
7. **Bhakoot (7 points)**: Rashi position compatibility. Score: 0 or 7
8. **Nadi (8 points)**: Same Nadi is inauspicious. Score: 0 or 8

### Overall Interpretation

- **32-36**: Excellent (उत्तम) - Highly auspicious
- **24-31**: Good (मध्यम) - Can proceed
- **18-23**: Average (साधारण) - Consider carefully
- **< 18**: Poor (अशुभ) - Not recommended

## Technical Details

### Syllable Extraction

The system extracts the first pronounceable syllable (Akshar) using:
1. 3-character combinations (e.g., क्ष, त्र)
2. 2-character combinations (most common: consonant + vowel)
3. Single character fallback

Example:
- राहुल → रा (2-char syllable)
- प्रिया → प्र (2-char syllable)

### Library Stack

- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation and serialization
- **jyotisha**: Astronomical calculations (optional, with fallback)
- **Barahadi Mapping**: Traditional syllable-to-Nakshatra mapping (fallback)

### Data Sources

- Nakshatra data: Traditional Vedic texts
- Planetary relationships: Brihat Samhita
- Compatibility rules: Classical Jyotish texts

## Testing Examples

### cURL Examples

```bash
# Test 1: Basic matching
curl -X POST "http://localhost:8000/api/v1/matchmaking/ashtakoot" \
  -H "Content-Type: application/json" \
  -d '{"boy_name": "राहुल", "girl_name": "प्रिया"}'

# Test 2: Another pair
curl -X POST "http://localhost:8000/api/v1/matchmaking/ashtakoot" \
  -H "Content-Type: application/json" \
  -d '{"boy_name": "अर्जुन", "girl_name": "द्रौपदी"}'

# Health check
curl "http://localhost:8000/api/v1/matchmaking/health"
```

### Python Example

```python
import requests
import json

url = "http://localhost:8000/api/v1/matchmaking/ashtakoot"
payload = {
    "boy_name": "राहुल",
    "girl_name": "प्रिया"
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Total Score: {data['total_score']}")
print(f"Compatibility: {data['compatibility_percentage']}%")
print(f"Result: {data['result_status']}")
print(f"Interpretation: {data['result_interpretation']}")

for koot in data['koot_scores']:
    print(f"{koot['koot_name']}: {koot['score']}/{koot['max_score']}")
```

## Error Handling

The API returns meaningful error messages for various scenarios:

1. **Invalid Script**: Non-Devanagari names
2. **Empty Names**: Empty or whitespace-only names
3. **Unknown Syllables**: Syllables not in the mapping database
4. **Processing Errors**: Server errors during calculation

## Doshas (Defects)

The system can identify:
- **Nadi Dosha**: Same Nadi in both profiles (health issues)
- **Bhakoot Dosha**: Inauspicious Rashi positions
- **Gana Dosha**: Incompatible temperaments

## Recommendations

The system provides recommendations when:
- Score is low (< 18)
- Specific doshas are detected
- Additional remedies are needed

## Interactive Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Production Deployment

For production:
1. Set `reload=False` in `main.py`
2. Use a production ASGI server like Gunicorn/Uvicorn
3. Configure CORS origins specifically
4. Add rate limiting
5. Enable logging to file
6. Use environment variables for configuration

Example Gunicorn deployment:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.v1:app --bind 0.0.0.0:8000
```

## References

- Vedic Astrology: Classical texts on Ashtakoot Milan
- jyotisha Library: https://github.com/V1Europe/jyotisha
- Barahadi System: Traditional Indian naming system
- Nakshatra Information: 27 lunar mansions in Vedic astronomy

## Notes

- All names must be in Devanagari script for accurate processing
- The system uses the first syllable as per Vedic naming traditions
- Results are based on name analysis only (birth chart analysis requires additional data)
- For complete Kundli (horoscope) analysis, birth time and location are needed

## License

This API follows the same license as the main Vivah.com project.

---

**For issues, suggestions, or enhancements, please refer to the main project repository.**
