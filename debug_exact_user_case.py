#!/usr/bin/env python3
"""
Debug script with the exact same values as shown in the user's screenshot.
Based on the screenshot, the user had 6총 (6 items) with multiple "높음" selections.

From the screenshot, the user selected:
- 인슐린 민감도: 정상
- 자율신경계: 정상
- 스트레스 상태: 높음
- 면역 및 피부 건강: 정상
- 부신 활성도: 높음
- 갑상선 활성도: 정상

But the comprehensive analysis only showed generic text about balanced minerals.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.models.input_models import (
    HairAnalysisInput, PersonalInfo, HeavyMetals, NutritionalMinerals,
    HealthIndicators, TestResultValue, HeavyMetalValue
)
from backend.app.services.analysis_service import HairAnalysisService
import json

def create_exact_user_case():
    """Create the exact case from user's screenshot"""
    return HairAnalysisInput(
        personal_info=PersonalInfo(
            name="사용자",
            age=35,  # Assuming adult age
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
            insulin_sensitivity=TestResultValue.NORMAL,     # 정상 ✓
            autonomic_nervous_system=TestResultValue.NORMAL, # 정상 ✓
            stress_state=TestResultValue.HIGH,               # 높음 ⭐
            immune_skin_health=TestResultValue.NORMAL,       # 정상 ✓
            adrenal_activity=TestResultValue.HIGH,           # 높음 ⭐
            thyroid_activity=TestResultValue.NORMAL          # 정상 ✓
        )
    )

def test_exact_user_case():
    """Test the exact user case and show detailed results"""
    print("🧪 Testing Exact User Case from Screenshot")
    print("=" * 70)

    # Create the exact case
    user_data = create_exact_user_case()

    print("📋 Input Data Summary:")
    print(f"   Name: {user_data.personal_info.name}")
    print(f"   Age: {user_data.personal_info.age}")
    print(f"   Heavy Metals: All NORMAL")
    print(f"   Nutritional Minerals: All NORMAL")
    print(f"   Health Indicators:")
    print(f"     - 인슐린 민감도: {user_data.health_indicators.insulin_sensitivity}")
    print(f"     - 자율신경계: {user_data.health_indicators.autonomic_nervous_system}")
    print(f"     - 스트레스 상태: {user_data.health_indicators.stress_state} ⭐")
    print(f"     - 면역 및 피부 건강: {user_data.health_indicators.immune_skin_health}")
    print(f"     - 부신 활성도: {user_data.health_indicators.adrenal_activity} ⭐")
    print(f"     - 갑상선 활성도: {user_data.health_indicators.thyroid_activity}")
    print()

    # Initialize service and run analysis
    service = HairAnalysisService()
    result = service.analyze(user_data)

    print("📊 Full Analysis Result:")
    print("-" * 50)

    print("🔸 Personal Info Section:")
    print(f"   Normal health indicators: {result.personal_info_section.health_normal}")
    print(f"   High health indicators: {result.personal_info_section.health_high}")
    print(f"   Low health indicators: {result.personal_info_section.health_low}")
    print()

    print("🔸 Comprehensive Analysis:")
    print(f"   First Paragraph: {result.comprehensive_analysis.first_paragraph}")
    print(f"   Heavy Metals Analysis: {result.comprehensive_analysis.heavy_metals_analysis}")
    print(f"   Minerals Analysis: {result.comprehensive_analysis.minerals_analysis}")
    print(f"   Health Indicators Analysis:")
    print(f"   {result.comprehensive_analysis.health_indicators_analysis}")
    print()

    print("🔸 Summary Explanation:")
    print(f"   Title: {result.summary_explanation.title}")
    print(f"   Recommended Foods: {result.summary_explanation.recommended_foods}")
    print(f"   Recommended Supplements: {result.summary_explanation.recommended_supplements}")
    print(f"   Recheck Period: {result.summary_explanation.recheck_period}")
    print()

    # Test what happens if we have some mineral imbalances
    print("🧪 Testing with mineral imbalances (to see if that's causing the issue)...")
    user_data_with_minerals = create_exact_user_case()
    user_data_with_minerals.nutritional_minerals.sodium = TestResultValue.HIGH
    user_data_with_minerals.nutritional_minerals.potassium = TestResultValue.HIGH

    result_with_minerals = service.analyze(user_data_with_minerals)
    print("🔸 With Mineral Imbalances:")
    print(f"   First Paragraph: {result_with_minerals.comprehensive_analysis.first_paragraph}")
    print(f"   Minerals Analysis: {result_with_minerals.comprehensive_analysis.minerals_analysis}")
    print(f"   Health Indicators Analysis: {result_with_minerals.comprehensive_analysis.health_indicators_analysis}")
    print()

    # Check if the issue is in the simple analysis service used by the API
    print("🧪 Testing Simple Analysis Service (used by API)...")
    from backend.app.services.simple_analysis_service import SimpleHairAnalysisService
    simple_service = SimpleHairAnalysisService()
    simple_result = simple_service.analyze(user_data)

    print("🔸 Simple Analysis Result:")
    print(f"   Data: {json.dumps(simple_result.dict(), ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    test_exact_user_case()