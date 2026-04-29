#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Vedic Matchmaking API
Run this to test the API endpoints and functionality
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_health_check():
    """Test the health check endpoint."""
    print_section("Test 1: Health Check")
    
    url = f"{BASE_URL}/api/v1/matchmaking/health"
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Health check failed"
    print("✓ Health check passed!")


def test_ashtakoot_matching(boy_name: str, girl_name: str):
    """Test Ashtakoot matching for a boy-girl pair."""
    print_section(f"Test: Ashtakoot Matching - {boy_name} & {girl_name}")
    
    url = f"{BASE_URL}/api/v1/matchmaking/ashtakoot"
    payload = {
        "boy_name": boy_name,
        "girl_name": girl_name
    }
    
    print(f"Request: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload)
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Print boy profile
        print(f"\n📍 Boy Profile:")
        print(f"  Name: {data['boy_profile']['name']}")
        print(f"  First Syllable: {data['boy_profile']['first_syllable']}")
        print(f"  Nakshatra: {data['boy_profile']['nakshatra_data']['nakshatra_name']} (#{data['boy_profile']['nakshatra_data']['nakshatra_number']})")
        print(f"  Rashi: {data['boy_profile']['nakshatra_data']['rashi_name']} (#{data['boy_profile']['nakshatra_data']['rashi_number']})")
        print(f"  Gana: {data['boy_profile']['nakshatra_data']['gana']}")
        print(f"  Yoni: {data['boy_profile']['nakshatra_data']['yoni']}")
        print(f"  Nadi: {data['boy_profile']['nakshatra_data']['nadi']}")
        print(f"  Source: {data['boy_profile']['source']}")
        
        # Print girl profile
        print(f"\n💑 Girl Profile:")
        print(f"  Name: {data['girl_profile']['name']}")
        print(f"  First Syllable: {data['girl_profile']['first_syllable']}")
        print(f"  Nakshatra: {data['girl_profile']['nakshatra_data']['nakshatra_name']} (#{data['girl_profile']['nakshatra_data']['nakshatra_number']})")
        print(f"  Rashi: {data['girl_profile']['nakshatra_data']['rashi_name']} (#{data['girl_profile']['nakshatra_data']['rashi_number']})")
        print(f"  Gana: {data['girl_profile']['nakshatra_data']['gana']}")
        print(f"  Yoni: {data['girl_profile']['nakshatra_data']['yoni']}")
        print(f"  Nadi: {data['girl_profile']['nakshatra_data']['nadi']}")
        print(f"  Source: {data['girl_profile']['source']}")
        
        # Print koot scores
        print(f"\n🎯 Ashtakoot Scores:")
        for koot in data['koot_scores']:
            status_emoji = "✓" if koot['status'] == "auspicious" else ("~" if koot['status'] == "neutral" else "✗")
            print(f"  {status_emoji} {koot['koot_name']}: {koot['score']}/{koot['max_score']} ({koot['status']})")
        
        # Print final result
        print(f"\n📊 Final Result:")
        print(f"  Total Score: {data['total_score']}/36")
        print(f"  Compatibility: {data['compatibility_percentage']}%")
        print(f"  Status: {data['result_status']}")
        print(f"  Interpretation: {data['result_interpretation']}")
        
        # Print doshas if any
        if data['doshas']:
            print(f"\n⚠️  Doshas Detected:")
            for dosha in data['doshas']:
                print(f"  • {dosha}")
        
        # Print recommendations if any
        if data['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in data['recommendations']:
                print(f"  • {rec}")
        
        print("\n✓ Test passed!")
        return True
    else:
        print(f"Error Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("\n✗ Test failed!")
        return False


def test_invalid_input():
    """Test error handling with invalid input."""
    print_section("Test: Error Handling - Invalid Input")
    
    url = f"{BASE_URL}/api/v1/matchmaking/ashtakoot"
    
    # Test 1: Invalid script (English names)
    print("Testing with English names (should fail)...")
    payload = {
        "boy_name": "Rahul",
        "girl_name": "Priya"
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 400, "Should have returned 400 error"
    print("✓ Correctly rejected English names")
    
    # Test 2: Empty names
    print("\nTesting with empty names (should fail)...")
    payload = {
        "boy_name": "",
        "girl_name": ""
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 422, "Should have returned 422 validation error"
    print("✓ Correctly rejected empty names")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("  Vedic Matchmaking API - Test Suite")
    print("="*60)
    
    try:
        # Test 1: Health check
        test_health_check()
        
        # Test 2: Multiple matching pairs
        test_cases = [
            ("राहुल", "प्रिया"),
            ("अर्जुन", "द्रौपदी"),
            ("विराट", "अनुष्का"),
            ("कृष्ण", "राधा"),
        ]
        
        for boy, girl in test_cases:
            test_ashtakoot_matching(boy, girl)
        
        # Test 3: Error handling
        test_invalid_input()
        
        print_section("All Tests Completed Successfully! ✓")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the API server.")
        print("   Make sure the server is running: python api/main.py")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
