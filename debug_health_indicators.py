#!/usr/bin/env python3
"""
Debug script to investigate health indicators analysis issue.
The user reports that health indicators with "높음" (high) values are not being
reflected in the comprehensive analysis results.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.models.input_models import (
    HairAnalysisInput, PersonalInfo, HeavyMetals, NutritionalMinerals,
    HealthIndicators, TestResultValue, HeavyMetalValue
)
from backend.app.services.analysis_service import HairAnalysisService

def create_test_case_from_screenshot():
    """Create test case based on the user's screenshot values"""
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
            insulin_sensitivity=TestResultValue.NORMAL,     # 정상
            autonomic_nervous_system=TestResultValue.NORMAL, # 정상
            stress_state=TestResultValue.HIGH,               # 높음 ⭐
            immune_skin_health=TestResultValue.NORMAL,       # 정상
            adrenal_activity=TestResultValue.HIGH,           # 높음 ⭐
            thyroid_activity=TestResultValue.NORMAL          # 정상
        )
    )

def debug_health_indicators_processing():
    """Debug the health indicators processing logic"""
    print("🔍 Debugging Health Indicators Analysis")
    print("=" * 60)

    # Create test case
    test_data = create_test_case_from_screenshot()
    print("✅ Test data created with health indicators:")
    print(f"   스트레스 상태: {test_data.health_indicators.stress_state}")
    print(f"   부신 활성도: {test_data.health_indicators.adrenal_activity}")
    print()

    # Initialize service
    service = HairAnalysisService()

    # Check if note4 is loaded
    note4_content = service.notes_cache.get("note4_health_indicators", "")
    if not note4_content:
        print("❌ ERROR: note4_health_indicators.md not loaded!")
        return
    else:
        print(f"✅ note4_health_indicators.md loaded ({len(note4_content)} characters)")

    # Test health indicators analysis extraction
    print("\n🔍 Testing _extract_health_indicators_analysis method...")
    health_analysis = service._extract_health_indicators_analysis(test_data)

    print(f"\n📋 Health Indicators Analysis Result:")
    print("-" * 40)
    if health_analysis:
        print(health_analysis)
    else:
        print("❌ NO CONTENT RETURNED!")

    # Test individual health content extraction
    print(f"\n🔍 Testing individual health indicator extraction...")

    # Test stress state (높음)
    print(f"\n1️⃣ Testing 스트레스 상태 - 높음:")
    stress_content = service._extract_individual_health_content(
        note4_content, "스트레스 상태", "높음", "20세 이상", False, "테스트"
    )
    if stress_content:
        print(f"✅ Found: {stress_content[:100]}...")
    else:
        print("❌ No content found for 스트레스 상태 - 높음")

    # Test adrenal activity (높음)
    print(f"\n2️⃣ Testing 부신 활성도 - 높음:")
    adrenal_content = service._extract_individual_health_content(
        note4_content, "부신 활성도", "높음", "20세 이상", False, "테스트"
    )
    if adrenal_content:
        print(f"✅ Found: {adrenal_content[:100]}...")
    else:
        print("❌ No content found for 부신 활성도 - 높음")

    # Debug section pattern matching
    print(f"\n🔍 Debugging section pattern matching...")

    # Check if stress section exists
    import re
    stress_pattern = r"^## .{1,3} 스트레스 상태$.*?(?=\n## |\Z)"
    stress_match = re.search(stress_pattern, note4_content, re.DOTALL | re.MULTILINE)
    if stress_match:
        print("✅ Found 스트레스 상태 section")
        stress_section = stress_match.group(0)

        # Check for 스트레스 상태 - 높음 subsection
        stress_high_pattern = r"### 스트레스 상태 - 높음.*?\*\*최종 멘트\*\*:\s*(.*?)(?=\n### |\n---|\Z)"
        stress_high_match = re.search(stress_high_pattern, stress_section, re.DOTALL)
        if stress_high_match:
            print("✅ Found 스트레스 상태 - 높음 subsection")
            print(f"   Content: {stress_high_match.group(1)[:100]}...")
        else:
            print("❌ No 스트레스 상태 - 높음 subsection found")
    else:
        print("❌ No 스트레스 상태 section found")

    # Check adrenal section
    adrenal_pattern = r"^## .{1,3} 부신 활성도$.*?(?=\n## |\Z)"
    adrenal_match = re.search(adrenal_pattern, note4_content, re.DOTALL | re.MULTILINE)
    if adrenal_match:
        print("✅ Found 부신 활성도 section")
        adrenal_section = adrenal_match.group(0)

        # Check for 부신 활성도 - 높음 (일반) subsection
        adrenal_high_pattern = r"### 부신 활성도 - 높음 \(일반\).*?\*\*최종 멘트\*\*:\s*(.*?)(?=\n### |\n---|\Z)"
        adrenal_high_match = re.search(adrenal_high_pattern, adrenal_section, re.DOTALL)
        if adrenal_high_match:
            print("✅ Found 부신 활성도 - 높음 (일반) subsection")
            print(f"   Content: {adrenal_high_match.group(1)[:100]}...")
        else:
            print("❌ No 부신 활성도 - 높음 (일반) subsection found")
    else:
        print("❌ No 부신 활성도 section found")

    # Run full analysis and check comprehensive result
    print(f"\n🔍 Running full analysis...")
    full_result = service.analyze(test_data)

    print(f"\n📋 Comprehensive Analysis Result:")
    print("-" * 40)
    print(f"First Paragraph: {full_result.comprehensive_analysis.first_paragraph}")
    print(f"\nHealth Indicators Analysis: {full_result.comprehensive_analysis.health_indicators_analysis}")

    print(f"\n" + "=" * 60)
    print("🔍 Analysis Complete")

if __name__ == "__main__":
    debug_health_indicators_processing()