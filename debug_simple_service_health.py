#!/usr/bin/env python3
"""
Debug script to investigate why Simple Analysis Service is missing the second health indicator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.models.input_models import (
    HairAnalysisInput, PersonalInfo, HeavyMetals, NutritionalMinerals,
    HealthIndicators, TestResultValue, HeavyMetalValue
)
from backend.app.services.simple_analysis_service import SimpleHairAnalysisService
import re

def create_test_case():
    """Create test case with both stress and adrenal high"""
    return HairAnalysisInput(
        personal_info=PersonalInfo(
            name="테스트",
            age=30,
            special_notes="없음"
        ),
        heavy_metals=HeavyMetals(
            mercury=HeavyMetalValue.NORMAL,
            arsenic=HeavyMetalValue.NORMAL,
            cadmium=HeavyMetalValue.NORMAL,
            lead=HeavyMetalValue.NORMAL,
            aluminum=HeavyMetalValue.NORMAL,
            barium=HeavyMetalValue.NORMAL,
            nickel=HeavyMetalValue.NORMAL,
            uranium=HeavyMetalValue.NORMAL,
            bismuth=HeavyMetalValue.NORMAL
        ),
        nutritional_minerals=NutritionalMinerals(
            calcium=TestResultValue.NORMAL,
            magnesium=TestResultValue.NORMAL,
            sodium=TestResultValue.NORMAL,
            potassium=TestResultValue.NORMAL,
            copper=TestResultValue.NORMAL,
            zinc=TestResultValue.NORMAL,
            phosphorus=TestResultValue.NORMAL,
            iron=TestResultValue.NORMAL,
            manganese=TestResultValue.NORMAL,
            chromium=TestResultValue.NORMAL,
            selenium=TestResultValue.NORMAL
        ),
        health_indicators=HealthIndicators(
            insulin_sensitivity=TestResultValue.NORMAL,
            autonomic_nervous_system=TestResultValue.NORMAL,
            stress_state=TestResultValue.HIGH,      # 높음
            immune_skin_health=TestResultValue.NORMAL,
            adrenal_activity=TestResultValue.HIGH,  # 높음
            thyroid_activity=TestResultValue.NORMAL
        )
    )

def debug_simple_health_extraction():
    """Debug the Simple Analysis Service health extraction specifically"""
    print("🔍 Debugging Simple Analysis Service Health Extraction")
    print("=" * 70)

    test_data = create_test_case()
    service = SimpleHairAnalysisService()

    # Test the _extract_health_analysis method directly
    print("📋 Direct _extract_health_analysis call:")
    health_analysis = service._extract_health_analysis(test_data)
    print(f"Result: {health_analysis}")
    print()

    # Let's step through the logic manually
    print("🔍 Manual step-through of the logic:")

    note4_content = service.notes_cache.get("note4_health_indicators", "")
    health = test_data.health_indicators
    age = test_data.personal_info.age
    name = test_data.personal_info.name

    print(f"Health indicators:")
    print(f"  - stress_state: {health.stress_state}")
    print(f"  - adrenal_activity: {health.adrenal_activity}")
    print(f"  - thyroid_activity: {health.thyroid_activity}")
    print()

    content_parts = []
    indicators_to_skip = []

    # Check complex conditions first
    print("🔍 Checking complex conditions:")
    adrenal_high = health.adrenal_activity == TestResultValue.HIGH
    thyroid_low = health.thyroid_activity == TestResultValue.LOW

    print(f"  - adrenal_high: {adrenal_high}")
    print(f"  - thyroid_low: {thyroid_low}")
    print(f"  - Complex condition (adrenal_high AND thyroid_low): {adrenal_high and thyroid_low}")

    if adrenal_high and thyroid_low:
        print("  ❌ Complex condition triggered - both adrenal and thyroid will be skipped!")
    else:
        print("  ✅ No complex condition - will process individual indicators")

    # Process individual health indicators
    health_map = {
        'insulin_sensitivity': '인슐린 민감도',
        'autonomic_nervous_system': '자율신경계',
        'stress_state': '스트레스 상태',
        'immune_skin_health': '면역 및 피부 건강',
        'adrenal_activity': '부신 활성도',
        'thyroid_activity': '갑상선 활성도'
    }

    print("\n🔍 Processing individual health indicators:")
    for health_key, health_name in health_map.items():
        if health_key in indicators_to_skip:
            print(f"  - {health_name}: SKIPPED (in skip list)")
            continue

        health_value = getattr(health, health_key)
        print(f"  - {health_name}: {health_value}")

        if health_value in [TestResultValue.HIGH, TestResultValue.LOW]:
            value_str = "높음" if health_value == TestResultValue.HIGH else "낮음"
            print(f"    → Processing {health_name} - {value_str}")

            health_content = service._extract_health_condition(note4_content, health_name, value_str, age, name, test_data)
            if health_content:
                print(f"    ✅ Content found: {health_content[:100]}...")
                content_parts.append(f"{health_content}")
            else:
                print(f"    ❌ No content found for {health_name} - {value_str}")
        else:
            print(f"    → Normal value, skipping")

    print(f"\n📊 Final result:")
    print(f"  - Content parts count: {len(content_parts)}")
    print(f"  - Combined result:")
    final_result = "\n\n".join(content_parts)
    print(f"    {final_result}")

    # Test the _extract_health_condition method directly for both indicators
    print("\n🔍 Direct _extract_health_condition tests:")

    # Test stress state
    stress_content = service._extract_health_condition(note4_content, "스트레스 상태", "높음", age, name, test_data)
    print(f"  - 스트레스 상태 - 높음: {'✅ Found' if stress_content else '❌ Not found'}")
    if stress_content:
        print(f"    Content: {stress_content[:100]}...")

    # Test adrenal activity
    adrenal_content = service._extract_health_condition(note4_content, "부신 활성도", "높음", age, name, test_data)
    print(f"  - 부신 활성도 - 높음: {'✅ Found' if adrenal_content else '❌ Not found'}")
    if adrenal_content:
        print(f"    Content: {adrenal_content[:100]}...")

if __name__ == "__main__":
    debug_simple_health_extraction()