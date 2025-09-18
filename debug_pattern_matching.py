#!/usr/bin/env python3
"""
Debug script to investigate pattern matching issues in Simple Analysis Service.
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

def debug_pattern_matching():
    """Debug pattern matching for adrenal activity extraction"""
    print("🔍 Debugging Pattern Matching for 부신 활성도 - 높음")
    print("=" * 70)

    service = SimpleHairAnalysisService()
    note4_content = service.notes_cache.get("note4_health_indicators", "")

    if not note4_content:
        print("❌ ERROR: note4_health_indicators.md not loaded!")
        return

    print(f"✅ note4_health_indicators.md loaded ({len(note4_content)} characters)")

    # Test the patterns used in _extract_health_condition for adrenal activity
    health_name = "부신 활성도"
    value = "높음"
    age = 30  # 20세 이상

    print(f"\n📋 Testing patterns for: {health_name} - {value} (age: {age})")

    # The patterns from _extract_health_condition method
    patterns_to_try = []

    # 특별 조건들 (none for 부신 활성도 높음)
    # 일반적인 연령별 조건
    if age <= 19:
        patterns_to_try.append(f"### {health_name} - {value} \\(19세 이하\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")
    else:
        patterns_to_try.append(f"### {health_name} - {value} \\(20세 이상\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")

    # 전 연령 조건
    patterns_to_try.append(f"### {health_name} - {value}\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")

    print(f"\n🔍 Trying patterns:")
    for i, pattern in enumerate(patterns_to_try, 1):
        print(f"\n{i}. Pattern: {pattern}")
        match = re.search(pattern, note4_content, re.DOTALL)
        if match:
            content = match.group(1).strip()
            print(f"   ✅ Match found: {content[:100]}...")
            break
        else:
            print(f"   ❌ No match")

    # Let's manually check what sections exist for 부신 활성도
    print(f"\n🔍 Manual search for 부신 활성도 sections:")

    # Find all 부신 활성도 sections
    adrenal_sections = re.findall(r'### 부신 활성도[^\n]*\n.*?(?=### |$)', note4_content, re.DOTALL)
    print(f"Found {len(adrenal_sections)} 부신 활성도 sections:")

    for i, section in enumerate(adrenal_sections, 1):
        # Extract just the header
        header = section.split('\n')[0]
        print(f"  {i}. {header}")

    # Look specifically for "부신 활성도 - 높음" patterns
    print(f"\n🔍 Looking for 부신 활성도 - 높음 patterns:")

    # Try different variations
    test_patterns = [
        r"### 부신 활성도 - 높음.*?\*\*최종 멘트\*\*: (.+?)(?=\n### |\n---|\Z)",
        r"### 부신 활성도 - 높음 \(일반\).*?\*\*최종 멘트\*\*: (.+?)(?=\n### |\n---|\Z)",
        r"### 부신 활성도 - 높음 \(20세 이상\).*?\*\*최종 멘트\*\*: (.+?)(?=\n### |\n---|\Z)",
        r"### 부신 활성도 - 높음.*?\*\*최종 멘트\*\*:\s*(.*?)(?=\n### |\n---|\Z)",
    ]

    for i, pattern in enumerate(test_patterns, 1):
        print(f"\n{i}. Testing pattern: {pattern}")
        matches = re.findall(pattern, note4_content, re.DOTALL)
        if matches:
            print(f"   ✅ Found {len(matches)} matches:")
            for j, match in enumerate(matches, 1):
                print(f"     {j}. {match.strip()[:100]}...")
        else:
            print(f"   ❌ No matches")

    # Show the actual content around 부신 활성도 section
    print(f"\n🔍 Actual content around 부신 활성도 section:")
    adrenal_start = note4_content.find("## ⚡ 부신 활성도")
    if adrenal_start != -1:
        # Find the end of this section (next ## or end of file)
        next_section = note4_content.find("\n## ", adrenal_start + 1)
        if next_section == -1:
            adrenal_section = note4_content[adrenal_start:]
        else:
            adrenal_section = note4_content[adrenal_start:next_section]

        print("Content:")
        print("-" * 50)
        print(adrenal_section[:1000])  # Show first 1000 characters
        print("-" * 50)
    else:
        print("❌ No 부신 활성도 section found!")

if __name__ == "__main__":
    debug_pattern_matching()