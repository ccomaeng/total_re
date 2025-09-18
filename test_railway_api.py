#!/usr/bin/env python3
"""
Test script to verify Railway API deployment behavior
Based on user screenshot showing 스트레스상태=높음, 부신활성도=높음
"""

import requests
import json

# Railway API base URL
BASE_URL = "https://qhatotalre-production.up.railway.app"

def test_health_endpoint():
    """Test basic health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health response: {response.json()}")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint to see available endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Available endpoints: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"Root endpoint failed: {response.text}")
            return False
    except Exception as e:
        print(f"Root endpoint error: {e}")
        return False

def create_user_test_data():
    """Create test data matching user's screenshot: 스트레스상태=높음, 부신활성도=높음"""
    return {
        "personal_info": {
            "name": "테스트사용자",
            "age": 35,
            "special_notes": "없음"
        },
        "heavy_metals": {
            "mercury": "정상",
            "arsenic": "정상",
            "cadmium": "정상",
            "lead": "정상",
            "aluminum": "정상",
            "barium": "정상",
            "nickel": "정상",
            "uranium": "정상",
            "bismuth": "정상"
        },
        "nutritional_minerals": {
            "calcium": "정상",
            "magnesium": "정상",
            "sodium": "정상",
            "potassium": "정상",
            "copper": "정상",
            "zinc": "정상",
            "phosphorus": "정상",
            "iron": "정상",
            "manganese": "정상",
            "chromium": "정상",
            "selenium": "정상"
        },
        "health_indicators": {
            "insulin_sensitivity": "정상",
            "autonomic_nervous_system": "정상",
            "stress_state": "높음",  # User's screenshot shows this
            "immune_skin_health": "정상",
            "adrenal_activity": "높음",  # User's screenshot shows this
            "thyroid_activity": "정상"
        }
    }

def test_simple_analysis():
    """Test /simple/analyze endpoint (기존 형식)"""
    test_data = create_user_test_data()

    try:
        print("Testing /simple/analyze endpoint...")
        response = requests.post(
            f"{BASE_URL}/simple/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"Simple analysis status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Simple analysis success: {result.get('success')}")
            print(f"Message: {result.get('message')}")

            if result.get('data'):
                data = result['data']

                # Check what sections are available
                print("\nAvailable sections in response:")
                for key in data.keys():
                    print(f"- {key}")

                # Check comprehensive_analysis section specifically
                if 'comprehensive_analysis' in data:
                    comp_analysis = data['comprehensive_analysis']
                    print(f"\nComprehensive analysis type: {type(comp_analysis)}")

                    if isinstance(comp_analysis, str):
                        print(f"Comprehensive analysis length: {len(comp_analysis)} chars")
                        print(f"First 500 chars: {comp_analysis[:500]}...")

                        # Check if it has multiple sections
                        if '[유해 중금속 분석]' in comp_analysis:
                            print("✅ Contains heavy metals analysis section")
                        if '[영양 미네랄 분석]' in comp_analysis:
                            print("✅ Contains minerals analysis section")
                        if '[건강 상태 지표 분석]' in comp_analysis:
                            print("✅ Contains health indicators analysis section")

                    elif isinstance(comp_analysis, dict):
                        print("Comprehensive analysis is a dict with keys:")
                        for key in comp_analysis.keys():
                            print(f"  - {key}")
                else:
                    print("❌ No comprehensive_analysis section found")

                return result
            else:
                print("❌ No data in response")
                return None
        else:
            print(f"❌ API error: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Simple analysis error: {e}")
        return None

def test_prompt_analysis():
    """Test /prompt/analyze endpoint"""
    test_data = create_user_test_data()

    try:
        print("\nTesting /prompt/analyze endpoint...")
        response = requests.post(
            f"{BASE_URL}/prompt/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"Prompt analysis status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Prompt analysis success: {result.get('success')}")

            if result.get('data') and 'comprehensive_analysis' in result['data']:
                comp_analysis = result['data']['comprehensive_analysis']
                print(f"Prompt analysis comprehensive section length: {len(comp_analysis) if isinstance(comp_analysis, str) else 'Not string'}")
                return result
            else:
                print("❌ No comprehensive_analysis in prompt result")
                return None
        else:
            print(f"❌ Prompt API error: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Prompt analysis error: {e}")
        return None

def main():
    """Main test function"""
    print("=== Testing Railway API Deployment ===\n")

    # Test basic connectivity
    if not test_health_endpoint():
        print("❌ Health check failed - API may be down")
        return

    print("\n" + "="*50)
    if not test_root_endpoint():
        print("❌ Root endpoint failed")
        return

    print("\n" + "="*50)
    # Test the specific endpoints user would use
    simple_result = test_simple_analysis()

    print("\n" + "="*50)
    prompt_result = test_prompt_analysis()

    print("\n=== Test Summary ===")
    print(f"Simple analysis worked: {simple_result is not None}")
    print(f"Prompt analysis worked: {prompt_result is not None}")

    if simple_result and prompt_result:
        print("\n✅ Both endpoints are working")

        # Compare comprehensive analysis lengths
        simple_comp = simple_result.get('data', {}).get('comprehensive_analysis', '')
        prompt_comp = prompt_result.get('data', {}).get('comprehensive_analysis', '')

        if isinstance(simple_comp, str) and isinstance(prompt_comp, str):
            print(f"Simple comprehensive length: {len(simple_comp)}")
            print(f"Prompt comprehensive length: {len(prompt_comp)}")

            if len(simple_comp) < 100:
                print("⚠️  Simple analysis comprehensive section seems too short")
            if len(prompt_comp) < 100:
                print("⚠️  Prompt analysis comprehensive section seems too short")

    else:
        print("❌ One or both endpoints failed")

if __name__ == "__main__":
    main()