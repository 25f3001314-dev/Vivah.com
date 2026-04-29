# Vedic Matchmaking API - Quick Start Guide

## Installation & Running the Server

### Step 1: Install Dependencies

```bash
cd /workspaces/Vivah.com/api
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python main.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 3: Access the API

- **API Base**: http://localhost:8000/api/v1
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Example Request/Response

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/matchmaking/ashtakoot" \
  -H "Content-Type: application/json" \
  -d '{
    "boy_name": "राहुल",
    "girl_name": "प्रिया"
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/v1/matchmaking/ashtakoot"
data = {
    "boy_name": "राहुल",
    "girl_name": "प्रिया"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Total Score: {result['total_score']}/36")
print(f"Compatibility: {result['compatibility_percentage']}%")
print(f"Status: {result['result_status']}")
```

### Using JavaScript/Fetch

```javascript
const url = "http://localhost:8000/api/v1/matchmaking/ashtakoot";
const data = {
    boy_name: "राहुल",
    girl_name: "प्रिया"
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
    console.log(`Total Score: ${data.total_score}/36`);
    console.log(`Compatibility: ${data.compatibility_percentage}%`);
    console.log(`Status: ${data.result_status}`);
})
.catch(error => console.error('Error:', error));
```

## Running Tests

```bash
# Run the test suite (make sure server is running)
python test_api.py
```

## Understanding Result Statuses

### Result Status Levels

- **Excellent** (32-36 points): "अत्यंत शुभ विवाह" - Highly auspicious, recommended
- **Good** (24-31 points): "शुभ विवाह" - Auspicious, can proceed
- **Average** (18-23 points): "साधारण" - Neutral, consider carefully
- **Poor** (< 18 points): "अशुभ विवाह" - Inauspicious, not recommended

### Dosha Warnings

The system may report:
- **नाड़ी दोष (Nadi Dosha)**: Same Nadi detected - health issues possible
- **भाकूट दोष (Bhakoot Dosha)**: Inauspicious Rashi positions
- **गण दोष (Gana Dosha)**: Incompatible temperaments

## Sample Test Names

You can test with these common Indian names:

**Boys:**
- राहुल (Rahul)
- अर्जुन (Arjun)
- विराट (Virat)
- कृष्ण (Krishna)
- अजय (Ajay)

**Girls:**
- प्रिया (Priya)
- द्रौपदी (Draupadi)
- अनुष्का (Anushka)
- राधा (Radha)
- आशा (Asha)

## Important Notes

1. **Names must be in Devanagari script** (Hindi/Sanskrit Unicode characters)
   - ✓ राहुल (correct)
   - ✗ Rahul (incorrect)
   - ✗ राहुल mixed with English (incorrect)

2. **Names are case-sensitive** in terms of Unicode representation but will be normalized automatically

3. **The system uses the first syllable** for matching, as per traditional Vedic system

4. **Results are name-based only** - for full Kundli (horoscope) analysis, birth time and location are needed

## API Response Structure

All successful responses follow this structure:

```json
{
  "boy_profile": { /* Person's astrological profile */ },
  "girl_profile": { /* Person's astrological profile */ },
  "koot_scores": [ /* Array of 8 Koot scores */ ],
  "total_score": 28.5,
  "compatibility_percentage": 79.2,
  "result_status": "Good",
  "doshas": [ /* List of doshas if any */ ],
  "recommendations": [ /* Recommendations based on results */ ],
  "result_interpretation": "विवाह अनुकूल है"
}
```

## Troubleshooting

### Issue: "Name must be in Devanagari script"
**Solution:** Ensure you're using Hindi/Devanagari Unicode characters, not Latin script

### Issue: "Could not extract syllable"
**Solution:** The name might have special characters not in the Barahadi mapping. Check the name spelling

### Issue: Connection refused
**Solution:** Make sure the server is running (`python main.py`)

### Issue: Module not found errors
**Solution:** Install dependencies with `pip install -r requirements.txt`

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/matchmaking/ashtakoot` | POST | Calculate 8 Koot matching |
| `/api/v1/matchmaking/health` | GET | Check API health |
| `/health` | GET | Basic health check |
| `/` | GET | Root/Info endpoint |

## Environment Variables

You can customize behavior with environment variables (in `.env` file):

```env
API_ENV=production
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
ENABLE_JYOTISHA=true
ENABLE_BARAHADI_FALLBACK=true
```

## Architecture Overview

```
Frontend (webapp/)
    ↓
API Gateway
    ↓
FastAPI Server (api/v1/__init__.py)
    ↓
├── Routers (api/v1/routers/)
│   └── Endpoints
│
├── Services (api/v1/services/)
│   └── AshtakootCalculator
│       ├── PersonAstrologyProfile
│       └── Koot Calculations
│
├── Utils (api/v1/utils/)
│   ├── Syllable Extraction
│   ├── Text Normalization
│   └── Validation
│
└── Schemas (api/v1/schemas/)
    └── Pydantic Models
```

## Library Dependencies

- **fastapi** (0.104.1): Web framework
- **uvicorn** (0.24.0): ASGI server
- **pydantic** (2.5.0): Data validation
- **jyotisha** (0.4.0): Astronomical calculations (optional)
- **panchanga** (0.1.2): Vedic calendar calculations

## Production Considerations

1. Use a production ASGI server (Gunicorn + Uvicorn)
2. Set up proper logging to files
3. Configure CORS for your specific frontend domain
4. Use environment variables for sensitive settings
5. Add rate limiting for public endpoints
6. Use HTTPS in production
7. Monitor API performance and errors

## Support & Documentation

- Full API documentation: See `README.md`
- Test script: `test_api.py`
- Swagger/OpenAPI docs: Available at `/api/docs`

---

**For more details, refer to the main API README.md file.**
