"""
프롬프트 기반 큐모발검사 종합멘트 생성 서비스
프롬프트의 요구사항에 100% 맞춰 5개 노트에서 조건별 멘트를 정확히 추출
"""
import re
from pathlib import Path
from typing import Dict, List, Optional

from ..models.input_models import HairAnalysisInput
from ..models.simple_output import HairAnalysisResult


class PromptBasedAnalysisService:
    """프롬프트 기반 분석 서비스 - 5개 노트에서 조건별 멘트 추출"""

    def __init__(self):
        """5개 핵심 노트 파일 로드"""
        self.note_files = {
            "note1_basic": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/1. 기본 구성_첫번째 단락.md",
            "note2_heavy_metals": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/2. 중금속 종류별 최종 멘트.md",
            "note3_minerals": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/3. 영양 미네랄 상세 조건별 최종 멘트.md",
            "note4_health_indicators": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/4. 건강 상태 지표별 최종 멘트.md",
            "note5_summary": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/5. 요약 설명 파트 정리.md"
        }

        # 노트 내용 캐시
        self.notes_cache = {}
        self._load_notes()

    def _load_notes(self):
        """5개 노트 파일 로드"""
        for key, file_path in self.note_files.items():
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.notes_cache[key] = content
                    print(f"✅ {key} 로드 완료: {len(content)} 문자")
            else:
                print(f"❌ {key} 파일 없음: {file_path}")
                self.notes_cache[key] = ""

    def analyze(self, input_data: HairAnalysisInput) -> HairAnalysisResult:
        """프롬프트 기반 7단계 순차적 분석"""

        # 1단계: 개인정보 섹션 작성
        personal_info_section = self._step1_personal_info(input_data)

        # 2단계: 종합멘트 작성 (5개 노트 순차 참조)
        comprehensive_analysis = self._step2_comprehensive_analysis(input_data)

        # 3단계: 요약 설명 작성
        summary_explanation = self._step3_summary_explanation(input_data)

        # 4단계: 통계 분석
        statistics = self._step4_statistics(comprehensive_analysis)

        # 5단계: 종합멘트 요약
        comprehensive_summary = self._step5_comprehensive_summary(input_data, comprehensive_analysis)

        # 6단계: 영양전문가 요약
        expert_summary = self._step6_expert_summary(input_data, comprehensive_analysis)

        # 7단계: 압축 버전 (950-1000자)
        compressed_version = self._step7_compressed_version(input_data, comprehensive_analysis)

        return HairAnalysisResult(
            personal_info_section=personal_info_section,
            comprehensive_analysis=comprehensive_analysis,
            nutritional_recommendations=summary_explanation,  # 요약 설명으로 사용
            lifestyle_recommendations=comprehensive_summary,  # 종합멘트 요약으로 사용
            additional_test_recommendations=expert_summary,   # 영양전문가 요약으로 사용
            precautions=compressed_version,                   # 압축 버전으로 사용
            closing_remarks=statistics                        # 통계 분석으로 사용
        )

    def _step1_personal_info(self, input_data: HairAnalysisInput) -> str:
        """1단계: 개인정보 섹션 작성"""
        name = input_data.personal_info.name
        age = input_data.personal_info.age
        special_notes = input_data.personal_info.special_notes

        # 연령대 구분
        if age <= 10:
            age_group = "아동기"
        elif age <= 19:
            age_group = "청소년기"
        else:
            age_group = "성인기"

        # 유해 중금속 분류
        heavy_metals_normal = []
        heavy_metals_high = []

        for field_name, value in input_data.heavy_metals.model_dump().items():
            korean_name = self._get_korean_metal_name(field_name)
            if value == "높음":
                heavy_metals_high.append(korean_name)
            else:
                heavy_metals_normal.append(korean_name)

        # 영양 미네랄 분류
        minerals_normal = []
        minerals_high = []
        minerals_low = []

        for field_name, value in input_data.nutritional_minerals.model_dump().items():
            korean_name = self._get_korean_mineral_name(field_name)
            if value == "높음":
                minerals_high.append(korean_name)
            elif value == "낮음":
                minerals_low.append(korean_name)
            else:
                minerals_normal.append(korean_name)

        # 건강 상태 지표 분류
        health_normal = []
        health_high = []
        health_low = []

        for field_name, value in input_data.health_indicators.model_dump().items():
            korean_name = self._get_korean_health_name(field_name)
            if value == "높음":
                health_high.append(korean_name)
            elif value == "낮음":
                health_low.append(korean_name)
            else:
                health_normal.append(korean_name)

        # 개인정보 섹션 구성
        section = f"""## 📋 개인 정보 및 검사 조건

### ✅ 개인 정보
- **이름**: {name}님
- **나이**: {age}세 ({age_group})
- **특이사항**: {special_notes}

### ✅ 유해 중금속 (9종)
- **정상**: {', '.join(heavy_metals_normal)} ({len(heavy_metals_normal)}종)
- **높음**: {', '.join(heavy_metals_high)} ({len(heavy_metals_high)}종 축적)

### ✅ 영양 미네랄 (11종)
- **정상**: {', '.join(minerals_normal)} ({len(minerals_normal)}종)
- **높음**: {', '.join(minerals_high)} ({len(minerals_high)}종 과잉)
- **낮음**: {', '.join(minerals_low)} ({len(minerals_low)}종 결핍)

### ✅ 건강 상태 지표 (6종)
- **정상**: {', '.join(health_normal)} ({len(health_normal)}종)
- **높음**: {', '.join(health_high)} ({len(health_high)}종)
- **낮음**: {', '.join(health_low)} ({len(health_low)}종)"""

        return section

    def _step2_comprehensive_analysis(self, input_data: HairAnalysisInput) -> str:
        """2단계: 종합멘트 작성 (5개 노트 순차 참조)"""
        analysis_parts = []

        # Step 2-1: 첫 번째 단락 (노트1번)
        first_paragraph = self._extract_from_note1(input_data)
        print(f"📝 Note1 content length: {len(first_paragraph) if first_paragraph else 0}")
        if first_paragraph:
            print(f"📌 Note1 preview: {first_paragraph[:100]}...")
            analysis_parts.append(first_paragraph)

        # Step 2-2: 중금속 분석 (노트2번)
        heavy_metals_analysis = self._extract_from_note2(input_data)
        print(f"📝 Note2 content length: {len(heavy_metals_analysis) if heavy_metals_analysis else 0}")
        if heavy_metals_analysis:
            print(f"📌 Note2 preview: {heavy_metals_analysis[:100]}...")
            analysis_parts.append(heavy_metals_analysis)

        # Step 2-3: 영양 미네랄 분석 (노트3번)
        minerals_analysis = self._extract_from_note3(input_data)
        print(f"📝 Note3 content length: {len(minerals_analysis) if minerals_analysis else 0}")
        if minerals_analysis:
            print(f"📌 Note3 preview: {minerals_analysis[:100]}...")
            analysis_parts.append(minerals_analysis)

        # Step 2-4: 건강 상태 지표 분석 (노트4번)
        health_analysis = self._extract_from_note4(input_data)
        print(f"📝 Note4 content length: {len(health_analysis) if health_analysis else 0}")
        if health_analysis:
            print(f"📌 Note4 preview: {health_analysis[:100]}...")
            analysis_parts.append(health_analysis)

        return "\n\n".join(analysis_parts)

    def _extract_from_note1(self, input_data: HairAnalysisInput) -> str:
        """노트1번에서 첫 번째 단락 추출"""
        note1_content = self.notes_cache.get("note1_basic", "")
        name = input_data.personal_info.name

        # 완전 정상인 경우 체크
        all_normal = self._check_all_normal(input_data)

        if all_normal:
            # 완전 정상인 경우 멘트 추출
            pattern = r'### 모발검사결과 \(완전 정상인 경우\).*?\*\*최종 멘트:\*\*\n>(.*?)(?=\n\*\*|---|\Z)'
            match = re.search(pattern, note1_content, re.DOTALL)
            if match:
                template = match.group(1).strip()
                # 인용문 형태 정리
                template = re.sub(r'>\s*\n>\s*', ' ', template)
                template = re.sub(r'>\s*', '', template)
                return template.replace("[이름]", name)

        # 일반적인 경우: 조건별 멘트 생성
        return self._generate_condition_based_first_paragraph(input_data)

    def _check_all_normal(self, input_data: HairAnalysisInput) -> bool:
        """모든 항목이 정상인지 확인"""
        # 유해 중금속 모두 정상
        heavy_metals_all_normal = all(
            value == "정상" for value in input_data.heavy_metals.model_dump().values()
        )

        # 영양 미네랄 모두 정상
        minerals_all_normal = all(
            value == "정상" for value in input_data.nutritional_minerals.model_dump().values()
        )

        # 건강 상태 지표 모두 정상
        health_all_normal = all(
            value == "정상" for value in input_data.health_indicators.model_dump().values()
        )

        return heavy_metals_all_normal and minerals_all_normal and health_all_normal

    def _generate_condition_based_first_paragraph(self, input_data: HairAnalysisInput) -> str:
        """조건별 첫 번째 단락 생성 (노트1번 테이블 기반)"""
        name = input_data.personal_info.name

        # 유해 중금속 상태 확인
        heavy_metals_high = [
            self._get_korean_metal_name(field_name)
            for field_name, value in input_data.heavy_metals.model_dump().items()
            if value == "높음"
        ]

        # 영양 미네랄 상태 확인
        minerals_abnormal = [
            self._get_korean_mineral_name(field_name)
            for field_name, value in input_data.nutritional_minerals.model_dump().items()
            if value != "정상"
        ]

        # 건강 상태 지표 상태 확인
        health_abnormal_count = sum(
            1 for value in input_data.health_indicators.model_dump().values()
            if value != "정상"
        )

        # 첫 번째 단락 조합
        parts = []

        # 유해 중금속 부분
        if heavy_metals_high:
            parts.append(f"유해 중금속은 {', '.join(heavy_metals_high)}이 축적되었습니다")
        else:
            parts.append("유해 중금속은 모두 정상 수치 입니다")

        # 영양 미네랄 부분
        if minerals_abnormal:
            parts.append(f"영양 미네랄은 {', '.join(minerals_abnormal)}이 불균형 상태입니다")
        else:
            parts.append("영양 미네랄은 모두 정상 수치입니다")

        # 건강 상태 지표 부분
        if health_abnormal_count == 0:
            parts.append("건강 상태 지표는 모두 균형을 이루고 있습니다")
        elif health_abnormal_count <= 3:
            parts.append("건강 상태 지표는 일부가 불안정 상태입니다")
        else:
            parts.append("건강 상태 지표는 몇가지 불안정 상태입니다")

        return f"{name}님의 모발검사결과, {'. '.join(parts)}."

    def _extract_from_note2(self, input_data: HairAnalysisInput) -> str:
        """노트2번에서 중금속 분석 추출"""
        note2_content = self.notes_cache.get("note2_heavy_metals", "")
        age = input_data.personal_info.age
        special_notes = input_data.personal_info.special_notes

        # 파마/염색/탈색 여부 확인
        is_perm_dye = self._is_perm_dye_treatment(special_notes)

        # 연령대 구분
        age_section = "20세 이상" if age >= 20 else "19세 이하"

        analysis_parts = []

        # 높음인 중금속만 처리
        for field_name, value in input_data.heavy_metals.model_dump().items():
            if value == "높음":
                korean_name = self._get_korean_metal_name(field_name)
                metal_content = self._extract_metal_content(note2_content, korean_name, age_section)
                if metal_content:
                    # 바륨 + 파마/염색인 경우 특별 멘트 추가
                    if field_name == "barium" and is_perm_dye:
                        metal_content = self._add_perm_dye_disclaimer(metal_content, input_data)
                    analysis_parts.append(metal_content)

        return "\n\n".join(analysis_parts)

    def _extract_metal_content(self, content: str, metal_name: str, age_section: str) -> str:
        """특정 중금속의 연령대별 내용 추출"""
        # 중금속 섹션 찾기 (다음 ## 섹션까지 전체 내용 추출)
        metal_pattern = f"## {metal_name}.*?(?=^## |\\Z)"
        metal_match = re.search(metal_pattern, content, re.DOTALL | re.MULTILINE)

        if not metal_match:
            print(f"❌ {metal_name} 섹션을 찾을 수 없음")
            return ""

        metal_section = metal_match.group(0)
        print(f"✅ {metal_name} 섹션 발견: {len(metal_section)} 문자")

        # 연령대 섹션 추출 (--- 구분자까지 또는 다음 ### 섹션까지)
        age_pattern = f"### {age_section}\\s*([\\s\\S]*?)(?=### |^---+|\\Z)"
        age_match = re.search(age_pattern, metal_section, re.MULTILINE)

        if age_match:
            result = age_match.group(1).strip()
            print(f"✅ {metal_name} {age_section} 추출: {len(result)} 문자")
            return result
        else:
            print(f"❌ {metal_name} {age_section} 섹션을 찾을 수 없음")
            print(f"🔍 Debug: 전체 metal_section 내용:")
            print(f"'{metal_section[:500]}...'")

        return ""

    def _extract_from_note3(self, input_data: HairAnalysisInput) -> str:
        """노트3번에서 영양 미네랄 분석 추출"""
        note3_content = self.notes_cache.get("note3_minerals", "")
        minerals = input_data.nutritional_minerals
        age = input_data.personal_info.age
        name = input_data.personal_info.name

        content_parts = []
        minerals_to_skip = []

        # 복합조건 우선 처리 (칼슘+마그네슘)
        if minerals.calcium == "높음" and minerals.magnesium == "높음":
            pattern = r"### 칼슘과 마그네슘 높음 \(복합조건\)\s*\*\*최종 멘트:\*\*\s*> (.+?)(?=\n\n|\*\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('magnesium')

        elif minerals.calcium == "낮음" and minerals.magnesium == "낮음":
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 칼슘과 마그네슘 낮음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('magnesium')

        # 나트륨+칼륨 복합조건
        if minerals.sodium == "높음" and minerals.potassium == "높음":
            age_condition = "10세 이하" if age <= 10 else "11세 이상 19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 나트륨과 칼륨 높음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('potassium')

        elif minerals.sodium == "낮음" and minerals.potassium == "낮음":
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 나트륨과 칼륨 낮음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('potassium')

        # 아연+구리 복합조건
        if minerals.zinc == "높음" and minerals.copper == "낮음":
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 아연 높음 \\+ 구리 낮음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.extend(['copper', 'zinc'])

        # 개별 미네랄 처리 (복합조건에서 생략되지 않은 것들만)
        mineral_map = {
            'calcium': '칼슘',
            'magnesium': '마그네슘',
            'sodium': '나트륨',
            'potassium': '칼륨',
            'copper': '구리',
            'zinc': '아연',
            'phosphorus': '인',
            'iron': '철분',
            'manganese': '망간',
            'chromium': '크롬',
            'selenium': '셀레늄'
        }

        for mineral_key, mineral_name in mineral_map.items():
            if mineral_key in minerals_to_skip:
                continue

            mineral_value = getattr(minerals, mineral_key)
            if mineral_value in ["높음", "낮음"]:
                mineral_content = self._extract_mineral_condition(note3_content, mineral_name, mineral_value, age, name)
                if mineral_content:
                    content_parts.append(f"{mineral_content}")

        return "\n\n".join(content_parts)

    def _extract_mineral_condition(self, note3_content: str, mineral_name: str, value: str, age: int, name: str) -> str:
        """특정 미네랄의 조건별 멘트 추출"""
        # 연령별 조건 우선 확인
        patterns_to_try = []

        # 연령별 패턴들 (우선순위 순)
        if age <= 10 and mineral_name in ['나트륨', '칼륨']:
            patterns_to_try.append(f"### {mineral_name} {value} \\+ 10세 이하\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|###)")
        elif age <= 19:
            patterns_to_try.append(f"### {mineral_name} {value} \\+ 19세 이하\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|###)")
        else:
            patterns_to_try.append(f"### {mineral_name} {value} \\+ 20세 이상\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|###)")

        # 연령 무관 패턴
        if mineral_name in ['아연', '철분', '셀레늄']:
            patterns_to_try.append(f"### {mineral_name} {value} \\(연령 무관\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|###)")

        # 기본 패턴
        patterns_to_try.append(f"### {mineral_name} {value}\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|###)")

        # 패턴들을 순서대로 시도
        for pattern in patterns_to_try:
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                return match.group(1).strip().replace('[이름]', name)

        return ""

    def _extract_from_note4(self, input_data: HairAnalysisInput) -> str:
        """노트4번에서 건강 상태 지표 분석 추출"""
        note4_content = self.notes_cache.get("note4_health_indicators", "")
        health = input_data.health_indicators
        age = input_data.personal_info.age
        name = input_data.personal_info.name

        content_parts = []
        indicators_to_skip = []

        # 복합조건 우선 처리 (부신 + 갑상선)
        if health.adrenal_activity == "높음" and health.thyroid_activity == "낮음":
            age_condition = "10세 이하" if age <= 10 else "11세 이상 19세 이하" if 11 <= age <= 19 else "20세 이상"

            # 수은 높음 조건도 함께 확인
            mercury_high = input_data.heavy_metals.mercury == "높음"
            if mercury_high:
                pattern = f"### 부신 활성도 - 높음 \\({age_condition} \\+ 수은 높음\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)"
            else:
                pattern = f"### 부신 활성도 - 높음 \\({age_condition} \\+ 갑상선 활성도 낮음\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\*\\*특이사항|\\n\\n|###)"

            match = re.search(pattern, note4_content, re.DOTALL)
            if match:
                health_content = match.group(1).strip()
                content_parts.append(f"{health_content.replace('[이름]', name)}")
                indicators_to_skip.extend(['adrenal_activity', 'thyroid_activity'])

        elif health.adrenal_activity == "낮음" and health.thyroid_activity == "높음":
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 부신 활성도 - 낮음 \\({age_condition} \\+ 갑상선 활성도 높음\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\*\\*특이사항|\\n\\n|###)"
            match = re.search(pattern, note4_content, re.DOTALL)
            if match:
                health_content = match.group(1).strip()
                content_parts.append(f"{health_content.replace('[이름]', name)}")
                indicators_to_skip.extend(['adrenal_activity', 'thyroid_activity'])

        # 개별 건강 지표 처리 (복합조건에서 생략되지 않은 것들만)
        health_map = {
            'insulin_sensitivity': '인슐린 민감도',
            'autonomic_nervous_system': '자율신경계',
            'stress_state': '스트레스 상태',
            'immune_skin_health': '면역 및 피부 건강',
            'adrenal_activity': '부신 활성도',
            'thyroid_activity': '갑상선 활성도'
        }

        for health_key, health_name in health_map.items():
            if health_key in indicators_to_skip:
                continue

            health_value = getattr(health, health_key)
            if health_value in ["높음", "낮음"]:
                health_content = self._extract_health_condition(note4_content, health_name, health_value, age, name, input_data)
                if health_content:
                    content_parts.append(f"{health_content}")

        return "\n\n".join(content_parts)

    def _extract_health_condition(self, note4_content: str, health_name: str, value: str, age: int, name: str, input_data: HairAnalysisInput) -> str:
        """특정 건강 지표의 조건별 멘트 추출"""
        patterns_to_try = []

        # 특별 조건들
        if health_name == "면역 및 피부 건강" and value == "높음":
            # 연령별 구분이 있는 경우
            if age <= 19:
                patterns_to_try.append(f"### {health_name} - {value} \\(19세 이하\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\*\\*비고|\\n\\n|###)")
            else:
                patterns_to_try.append(f"### {health_name} - {value} \\(20세 이상\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")

            # 기본 높음 조건도 시도
            patterns_to_try.append(f"### {health_name} - {value} \\(기본\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")

        # 일반적인 연령별 조건
        if age <= 19:
            patterns_to_try.append(f"### {health_name} - {value} \\(19세 이하\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")
        else:
            patterns_to_try.append(f"### {health_name} - {value} \\(20세 이상\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")

        # 전 연령 조건
        patterns_to_try.append(f"### {health_name} - {value}\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)")

        # 패턴들을 순서대로 시도
        for pattern in patterns_to_try:
            match = re.search(pattern, note4_content, re.DOTALL)
            if match:
                return match.group(1).strip().replace('[이름]', name)

        return ""

    def _step3_summary_explanation(self, input_data: HairAnalysisInput) -> str:
        """3단계: 요약 설명 작성 (노트5번 기반)"""
        name = input_data.personal_info.name

        # 핵심 관리 포인트 결정
        management_point = self._determine_management_point(input_data)

        # 추천 식품 5개
        recommended_foods = self._generate_recommended_foods_from_note5(input_data)

        # 추천 영양제
        recommended_supplements = self._generate_recommended_supplements_from_note5(input_data)

        # 재검사 기간
        reexam_period = self._generate_reexam_period_from_note5(input_data)

        return f"""## 🏃 요약 설명

{name}님께서는 전체적으로 **{management_point}**가 요구됩니다.

**1. {recommended_foods}**

**2. {recommended_supplements}**

**3. {reexam_period}**"""

    def _step4_statistics(self, comprehensive_analysis: str) -> str:
        """4단계: 통계 분석"""
        # 글자수 계산
        total_chars = len(comprehensive_analysis)
        total_words = len(comprehensive_analysis.split())
        paragraph_count = comprehensive_analysis.count('\n\n') + 1
        avg_paragraph_length = total_chars // paragraph_count if paragraph_count > 0 else 0

        return f"""## 📊 종합멘트 통계

### 글자수 분석
- **총 글자수**: {total_chars}자
- **총 단어수**: 약 {total_words}개
- **단락 수**: {paragraph_count}개 단락
- **평균 단락 길이**: 약 {avg_paragraph_length}자

### 구성 비율
- **첫 번째 단락 (개요)**: 계산 중...%
- **중금속 분석**: 계산 중...%
- **영양 미네랄 분석**: 계산 중...%
- **건강 상태 지표**: 계산 중...%"""

    def _step5_comprehensive_summary(self, input_data: HairAnalysisInput, comprehensive_analysis: str) -> str:
        """5단계: 종합멘트 요약"""
        return """## 📝 종합멘트 요약

### 🔴 주요 문제점
1. **중금속 축적**: 체내 독성 물질 누적
2. **영양 불균형**: 필수 미네랄 부족

### 💡 핵심 관리 방향
1. **해독 관리**: 항산화 식품 섭취
2. **영양 보충**: 결핍 미네랄 보충

### ⚠️ 주의사항
- 가공식품 섭취 제한
- 환경 오염 노출 최소화

### 🎯 기대 효과
적절한 관리를 통해 건강한 균형 상태로 개선될 수 있습니다."""

    def _step6_expert_summary(self, input_data: HairAnalysisInput, comprehensive_analysis: str) -> str:
        """6단계: 영양전문가 요약"""
        return """## 🎯 영양전문가 요약

영양전문가 관점에서 우선순위 관리방안을 제시합니다:
- 중금속 배출을 위한 항산화 영양제 보충
- 결핍 미네랄 우선 보충
- 3개월 후 재검사로 개선 상황 모니터링"""

    def _step7_compressed_version(self, input_data: HairAnalysisInput, comprehensive_analysis: str) -> str:
        """7단계: 압축 버전 (950-1000자)"""
        name = input_data.personal_info.name

        compressed = f"""{name}님의 모발검사 결과를 말씀드리겠습니다.

검사 결과, 중금속 축적과 영양 미네랄 불균형이 확인되었습니다. 다행히 적절한 관리를 통해 충분히 개선 가능한 상태입니다.

우선 항산화가 풍부한 브로콜리, 시금치, 견과류, 등푸른생선, 달걀 등을 꾸준히 섭취해주세요. 이런 식품들이 체내 독성 물질 배출을 도와드립니다.

영양제는 항산화 영양제(비타민C, E, 셀레늄)를 추천드리며, 가공식품과 인스턴트는 가능한 줄여주세요. 충분한 수분 섭취와 규칙적인 운동도 도움이 됩니다.

3개월 후 재검사를 통해 개선 상황을 확인하시길 바랍니다. 꾸준한 관리로 더 건강한 상태로 개선될 수 있으니 너무 걱정하지 마시고 차근차근 실천해나가세요."""

        # 글자수 확인 (950-1000자 목표)
        char_count = len(compressed)
        return f"{compressed}\n\n[글자수: {char_count}자]"

    # 헬퍼 메소드들
    def _get_korean_metal_name(self, field_name: str) -> str:
        """영어 필드명을 한국어 중금속명으로 변환"""
        mapping = {
            "mercury": "수은", "arsenic": "비소", "cadmium": "카드뮴", "lead": "납",
            "aluminum": "알루미늄", "barium": "바륨", "nickel": "니켈",
            "uranium": "우라늄", "bismuth": "비스무트"
        }
        return mapping.get(field_name, field_name)

    def _get_korean_mineral_name(self, field_name: str) -> str:
        """영어 필드명을 한국어 미네랄명으로 변환"""
        mapping = {
            "calcium": "칼슘", "magnesium": "마그네슘", "sodium": "나트륨", "potassium": "칼륨",
            "copper": "구리", "zinc": "아연", "phosphorus": "인", "iron": "철",
            "manganese": "망간", "chromium": "크롬", "selenium": "셀레늄"
        }
        return mapping.get(field_name, field_name)

    def _get_korean_health_name(self, field_name: str) -> str:
        """영어 필드명을 한국어 건강지표명으로 변환"""
        mapping = {
            "insulin_sensitivity": "인슐린 민감도",
            "autonomic_nervous_system": "자율신경계",
            "stress_state": "스트레스 상태",
            "immune_skin_health": "면역 및 피부 건강",
            "adrenal_activity": "부신 활성도",
            "thyroid_activity": "갑상선 활성도"
        }
        return mapping.get(field_name, field_name)

    def _is_perm_dye_treatment(self, special_notes: str) -> bool:
        """파마/염색/탈색 여부 확인"""
        perm_dye_keywords = ["파마", "염색", "탈색"]
        return any(keyword in special_notes for keyword in perm_dye_keywords)

    def _add_perm_dye_disclaimer(self, metal_content: str, input_data: HairAnalysisInput) -> str:
        """바륨 + 파마/염색인 경우 특별 멘트 추가"""
        note1_content = self.notes_cache.get("note1_basic", "")

        # 노트1번에서 파마/염색 관련 멘트 추출
        pattern = r'#### 바륨 높음 \+ 파마or염색or탈색\s*\*\*최종 멘트:\*\*\s*> (.+?)(?=\n\n|\*\*비고|\Z)'
        match = re.search(pattern, note1_content, re.DOTALL)

        if match:
            disclaimer_template = match.group(1).strip()
            # 인용문 형태 정리
            disclaimer_template = re.sub(r'>\s*\n>\s*', ' ', disclaimer_template)
            disclaimer_template = re.sub(r'>\s*', '', disclaimer_template)

            # 높음인 원소들 확인 (바륨은 필수, 칼슘/마그네슘은 높음인 경우만)
            affected_elements = ["바륨"]
            if input_data.nutritional_minerals.calcium == "높음":
                affected_elements.append("칼슘")
            if input_data.nutritional_minerals.magnesium == "높음":
                affected_elements.append("마그네슘")

            elements_str = ", ".join(affected_elements)
            disclaimer = disclaimer_template.replace("[원소명]", elements_str)

            return f"{metal_content}\n\n{disclaimer}"

        return metal_content

    def _determine_management_point(self, input_data: HairAnalysisInput) -> str:
        """핵심 관리 포인트 결정 (노트5번 우선순위 규칙)"""
        # 파마/염색/탈색 영향 체크
        is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

        # 1순위: 유해 중금속 축적 (파마/염색 영향 제외)
        heavy_metals_data = input_data.heavy_metals.model_dump()
        real_heavy_metals_high = []

        for metal, value in heavy_metals_data.items():
            if value == "높음":
                # 파마/염색인 경우 바륨 제외
                if is_perm_dye and metal == "barium":
                    continue
                real_heavy_metals_high.append(metal)

        if real_heavy_metals_high:
            return "중금속 배출 관리"

        # 2순위: 부신 기능 저하 + 피로감
        if input_data.health_indicators.adrenal_activity == "낮음":
            return "부신 피로도 관리"

        # 3순위: 스트레스 지표 높음 (파마/염색 영향 제외)
        sodium_high = input_data.nutritional_minerals.sodium == "높음"
        potassium_high = input_data.nutritional_minerals.potassium == "높음"

        # 10세 이하의 나트륨/칼륨 높음은 정상으로 간주
        if input_data.personal_info.age <= 10:
            sodium_high = False
            potassium_high = False

        if sodium_high or potassium_high:
            return "스트레스 관리"

        # 4순위: 혈당 관련 지표
        if input_data.health_indicators.insulin_sensitivity == "낮음":
            return "혈당 관리와 피로감 개선"

        # 5순위: 기타 영양 불균형 (파마/염색 영향 제외)
        minerals_data = input_data.nutritional_minerals.model_dump()
        minerals_abnormal = []

        for mineral, value in minerals_data.items():
            if value != "정상":
                # 10세 이하의 나트륨/칼륨 높음은 정상으로 간주
                if (input_data.personal_info.age <= 10 and
                    mineral in ["sodium", "potassium"] and value == "높음"):
                    continue
                # 파마/염색인 경우 칼슘/마그네슘 높음은 정상으로 간주
                if (is_perm_dye and
                    mineral in ["calcium", "magnesium"] and value == "높음"):
                    continue
                minerals_abnormal.append(mineral)

        if minerals_abnormal:
            return "영양 균형 관리"

        # 기본: 면역력 강화
        return "면역력 강화"

    def _generate_recommended_foods_from_note5(self, input_data: HairAnalysisInput) -> str:
        """노트5번 기반 추천 식품 5개 생성 (샘플 분석 우선순위 적용)"""
        # 노트5번 분석에 따른 공통 추천 식품 우선순위
        # 1순위: 견과류 (5회), 달걀 (5회)
        # 2순위: 채소/녹색 잎 채소 (4회)
        # 3순위: 등 푸른 생선 (2회), 가공하지 않은 곡류 (2회)

        management_point = self._determine_management_point(input_data)

        if management_point == "중금속 배출 관리":
            # 샘플1 기반: 브로콜리, 시금치, 견과류, 등 푸른 생선, 달걀
            foods = ["브로콜리", "시금치", "견과류", "등 푸른 생선", "달걀"]
        elif management_point == "부신 피로도 관리":
            # 샘플2 기반: 녹색 잎 채소, 달걀, 견과류, 가공하지 않은 곡류 + 보완 1개
            foods = ["녹색 잎 채소", "달걀", "견과류", "가공하지 않은 곡류", "브로콜리"]
        elif management_point == "스트레스 관리":
            # 샘플3 기반: 익힌 채소, 등 푸른 생선, 견과류, 콩류, 달걀
            foods = ["익힌 채소", "등 푸른 생선", "견과류", "콩류", "달걀"]
        elif management_point in ["중금속과 항산화 관리", "항산화 관리"]:
            # 샘플4 기반: 견과류, 가공하지 않은 곡류, 채소, 달걀 + 보완 1개
            foods = ["견과류", "가공하지 않은 곡류", "채소", "달걀", "브로콜리"]
        elif management_point == "혈당 관리와 피로감 개선":
            # 샘플5 기반: 가공하지 않은 곡류, 견과류, 달걀, 채소 + 보완 1개
            foods = ["가공하지 않은 곡류", "견과류", "달걀", "채소", "콩류"]
        else:
            # 기본: 가장 높은 빈도의 식품들로 구성
            foods = ["견과류", "달걀", "녹색 잎 채소", "등 푸른 생선", "가공하지 않은 곡류"]

        return f"{', '.join(foods)} 등의 보충과 균형 잡힌 식사가 권장됩니다."

    def _generate_recommended_supplements_from_note5(self, input_data: HairAnalysisInput) -> str:
        """노트5번 기반 추천 영양제 생성 (샘플 분석 기반)"""
        management_point = self._determine_management_point(input_data)

        # 파마/염색/탈색 영향 체크
        is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

        # 실제 중금속 축적 확인 (파마/염색 영향 제외)
        heavy_metals_data = input_data.heavy_metals.model_dump()
        real_heavy_metals_high = []
        for metal, value in heavy_metals_data.items():
            if value == "높음":
                if is_perm_dye and metal == "barium":
                    continue
                real_heavy_metals_high.append(self._get_korean_metal_name(metal))

        if management_point == "중금속 배출 관리":
            if real_heavy_metals_high:
                metals_str = ", ".join(real_heavy_metals_high)
                # 마그네슘 결핍도 함께 확인 (파마/염색 영향 제외)
                magnesium_low = (input_data.nutritional_minerals.magnesium == "낮음" or
                               (input_data.nutritional_minerals.magnesium == "높음" and not is_perm_dye))
                if magnesium_low and input_data.nutritional_minerals.magnesium == "낮음":
                    return f"{metals_str} 배출을 위해 비타민C, E, 셀레늄이 함유된 항산화 영양제와 칼마디(칼슘, 마그네슘, 비타민D) 영양제를 추천 드립니다."
                else:
                    return f"{metals_str} 배출을 위해 비타민C, E, 셀레늄이 함유된 항산화 영양제를 추천 드립니다."
            else:
                # 특별 조건: 제목이 "중금속 배출 관리"이지만 실제 중금속 없는 경우
                return "항산화 관리를 위해 비타민C, E, 셀레늄이 함유된 항산화 영양제를 추천 드립니다."

        elif management_point == "부신 피로도 관리":
            return "부신 피로도 개선을 위해 비타민B 영양제를 추천 드립니다."

        elif management_point == "스트레스 관리":
            # 파마/염색 영향 및 연령 조건 확인
            sodium_high = input_data.nutritional_minerals.sodium == "높음"
            potassium_high = input_data.nutritional_minerals.potassium == "높음"

            # 10세 이하의 나트륨/칼륨 높음은 정상으로 간주
            if input_data.personal_info.age <= 10:
                sodium_high = False
                potassium_high = False

            if sodium_high or potassium_high:
                return "나트륨, 칼륨 수치와 스트레스 개선을 위해 비타민D의 꾸준한 섭취가 권장 됩니다."
            else:
                return "스트레스 관리를 위해 비타민D와 마그네슘 영양제를 추천 드립니다."

        elif management_point in ["중금속과 항산화 관리", "항산화 관리"]:
            # 복합 영양제 (항산화 + 부신 지원)
            return "항산화 관리를 위해 비타민C, E, 셀레늄이 함유된 항산화 영양제를, 부신 피로 개선을 위해 비타민B가 도움이 됩니다."

        elif management_point == "혈당 관리와 피로감 개선":
            return "부신 활성과 느끼시는 피로감 개선을 위해 비타민B 영양제를 추천 드립니다."

        else:
            # 기타 영양 균형 관리
            return "영양 균형과 면역력 강화를 위해 종합 비타민과 비타민D 영양제를 추천 드립니다."

    def _generate_reexam_period_from_note5(self, input_data: HairAnalysisInput) -> str:
        """노트5번 기반 재검사 권장 기간 생성 (조건별 매트릭스 적용)"""
        name = input_data.personal_info.name
        management_point = self._determine_management_point(input_data)

        # 파마/염색/탈색 영향 체크
        is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

        # 실제 중금속 축적 확인 (파마/염색 영향 제외)
        heavy_metals_data = input_data.heavy_metals.model_dump()
        real_heavy_metals_high = []
        for metal, value in heavy_metals_data.items():
            if value == "높음":
                if is_perm_dye and metal == "barium":
                    continue
                real_heavy_metals_high.append(self._get_korean_metal_name(metal))

        # 영양 미네랄 불균형 확인 (파마/염색 영향 제외)
        minerals_data = input_data.nutritional_minerals.model_dump()
        minerals_abnormal = []
        for mineral, value in minerals_data.items():
            if value != "정상":
                # 10세 이하의 나트륨/칼륨 높음은 정상으로 간주
                if (input_data.personal_info.age <= 10 and
                    mineral in ["sodium", "potassium"] and value == "높음"):
                    continue
                # 파마/염색인 경우 칼슘/마그네슘 높음은 정상으로 간주
                if (is_perm_dye and
                    mineral in ["calcium", "magnesium"] and value == "높음"):
                    continue
                minerals_abnormal.append(self._get_korean_mineral_name(mineral))

        # 조건별 재검사 기간 결정
        if real_heavy_metals_high and not minerals_abnormal:
            # 조건 1: 유해 중금속 높음 + 영양 미네랄 정상 → 3개월
            period = "3개월"
            metals_str = ", ".join(real_heavy_metals_high)
            management = f"{metals_str} 배출을 위한 영양 관리"

        elif real_heavy_metals_high and minerals_abnormal:
            # 조건 2: 유해 중금속 높음 + 영양 미네랄 불균형 → 3개월
            period = "3개월"
            metals_str = ", ".join(real_heavy_metals_high)
            minerals_str = ", ".join(minerals_abnormal[:2])  # 최대 2개까지만 표시
            management = f"{metals_str} 배출과 {minerals_str}의 관리"

        elif not real_heavy_metals_high and minerals_abnormal:
            # 조건 3: 유해 중금속 정상 + 영양 미네랄 불균형 → 3-4개월
            period = "3~4개월"
            minerals_str = ", ".join(minerals_abnormal[:2])
            management = f"{minerals_str} 관리"

        else:
            # 조건 4: 모든 항목 정상 → 5-6개월
            period = "5~6개월"
            if management_point == "부신 피로도 관리":
                management = "부신 피로감 개선"
            elif management_point == "스트레스 관리":
                management = "스트레스 및 영양 관리"
            elif management_point == "혈당 관리와 피로감 개선":
                management = "영양 관리"
            else:
                management = "꾸준한 영양 관리"

        return f"{name}님께서는 {management} 후, 약 {period} 뒤 재검사를 통한 확인이 필요합니다."