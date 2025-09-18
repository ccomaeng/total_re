import os
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path

from ..models.input_models import HairAnalysisInput, TestResultValue, HeavyMetalValue
from ..models.output_models import (
    PersonalInfoSection, ComprehensiveAnalysis, SummaryExplanation,
    StatisticsAnalysis, ComprehensiveSummary, NutritionistSummary,
    CompressedVersion, HairAnalysisOutput
)

try:
    from .secure_data_loader import SecureDataLoader
except ImportError:
    SecureDataLoader = None

class HairAnalysisService:
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
        self.notes_cache = {}
        self._load_note_files()

    def _load_note_files(self):
        """5개 핵심 노트 파일을 캐시에 로드 - 환경변수 우선, 로컬 파일 폴백"""
        if SecureDataLoader:
            # SecureDataLoader 사용 (환경변수/S3/로컬 우선순위)
            try:
                notes = SecureDataLoader.load_notes()
                self.notes_cache = {
                    "note1_basic": notes.get("note1", ""),
                    "note2_heavy_metals": notes.get("note2", ""),
                    "note3_minerals": notes.get("note3", ""),
                    "note4_health_indicators": notes.get("note4", ""),
                    "note5_summary": notes.get("note5", "")
                }
                return
            except Exception as e:
                print(f"SecureDataLoader failed: {e}, falling back to local files")

        # 로컬 파일 로드 (폴백)
        note_files = {
            "note1_basic": self.data_path / "note1_basic.md",
            "note2_heavy_metals": self.data_path / "note2_heavy_metals.md",
            "note3_minerals": self.data_path / "note3_minerals.md",
            "note4_health_indicators": self.data_path / "note4_health_indicators.md",
            "note5_summary": self.data_path / "note5_summary.md"
        }

        for key, file_path in note_files.items():
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.notes_cache[key] = f.read()

    def analyze(self, input_data: HairAnalysisInput) -> HairAnalysisOutput:
        """메인 분석 함수 - 7단계 순차 처리"""

        # 1단계: 개인정보 섹션 작성
        personal_info_section = self._step1_personal_info(input_data)

        # 2단계: 종합멘트 작성 (5개 노트 순차 참조)
        comprehensive_analysis = self._step2_comprehensive_analysis(input_data)

        # 3단계: 요약 설명 작성
        summary_explanation = self._step3_summary_explanation(input_data, comprehensive_analysis)

        # 4단계: 통계 분석
        statistics_analysis = self._step4_statistics_analysis(comprehensive_analysis)

        # 5단계: 종합멘트 요약
        comprehensive_summary = self._step5_comprehensive_summary(comprehensive_analysis)

        # 6단계: 영양전문가 요약
        nutritionist_summary = self._step6_nutritionist_summary(input_data, comprehensive_analysis)

        # 7단계: 압축 버전 (950-1000자)
        compressed_version = self._step7_compressed_version(input_data, comprehensive_analysis)

        return HairAnalysisOutput(
            personal_info_section=personal_info_section,
            comprehensive_analysis=comprehensive_analysis,
            summary_explanation=summary_explanation,
            statistics_analysis=statistics_analysis,
            comprehensive_summary=comprehensive_summary,
            nutritionist_summary=nutritionist_summary,
            compressed_version=compressed_version
        )

    def _step1_personal_info(self, input_data: HairAnalysisInput) -> PersonalInfoSection:
        """1단계: 개인정보 섹션 작성"""
        name = input_data.personal_info.name
        age = input_data.personal_info.age
        special_notes = input_data.personal_info.special_notes

        # 연령대 구분
        if age <= 10:
            age_group = "10세 이하"
        elif age <= 19:
            age_group = "11-19세"
        else:
            age_group = "20세 이상"

        # 유해 중금속 분류
        heavy_metals_normal = []
        heavy_metals_high = []

        heavy_metals_dict = {
            "수은": input_data.heavy_metals.mercury,
            "비소": input_data.heavy_metals.arsenic,
            "카드뮴": input_data.heavy_metals.cadmium,
            "납": input_data.heavy_metals.lead,
            "알루미늄": input_data.heavy_metals.aluminum,
            "바륨": input_data.heavy_metals.barium,
            "니켈": input_data.heavy_metals.nickel,
            "우라늄": input_data.heavy_metals.uranium,
            "비스무트": input_data.heavy_metals.bismuth
        }

        for metal, value in heavy_metals_dict.items():
            if value == HeavyMetalValue.HIGH:
                heavy_metals_high.append(metal)
            else:
                heavy_metals_normal.append(metal)

        # 영양 미네랄 분류
        minerals_normal = []
        minerals_high = []
        minerals_low = []

        minerals_dict = {
            "칼슘": input_data.nutritional_minerals.calcium,
            "마그네슘": input_data.nutritional_minerals.magnesium,
            "나트륨": input_data.nutritional_minerals.sodium,
            "칼륨": input_data.nutritional_minerals.potassium,
            "구리": input_data.nutritional_minerals.copper,
            "아연": input_data.nutritional_minerals.zinc,
            "인": input_data.nutritional_minerals.phosphorus,
            "철": input_data.nutritional_minerals.iron,
            "망간": input_data.nutritional_minerals.manganese,
            "크롬": input_data.nutritional_minerals.chromium,
            "셀레늄": input_data.nutritional_minerals.selenium
        }

        for mineral, value in minerals_dict.items():
            if value == TestResultValue.HIGH:
                minerals_high.append(mineral)
            elif value == TestResultValue.LOW:
                minerals_low.append(mineral)
            else:
                minerals_normal.append(mineral)

        # 건강 상태 지표 분류
        health_normal = []
        health_high = []
        health_low = []

        health_dict = {
            "인슐린 민감도": input_data.health_indicators.insulin_sensitivity,
            "자율신경계": input_data.health_indicators.autonomic_nervous_system,
            "스트레스 상태": input_data.health_indicators.stress_state,
            "면역 및 피부 건강": input_data.health_indicators.immune_skin_health,
            "부신 활성도": input_data.health_indicators.adrenal_activity,
            "갑상선 활성도": input_data.health_indicators.thyroid_activity
        }

        for indicator, value in health_dict.items():
            if value == TestResultValue.HIGH:
                health_high.append(indicator)
            elif value == TestResultValue.LOW:
                health_low.append(indicator)
            else:
                health_normal.append(indicator)

        return PersonalInfoSection(
            name=name,
            age=age,
            age_group=age_group,
            special_notes=special_notes,
            heavy_metals_normal=heavy_metals_normal,
            heavy_metals_high=heavy_metals_high,
            heavy_metals_normal_count=len(heavy_metals_normal),
            heavy_metals_high_count=len(heavy_metals_high),
            minerals_normal=minerals_normal,
            minerals_high=minerals_high,
            minerals_low=minerals_low,
            minerals_normal_count=len(minerals_normal),
            minerals_high_count=len(minerals_high),
            minerals_low_count=len(minerals_low),
            health_normal=health_normal,
            health_high=health_high,
            health_low=health_low,
            health_normal_count=len(health_normal),
            health_high_count=len(health_high),
            health_low_count=len(health_low)
        )

    def _step2_comprehensive_analysis(self, input_data: HairAnalysisInput) -> ComprehensiveAnalysis:
        """2단계: 종합멘트 작성 (5개 노트 순차 참조)"""

        # Step 2-1: 첫 번째 단락 (note1_basic.md에서 추출)
        first_paragraph = self._extract_first_paragraph(input_data)

        # Step 2-2: 중금속 분석 (note2_heavy_metals.md에서 추출)
        heavy_metals_analysis = self._extract_heavy_metals_analysis(input_data)

        # Step 2-3: 영양 미네랄 분석 (note3_minerals.md에서 추출)
        minerals_analysis = self._extract_minerals_analysis(input_data)

        # Step 2-4: 건강 상태 지표 분석 (note4_health_indicators.md에서 추출)
        health_indicators_analysis = self._extract_health_indicators_analysis(input_data)

        return ComprehensiveAnalysis(
            first_paragraph=first_paragraph,
            heavy_metals_analysis=heavy_metals_analysis,
            minerals_analysis=minerals_analysis,
            health_indicators_analysis=health_indicators_analysis
        )

    def _extract_first_paragraph(self, input_data: HairAnalysisInput) -> str:
        """note1_basic.md에서 첫 번째 단락 추출"""
        note1_content = self.notes_cache.get("note1_basic", "")
        name = input_data.personal_info.name

        # 완전 정상인 경우 체크
        heavy_metals_all_normal = all(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.NORMAL
            for field in input_data.heavy_metals.__fields__
        )
        minerals_all_normal = all(
            getattr(input_data.nutritional_minerals, field) == TestResultValue.NORMAL
            for field in input_data.nutritional_minerals.__fields__
        )
        health_all_normal = all(
            getattr(input_data.health_indicators, field) == TestResultValue.NORMAL
            for field in input_data.health_indicators.__fields__
        )

        if heavy_metals_all_normal and minerals_all_normal and health_all_normal:
            # 완전 정상인 경우 멘트 추출 - 실제 노트의 구조에 맞춘 패턴
            pattern = r'### 모발검사결과 \(완전 정상인 경우\).*?\*\*최종 멘트:\*\*\n>(.*?)(?=\n\*\*|---|\Z)'
            match = re.search(pattern, note1_content, re.DOTALL)
            if match:
                template = match.group(1).strip()
                # 줄바꿈 제거하고 연속된 텍스트로 만들기
                template = re.sub(r'>\s*\n>\s*', ' ', template)
                template = re.sub(r'>\s*', '', template)
                # [이름] 치환
                result = template.replace("[이름]", name)
                return result

        # 일반적인 경우: 테이블 기반 조건별 멘트 생성
        return self._generate_first_paragraph_from_table(input_data, note1_content)

    def _generate_first_paragraph_from_table(self, input_data: HairAnalysisInput, note_content: str) -> str:
        """테이블 기반 조건별 첫 번째 단락 생성"""
        name = input_data.personal_info.name

        # 1. 유해 중금속 멘트 결정
        heavy_metals_high = []
        for field_name in input_data.heavy_metals.__fields__:
            value = getattr(input_data.heavy_metals, field_name)
            if value == HeavyMetalValue.HIGH:
                korean_name = self._get_korean_metal_name(field_name)
                heavy_metals_high.append(korean_name)

        if heavy_metals_high:
            metals_str = ", ".join(heavy_metals_high)
            heavy_metal_text = f"유해 중금속은 {metals_str}이 축적되었습니다."
        else:
            heavy_metal_text = "유해 중금속은 모두 정상 수치 입니다."

        # 2. 영양 미네랄 멘트 결정
        minerals_abnormal = []
        for field_name in input_data.nutritional_minerals.__fields__:
            value = getattr(input_data.nutritional_minerals, field_name)
            if value != TestResultValue.NORMAL:
                korean_name = self._get_korean_mineral_name(field_name)
                minerals_abnormal.append(korean_name)

        if minerals_abnormal:
            minerals_str = ", ".join(minerals_abnormal)
            minerals_text = f"영양 미네랄은 {minerals_str}이 불균형 상태입니다."
        else:
            minerals_text = "영양 미네랄은 모두 정상 수치입니다."

        # 3. 건강 상태 지표 멘트 결정
        health_abnormal_count = sum(
            1 for field_name in input_data.health_indicators.__fields__
            if getattr(input_data.health_indicators, field_name) != TestResultValue.NORMAL
        )

        if health_abnormal_count == 0:
            health_text = "건강 상태 지표는 모두 균형을 이루고 있습니다."
        elif health_abnormal_count <= 3:
            health_text = "건강 상태 지표는 일부가 불안정 상태입니다."
        else:
            health_text = "건강 상태 지표는 몇가지 불안정 상태입니다."

        # 4. 최종 첫 번째 단락 조합 (노트의 테이블 규칙 따름)
        result = f"{name}님의 모발검사결과, {heavy_metal_text} {minerals_text} {health_text}"

        return result

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

    def _extract_heavy_metals_analysis(self, input_data: HairAnalysisInput) -> str:
        """note2_heavy_metals.md에서 중금속 분석 추출"""
        note2_content = self.notes_cache.get("note2_heavy_metals", "")
        name = input_data.personal_info.name
        age = input_data.personal_info.age

        analysis_parts = []

        # 높음으로 표시된 중금속만 처리
        heavy_metals_data = {
            "mercury": (input_data.heavy_metals.mercury, "수은"),
            "arsenic": (input_data.heavy_metals.arsenic, "비소"),
            "cadmium": (input_data.heavy_metals.cadmium, "카드뮴"),
            "lead": (input_data.heavy_metals.lead, "납"),
            "aluminum": (input_data.heavy_metals.aluminum, "알루미늄"),
            "barium": (input_data.heavy_metals.barium, "바륨"),
            "nickel": (input_data.heavy_metals.nickel, "니켈"),
            "uranium": (input_data.heavy_metals.uranium, "우라늄"),
            "bismuth": (input_data.heavy_metals.bismuth, "비스무트")
        }

        for field_name, (value, korean_name) in heavy_metals_data.items():
            if value == HeavyMetalValue.HIGH:
                metal_analysis = self._extract_metal_specific_content(
                    note2_content, korean_name, age, name
                )
                if metal_analysis:
                    analysis_parts.append(metal_analysis)

        return "\n\n".join(analysis_parts)

    def _extract_metal_specific_content(self, note_content: str, metal_name: str, age: int, name: str) -> str:
        """특정 중금속에 대한 연령별 멘트 추출"""
        # 연령대 결정
        if age <= 19:
            age_section = "19세 이하"
        else:
            age_section = "20세 이상"

        # 중금속별 섹션 찾기 (개선된 패턴)
        metal_pattern = f"## {metal_name}.*?(?=\n## |\n---|\Z)"
        metal_match = re.search(metal_pattern, note_content, re.DOTALL)

        if not metal_match:
            return ""

        metal_section = metal_match.group(0)

        # 연령별 섹션 찾기
        age_pattern = f"### {age_section}(.*?)(?=### |---|\Z)"
        age_match = re.search(age_pattern, metal_section, re.DOTALL)

        if age_match:
            content = age_match.group(1).strip()
            # [이름] 치환
            content = content.replace("[이름]", name)
            return content

        return ""

    def _extract_minerals_analysis(self, input_data: HairAnalysisInput) -> str:
        """note3_minerals.md에서 영양 미네랄 분석 추출"""
        note3_content = self.notes_cache.get("note3_minerals", "")
        if not note3_content:
            return ""

        name = input_data.personal_info.name
        age = input_data.personal_info.age
        analysis_parts = []

        # 연령대 결정
        age_group = "20세 이상" if age >= 20 else "19세 이하"

        # 복합조건 먼저 확인
        complex_conditions = [
            ("칼슘과 마그네슘 높음",
             input_data.nutritional_minerals.calcium == TestResultValue.HIGH and
             input_data.nutritional_minerals.magnesium == TestResultValue.HIGH),
            ("나트륨과 칼륨 높음",
             input_data.nutritional_minerals.sodium == TestResultValue.HIGH and
             input_data.nutritional_minerals.potassium == TestResultValue.HIGH),
            ("마그네슘 낮음과 칼슘 높음",
             input_data.nutritional_minerals.magnesium == TestResultValue.LOW and
             input_data.nutritional_minerals.calcium == TestResultValue.HIGH)
        ]

        used_minerals = set()

        # 복합조건 처리
        for condition_name, condition_met in complex_conditions:
            if condition_met:
                complex_content = self._extract_mineral_complex_content(note3_content, condition_name, age_group, name)
                if complex_content:
                    analysis_parts.append(complex_content)
                    # 복합조건에 포함된 미네랄들을 사용됨으로 표시
                    if "칼슘" in condition_name:
                        used_minerals.add("calcium")
                    if "마그네슘" in condition_name:
                        used_minerals.add("magnesium")
                    if "나트륨" in condition_name:
                        used_minerals.add("sodium")
                    if "칼륨" in condition_name:
                        used_minerals.add("potassium")

        # 개별 미네랄 조건 처리 (복합조건에서 사용되지 않은 것만)
        minerals_data = {
            "calcium": (input_data.nutritional_minerals.calcium, "칼슘"),
            "magnesium": (input_data.nutritional_minerals.magnesium, "마그네슘"),
            "sodium": (input_data.nutritional_minerals.sodium, "나트륨"),
            "potassium": (input_data.nutritional_minerals.potassium, "칼륨"),
            "copper": (input_data.nutritional_minerals.copper, "구리"),
            "zinc": (input_data.nutritional_minerals.zinc, "아연"),
            "phosphorus": (input_data.nutritional_minerals.phosphorus, "인"),
            "iron": (input_data.nutritional_minerals.iron, "철"),
            "manganese": (input_data.nutritional_minerals.manganese, "망간"),
            "chromium": (input_data.nutritional_minerals.chromium, "크롬"),
            "selenium": (input_data.nutritional_minerals.selenium, "셀레늄")
        }

        for field_name, (value, korean_name) in minerals_data.items():
            if field_name not in used_minerals and value != TestResultValue.NORMAL:
                status = "높음" if value == TestResultValue.HIGH else "낮음"
                mineral_content = self._extract_individual_mineral_content(note3_content, korean_name, status, age_group, name)
                if mineral_content:
                    analysis_parts.append(mineral_content)

        return "\n\n".join(analysis_parts)

    def _extract_mineral_complex_content(self, note_content: str, condition: str, age_group: str, name: str) -> str:
        """복합조건 미네랄 멘트 추출"""
        # Note 3의 복합조건은 연령대가 포함된 형태
        complex_condition = f"{condition} + {age_group} (복합조건)"

        # 패턴에서 특수 문자 이스케이프
        escaped_condition = re.escape(complex_condition)
        pattern = f"### {escaped_condition}.*?\*\*최종 멘트:\*\*(.*?)(?=\*\*⚠️|### |## |\Z)"

        section_match = re.search(pattern, note_content, re.DOTALL)

        if section_match:
            content = section_match.group(1).strip()
            # > 기호로 시작하는 경우 제거
            if content.startswith('>'):
                content = content[1:].strip()
            # [이름] 치환
            content = content.replace("[이름]", name)
            return content

        return ""

    def _extract_individual_mineral_content(self, note_content: str, mineral_name: str, status: str, age_group: str, name: str) -> str:
        """개별 미네랄 멘트 추출"""
        # Note 3의 개별 미네랄은 "미네랄명 상태 + 연령대" 형태
        condition = f"{mineral_name} {status} + {age_group}"

        # 패턴에서 특수 문자 이스케이프
        escaped_condition = re.escape(condition)
        pattern = f"### {escaped_condition}.*?\*\*최종 멘트:\*\*(.*?)(?=### |## |\Z)"

        match = re.search(pattern, note_content, re.DOTALL)

        if match:
            content = match.group(1).strip()
            # > 기호로 시작하는 경우 제거
            if content.startswith('>'):
                content = content[1:].strip()
            # [이름] 치환
            content = content.replace("[이름]", name)
            return content

        return ""

    def _extract_health_indicators_analysis(self, input_data: HairAnalysisInput) -> str:
        """note4_health_indicators.md에서 건강 상태 지표 분석 추출"""
        note4_content = self.notes_cache.get("note4_health_indicators", "")
        if not note4_content:
            return ""

        name = input_data.personal_info.name
        age = input_data.personal_info.age
        analysis_parts = []
        skip_thyroid = False

        # 연령대 결정
        if age <= 10:
            age_group = "10세 이하"
        elif age <= 19:
            age_group = "11-19세" if 11 <= age <= 19 else "19세 이하"
        else:
            age_group = "20세 이상"

        # 복합조건 우선 처리 (부신+갑상선)
        adrenal_high = input_data.health_indicators.adrenal_activity == TestResultValue.HIGH
        thyroid_low = input_data.health_indicators.thyroid_activity == TestResultValue.LOW
        adrenal_low = input_data.health_indicators.adrenal_activity == TestResultValue.LOW
        thyroid_high = input_data.health_indicators.thyroid_activity == TestResultValue.HIGH
        mercury_high = input_data.heavy_metals.mercury == HeavyMetalValue.HIGH

        # 부신 높음 + 갑상선 낮음 조건들
        if adrenal_high and thyroid_low:
            complex_content = self._extract_adrenal_thyroid_complex(note4_content, age_group, mercury_high, name)
            if complex_content:
                analysis_parts.append(complex_content)
                skip_thyroid = True

        # 부신 낮음 + 갑상선 높음 조건들
        elif adrenal_low and thyroid_high:
            complex_content = self._extract_adrenal_low_thyroid_high_complex(note4_content, age_group, name)
            if complex_content:
                analysis_parts.append(complex_content)
                skip_thyroid = True

        # 개별 건강지표 처리
        health_indicators = {
            "insulin_sensitivity": (input_data.health_indicators.insulin_sensitivity, "인슐린 민감도"),
            "autonomic_nervous_system": (input_data.health_indicators.autonomic_nervous_system, "자율신경계"),
            "stress_state": (input_data.health_indicators.stress_state, "스트레스 상태"),
            "immune_skin_health": (input_data.health_indicators.immune_skin_health, "면역 및 피부 건강"),
            "adrenal_activity": (input_data.health_indicators.adrenal_activity, "부신 활성도"),
            "thyroid_activity": (input_data.health_indicators.thyroid_activity, "갑상선 활성도")
        }

        for field_name, (value, korean_name) in health_indicators.items():
            # 갑상선 활성도는 복합조건에서 처리된 경우 생략
            if field_name == "thyroid_activity" and skip_thyroid:
                continue

            # 부신 활성도는 복합조건에서 처리된 경우 생략
            if field_name == "adrenal_activity" and ((adrenal_high and thyroid_low) or (adrenal_low and thyroid_high)):
                continue

            if value != TestResultValue.NORMAL:
                status = "높음" if value == TestResultValue.HIGH else "낮음"
                health_content = self._extract_individual_health_content(note4_content, korean_name, status, age_group, mercury_high, name)
                if health_content:
                    analysis_parts.append(health_content)

        # 모든 건강 지표가 정상인 경우 기본 멘트 제공
        if not analysis_parts:
            analysis_parts.append(f"{name}님의 건강 상태 지표들은 전반적으로 균형을 이루고 있어 양호한 상태입니다. 현재의 건강한 생활습관을 유지하시면서 정기적인 검사를 통해 지속적으로 관리해 주시기 바랍니다.")

        return "\n\n".join(analysis_parts)

    def _extract_adrenal_thyroid_complex(self, note_content: str, age_group: str, mercury_high: bool, name: str) -> str:
        """부신 높음 + 갑상선 낮음 복합조건 멘트 추출"""
        # 우선순위: 수은 높음 조건 > 연령별 조건
        if mercury_high:
            if age_group == "20세 이상":
                pattern = r"### 부신 활성도 - 높음 \(20세 이상 \+ 수은 높음\).*?\*\*최종 멘트\*\*:(.*?)(?=### |$)"
            else:
                pattern = r"### 부신 활성도 - 높음 \(19세 이하 \+ 수은 높음\).*?\*\*최종 멘트\*\*:(.*?)(?=### |$)"
        else:
            if age_group == "20세 이상":
                pattern = r"### 부신 활성도 - 높음 \(20세 이상 \+ 갑상선 활성도 낮음\).*?\*\*최종 멘트\*\*:(.*?)(?=\*\*특이사항|### |$)"
            elif age_group == "10세 이하":
                pattern = r"### 부신 활성도 - 높음 \(10세 이하 \+ 갑상선 활성도 낮음\).*?\*\*최종 멘트\*\*:(.*?)(?=\*\*특이사항|### |$)"
            else:  # 11-19세
                pattern = r"### 부신 활성도 - 높음 \(11-19세 \+ 갑상선 활성도 낮음\).*?\*\*최종 멘트\*\*:(.*?)(?=\*\*특이사항|### |$)"

        match = re.search(pattern, note_content, re.DOTALL)
        if match:
            content = match.group(1).strip()
            content = content.replace("[이름]", name)
            return content
        return ""

    def _extract_adrenal_low_thyroid_high_complex(self, note_content: str, age_group: str, name: str) -> str:
        """부신 낮음 + 갑상선 높음 복합조건 멘트 추출"""
        if age_group == "20세 이상":
            pattern = r"### 부신 활성도 - 낮음 \(20세 이상 \+ 갑상선 활성도 높음\).*?\*\*최종 멘트\*\*:(.*?)(?=\*\*특이사항|### |$)"
        else:  # 19세 이하
            pattern = r"### 부신 활성도 - 낮음 \(19세 이하 \+ 갑상선 활성도 높음\).*?\*\*최종 멘트\*\*:(.*?)(?=\*\*특이사항|### |$)"

        match = re.search(pattern, note_content, re.DOTALL)
        if match:
            content = match.group(1).strip()
            content = content.replace("[이름]", name)
            return content
        return ""

    def _extract_individual_health_content(self, note_content: str, indicator_name: str, status: str, age_group: str, mercury_high: bool, name: str) -> str:
        """개별 건강지표 멘트 추출"""

        # 건강지표별 섹션 찾기 - 정확한 섹션 헤더만 매칭 (라인 시작부터)
        indicator_pattern = f"^## .{{1,3}} {re.escape(indicator_name)}$.*?(?=\n## |\Z)"
        indicator_match = re.search(indicator_pattern, note_content, re.DOTALL | re.MULTILINE)

        if not indicator_match:
            return ""

        indicator_section = indicator_match.group(0)

        # 상태별 + 연령별 멘트 찾기
        if indicator_name == "부신 활성도" and status == "높음" and not mercury_high:
            # 일반 부신 높음 조건
            pattern = r"### 부신 활성도 - 높음 \(일반\).*?\*\*최종 멘트\*\*:\s*(.*?)(?=\n### |\n---|\Z)"
        elif indicator_name == "부신 활성도" and status == "낮음":
            if age_group == "20세 이상":
                pattern = r"### 부신 활성도 - 낮음 \(20세 이상\).*?\*\*최종 멘트\*\*:\s*(.*?)(?=\n### |\n---|\Z)"
            else:
                pattern = r"### 부신 활성도 - 낮음 \(19세 이하\).*?\*\*최종 멘트\*\*:\s*(.*?)(?=\n### |\n---|\Z)"
        else:
            # 일반적인 패턴 - 먼저 연령별 시도, 실패하면 전연령 패턴 시도
            if age_group in ["19세 이하", "20세 이상"]:
                # 연령별 패턴 먼저 시도
                pattern = f"### {re.escape(indicator_name)} - {status} \\({re.escape(age_group)}\\).*?\\*\\*최종 멘트\\*\\*:\\s*(.*?)(?=\\n### |\\n---|\Z)"
                match = re.search(pattern, indicator_section, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    content = content.replace("[이름]", name)
                    return content

                # 연령별 패턴이 없으면 전연령 패턴 시도
                pattern = f"### {re.escape(indicator_name)} - {status} \\(전 연령\\).*?\\*\\*최종 멘트\\*\\*:\\s*(.*?)(?=\\n### |\\n---|\Z)"
                match = re.search(pattern, indicator_section, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    content = content.replace("[이름]", name)
                    return content

                # 마지막으로 조건 없는 패턴 시도
                pattern = f"### {re.escape(indicator_name)} - {status}.*?\\*\\*최종 멘트\\*\\*:\\s*(.*?)(?=\\n### |\\n---|\Z)"
            else:
                pattern = f"### {re.escape(indicator_name)} - {status}.*?\\*\\*최종 멘트\\*\\*:\\s*(.*?)(?=\\n### |\\n---|\Z)"

        match = re.search(pattern, indicator_section, re.DOTALL)
        if match:
            content = match.group(1).strip()
            content = content.replace("[이름]", name)
            return content

        return ""

    def _step3_summary_explanation(self, input_data: HairAnalysisInput, comprehensive_analysis: ComprehensiveAnalysis) -> SummaryExplanation:
        """3단계: 요약 설명 작성 (Note 5 규칙 기반)"""
        note5_content = self.notes_cache.get("note5_summary", "")
        name = input_data.personal_info.name

        # 1. 핵심 관리 포인트 결정 (Note 5 우선순위 규칙)
        title = self._determine_management_focus_note5(input_data)

        # 2. 추천 식품 5개 선정 (종합멘트에서 언급된 식품 우선)
        recommended_foods = self._select_recommended_foods_note5(input_data, comprehensive_analysis)

        # 3. 추천 영양제 선정 (종합멘트 기반)
        recommended_supplements = self._select_recommended_supplements_note5(input_data, comprehensive_analysis, title)

        # 4. 재검사 기간 결정 (Note 5 조건별 매트릭스)
        recheck_period = self._determine_recheck_period_note5(input_data, name)

        return SummaryExplanation(
            title=f"{name}님께서는 전체적으로 {title}가 요구됩니다.",
            recommended_foods=recommended_foods,
            recommended_supplements=recommended_supplements,
            recheck_period=recheck_period
        )

    def _determine_management_focus_note5(self, input_data: HairAnalysisInput) -> str:
        """Note 5 우선순위 규칙에 따른 핵심 관리 포인트 결정"""
        # 1순위: 유해 중금속 축적 (파마/염색 바륨 제외)
        has_high_metals = False
        for field in input_data.heavy_metals.__fields__:
            value = getattr(input_data.heavy_metals, field)
            if value == HeavyMetalValue.HIGH:
                # 바륨은 파마/염색 영향으로 제외 가능하지만 일단 포함
                has_high_metals = True
                break

        if has_high_metals:
            # 복합 문제가 있는지 확인
            has_other_issues = (
                input_data.health_indicators.adrenal_activity == TestResultValue.LOW or
                any(getattr(input_data.nutritional_minerals, field) != TestResultValue.NORMAL
                    for field in input_data.nutritional_minerals.__fields__)
            )
            if has_other_issues:
                return "중금속과 항산화 관리"  # 복합 문제인 경우
            return "중금속 배출 관리"

        # 2순위: 부신 기능 저하 + 피로감
        if input_data.health_indicators.adrenal_activity == TestResultValue.LOW:
            return "부신 피로도 관리"

        # 3순위: 스트레스 지표 높음
        if input_data.health_indicators.stress_state == TestResultValue.HIGH:
            return "스트레스 관리"

        # 4순위: 혈당 관련 지표
        if input_data.health_indicators.insulin_sensitivity != TestResultValue.NORMAL:
            return "혈당 관리와 피로감 개선"

        # 5순위: 기타 영양 불균형
        return "영양 균형 관리"

    def _select_recommended_foods_note5(self, input_data: HairAnalysisInput, comprehensive_analysis: ComprehensiveAnalysis) -> List[str]:
        """Note 5 규칙에 따른 추천 식품 5개 선정 (종합멘트에서 언급된 식품 우선)"""
        # 1. 종합멘트에서 언급된 식품들을 추출
        mentioned_foods = self._extract_mentioned_foods_advanced(comprehensive_analysis)

        # 2. 기본 추천 식품 (Note 5 샘플 분석 기반 우선순위)
        priority_foods = ["견과류", "달걀", "녹색 잎 채소", "등 푸른 생선", "가공하지 않은 곡류"]

        # 3. 건강 상태별 보완 식품
        supplement_foods = {
            "중금속": ["브로콜리", "마늘", "양파", "시금치", "해조류"],
            "부신피로": ["아보카도", "바나나", "고구마", "현미"],
            "스트레스": ["콩류", "두부", "아몬드", "연어"],
            "혈당": ["귀리", "퀴노아", "렌틸콩", "블루베리"],
            "면역": ["마늘", "생강", "버섯류", "베리류"]
        }

        # 4. 종합멘트 언급 식품을 우선하여 선정
        recommended = []

        # 종합멘트에서 언급된 식품 우선 추가
        for food in mentioned_foods:
            if len(recommended) < 5 and food not in recommended:
                recommended.append(food)

        # 우선순위 식품으로 부족분 보완
        for food in priority_foods:
            if len(recommended) < 5 and food not in recommended:
                recommended.append(food)

        # 여전히 부족하면 건강 상태별 식품으로 보완
        if len(recommended) < 5:
            # 핵심 관리 포인트에 따른 보완 식품 선택
            title = self._determine_management_focus_note5(input_data)
            if "중금속" in title:
                supplement_list = supplement_foods["중금속"]
            elif "부신" in title:
                supplement_list = supplement_foods["부신피로"]
            elif "스트레스" in title:
                supplement_list = supplement_foods["스트레스"]
            elif "혈당" in title:
                supplement_list = supplement_foods["혈당"]
            else:
                supplement_list = supplement_foods["면역"]

            for food in supplement_list:
                if len(recommended) < 5 and food not in recommended:
                    recommended.append(food)

        return recommended[:5]

    def _extract_mentioned_foods_advanced(self, comprehensive_analysis: ComprehensiveAnalysis) -> List[str]:
        """종합멘트에서 언급된 식품들을 고급 패턴으로 추출"""
        # 전체 종합멘트 텍스트 결합
        full_text = " ".join([
            comprehensive_analysis.first_paragraph,
            comprehensive_analysis.heavy_metals_analysis,
            comprehensive_analysis.minerals_analysis,
            comprehensive_analysis.health_indicators_analysis
        ])

        foods = []
        # Note 5 샘플 분석 기반 식품 키워드 (우선순위 순)
        food_patterns = [
            # 구체적 식품명
            "브로콜리", "시금치", "견과류", "등 푸른 생선", "달걀",
            "녹색 잎 채소", "가공하지 않은 곡류", "콩류", "두부", "채소",
            "익힌 채소", "바나나", "아보카도", "고구마", "현미",
            "유제품", "해조류", "멸치", "마늘", "양파", "생강",
            # 일반적 카테고리
            "붉은 고기", "육류", "생선", "곡류", "과일", "버섯류"
        ]

        # 언급 순서대로 추출 (중복 제거)
        for pattern in food_patterns:
            if pattern in full_text and pattern not in foods:
                foods.append(pattern)

        return foods

    def _select_recommended_supplements_note5(self, input_data: HairAnalysisInput, comprehensive_analysis: ComprehensiveAnalysis, title: str) -> str:
        """Note 5 규칙에 따른 추천 영양제 선정 (종합멘트에서 언급된 영양제 우선)"""
        name = input_data.personal_info.name

        # 1. 종합멘트에서 언급된 영양제 추출
        mentioned_supplements = self._extract_mentioned_supplements(comprehensive_analysis)

        if mentioned_supplements:
            return mentioned_supplements

        # 2. 종합멘트에 영양제 언급이 없는 경우 - 제목 기반 영양제 결정
        if "중금속 배출 관리" in title:
            # 특별 조건: 중금속 배출 관리 + 영양제 언급 없음 → 항산화 영양제
            return f"{self._get_primary_metal_name(input_data)} 배출을 위해 비타민C, E, 셀레늄이 함유된 항산화 영양제를 추천 드립니다."
        elif "중금속과 항산화 관리" in title:
            return f"{self._get_primary_metal_name(input_data)} 관리를 위해 비타민C, E, 셀레늄이 함유된 항산화 영양제와 부신 피로 개선을 위해 비타민B군이 도움이 됩니다."
        elif "부신 피로도 관리" in title:
            return "부신 피로도 개선을 위해 비타민B 영양제를 추천 드립니다."
        elif "스트레스 관리" in title:
            return "나트륨, 칼륨 수치와 스트레스 개선을 위해 비타민D의 꾸준한 섭취가 권장 됩니다."
        elif "혈당 관리와 피로감 개선" in title:
            return "부신 활성과 느끼시는 피로감 개선을 위해 비타민B 영양제를 추천 드립니다."
        else:
            return "영양 균형 관리를 위해 비타민B군 영양제를 추천 드립니다."

    def _extract_mentioned_supplements(self, comprehensive_analysis: ComprehensiveAnalysis) -> str:
        """종합멘트에서 언급된 영양제 추출"""
        full_text = " ".join([
            comprehensive_analysis.heavy_metals_analysis,
            comprehensive_analysis.minerals_analysis,
            comprehensive_analysis.health_indicators_analysis
        ])

        # 영양제 관련 키워드 패턴
        supplement_patterns = [
            ("비타민C.*?비타민E.*?셀레늄", "비타민C, E, 셀레늄이 함유된 항산화 영양제"),
            ("항산화.*?영양제", "항산화 영양제"),
            ("비타민B군.*?보충", "비타민B군"),
            ("비타민B.*?영양제", "비타민B 영양제"),
            ("비타민D.*?보충", "비타민D"),
            ("칼슘.*?마그네슘.*?영양제", "칼마디(칼슘, 마그네슘, 비타민D) 영양제")
        ]

        for pattern, supplement_name in supplement_patterns:
            if re.search(pattern, full_text, re.IGNORECASE):
                return supplement_name

        return ""

    def _get_primary_metal_name(self, input_data: HairAnalysisInput) -> str:
        """주요 중금속명 추출"""
        metals_kr = {
            "mercury": "수은", "lead": "납", "cadmium": "카드뮴",
            "arsenic": "비소", "nickel": "니켈", "aluminum": "알루미늄",
            "barium": "바륨", "uranium": "우라늄", "bismuth": "비스무트"
        }

        for field, korean_name in metals_kr.items():
            if getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH:
                return korean_name

        return "중금속"

    def _determine_recheck_period_note5(self, input_data: HairAnalysisInput, name: str) -> str:
        """Note 5 조건별 매트릭스에 따른 재검사 기간 결정"""
        # 조건 1: 유해 중금속 높음 + 영양 미네랄 정상 → 3개월
        has_high_metals = any(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH
            for field in input_data.heavy_metals.__fields__
        )

        has_mineral_imbalance = any(
            getattr(input_data.nutritional_minerals, field) != TestResultValue.NORMAL
            for field in input_data.nutritional_minerals.__fields__
        )

        if has_high_metals:
            primary_metal = self._get_primary_metal_name(input_data)

            if not has_mineral_imbalance:
                # 조건 1: 중금속 높음 + 영양 미네랄 정상
                return f"3. {name}님께서는 {primary_metal} 배출을 위한 영양 관리 후, 약 3개월 뒤 재검사를 통한 확인이 필요합니다."
            else:
                # 조건 2: 중금속 높음 + 영양 미네랄 불균형
                mineral_issue = self._get_primary_mineral_issue(input_data)
                return f"3. {name}님께서는 {primary_metal} 배출과 {mineral_issue}의 관리 후, 약 3개월 뒤 재검사를 통한 확인이 필요합니다."

        elif has_mineral_imbalance:
            # 조건 3: 중금속 정상 + 영양 미네랄 불균형
            mineral_issue = self._get_primary_mineral_issue(input_data)
            return f"3. {name}님께서는 {mineral_issue} 관리 후, 약 3~4개월 뒤 재검사를 통한 확인이 필요합니다."

        else:
            # 조건 4: 모든 항목 정상
            return f"3. {name}님께서는 꾸준한 영양 관리 후, 약 5~6개월 뒤 재검사를 통한 확인이 필요합니다."

    def _get_primary_mineral_issue(self, input_data: HairAnalysisInput) -> str:
        """주요 미네랄 문제 추출"""
        minerals_kr = {
            "calcium": "칼슘", "magnesium": "마그네슘", "sodium": "나트륨", "potassium": "칼륨",
            "copper": "구리", "zinc": "아연", "phosphorus": "인", "iron": "철",
            "manganese": "망간", "chromium": "크롬", "selenium": "셀레늄"
        }

        abnormal_minerals = []
        for field, korean_name in minerals_kr.items():
            value = getattr(input_data.nutritional_minerals, field)
            if value != TestResultValue.NORMAL:
                abnormal_minerals.append(korean_name)

        if abnormal_minerals:
            if len(abnormal_minerals) == 1:
                return abnormal_minerals[0]
            else:
                return ", ".join(abnormal_minerals[:2])  # 최대 2개까지만

        return "영양 미네랄"

    def _step4_statistics_analysis(self, comprehensive_analysis: ComprehensiveAnalysis) -> StatisticsAnalysis:
        """4단계: 통계 분석"""
        # 전체 텍스트 결합
        full_text = "\n\n".join([
            comprehensive_analysis.first_paragraph,
            comprehensive_analysis.heavy_metals_analysis,
            comprehensive_analysis.minerals_analysis,
            comprehensive_analysis.health_indicators_analysis
        ])

        # 통계 계산
        total_characters = len(full_text)
        total_words = len(full_text.split())
        paragraphs = full_text.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])
        average_paragraph_length = total_characters // paragraph_count if paragraph_count > 0 else 0

        # 각 섹션 비율 계산
        first_para_len = len(comprehensive_analysis.first_paragraph)
        heavy_metals_len = len(comprehensive_analysis.heavy_metals_analysis)
        minerals_len = len(comprehensive_analysis.minerals_analysis)
        health_len = len(comprehensive_analysis.health_indicators_analysis)

        first_paragraph_ratio = (first_para_len / total_characters * 100) if total_characters > 0 else 0
        heavy_metals_ratio = (heavy_metals_len / total_characters * 100) if total_characters > 0 else 0
        minerals_ratio = (minerals_len / total_characters * 100) if total_characters > 0 else 0
        health_indicators_ratio = (health_len / total_characters * 100) if total_characters > 0 else 0

        return StatisticsAnalysis(
            total_characters=total_characters,
            total_words=total_words,
            paragraph_count=paragraph_count,
            average_paragraph_length=average_paragraph_length,
            first_paragraph_ratio=round(first_paragraph_ratio, 1),
            heavy_metals_ratio=round(heavy_metals_ratio, 1),
            minerals_ratio=round(minerals_ratio, 1),
            health_indicators_ratio=round(health_indicators_ratio, 1)
        )

    def _step5_comprehensive_summary(self, comprehensive_analysis: ComprehensiveAnalysis) -> ComprehensiveSummary:
        """5단계: 종합멘트 요약"""
        # 간단한 키워드 분석으로 주요 문제점 추출
        main_problems = self._extract_main_problems(comprehensive_analysis)
        key_management_directions = self._extract_management_directions(comprehensive_analysis)
        precautions = self._extract_precautions(comprehensive_analysis)
        expected_effects = "관리 시 영양 균형 개선과 건강 지표 안정화를 기대할 수 있습니다."

        return ComprehensiveSummary(
            main_problems=main_problems,
            key_management_directions=key_management_directions,
            precautions=precautions,
            expected_effects=expected_effects
        )

    def _extract_main_problems(self, comprehensive_analysis: ComprehensiveAnalysis) -> List[str]:
        """주요 문제점 추출"""
        problems = []

        if "축적" in comprehensive_analysis.heavy_metals_analysis:
            problems.append("유해 중금속 축적")

        if "결핍" in comprehensive_analysis.minerals_analysis:
            problems.append("영양 미네랄 결핍")

        if "불안정" in comprehensive_analysis.health_indicators_analysis:
            problems.append("건강 지표 불안정")

        return problems[:3]  # 최대 3개

    def _extract_management_directions(self, comprehensive_analysis: ComprehensiveAnalysis) -> List[str]:
        """핵심 관리 방향 추출"""
        directions = []

        if "배출" in comprehensive_analysis.heavy_metals_analysis:
            directions.append("중금속 배출을 위한 해독 관리")

        if "보충" in comprehensive_analysis.minerals_analysis:
            directions.append("영양 미네랄 균형 회복")

        if "스트레스" in comprehensive_analysis.health_indicators_analysis:
            directions.append("스트레스 관리 및 생활습관 개선")

        return directions[:3]  # 최대 3개

    def _extract_precautions(self, comprehensive_analysis: ComprehensiveAnalysis) -> List[str]:
        """주의사항 추출"""
        precautions = []

        if "가공식품" in comprehensive_analysis.minerals_analysis:
            precautions.append("가공식품 섭취 제한")

        if "환경" in comprehensive_analysis.heavy_metals_analysis:
            precautions.append("유해 환경 노출 최소화")

        return precautions[:2]  # 최대 2개

    def _step6_nutritionist_summary(self, input_data: HairAnalysisInput, comprehensive_analysis: ComprehensiveAnalysis) -> NutritionistSummary:
        """6단계: 영양전문가 요약"""
        professional_summary = f"{input_data.personal_info.name}님의 검사 결과를 전문가 관점에서 분석한 결과입니다."
        priority_management = "우선적으로 중금속 배출과 영양 균형 회복이 필요합니다."
        supplement_strategy = "개인별 상태에 맞는 맞춤형 영양제 전략을 권장합니다."
        prognosis_analysis = "적절한 관리 시 3-6개월 내 개선 효과를 기대할 수 있습니다."

        return NutritionistSummary(
            professional_summary=professional_summary,
            priority_management=priority_management,
            supplement_strategy=supplement_strategy,
            prognosis_analysis=prognosis_analysis
        )

    def _step7_compressed_version(self, input_data: HairAnalysisInput, comprehensive_analysis: ComprehensiveAnalysis) -> CompressedVersion:
        """7단계: 압축 버전 (950-1000자)"""
        name = input_data.personal_info.name

        compressed_text = f"""
{name}님의 큐모발검사 결과를 종합적으로 분석한 결과입니다.

{comprehensive_analysis.first_paragraph}

검사 결과에 따른 주요 관리 사항은 다음과 같습니다. 첫째, 유해 중금속이 검출된 경우 항산화 영양소가 풍부한 식품 섭취와 생활 환경 개선이 필요합니다. 둘째, 영양 미네랄 불균형 개선을 위해 균형 잡힌 식단과 적절한 영양제 보충을 권장합니다. 셋째, 건강 지표 안정화를 위한 스트레스 관리와 충분한 수면, 규칙적인 운동이 중요합니다.

추천 식품으로는 견과류, 달걀, 녹색 잎 채소, 등 푸른 생선, 가공하지 않은 곡류 등의 섭취를 권장하며, 개인별 상태에 맞는 항산화 영양제나 비타민B군 보충을 추천합니다.

{name}님께서는 이러한 관리를 통해 약 3-6개월 후 재검사를 받으시기 바랍니다. 꾸준한 관리를 통해 영양 균형 개선과 건강 지표 안정화 효과를 기대할 수 있습니다.
        """.strip()

        # 950-1000자 범위로 조정
        if len(compressed_text) > 1000:
            compressed_text = compressed_text[:997] + "..."
        elif len(compressed_text) < 950:
            # 부족한 경우 내용 보완
            compressed_text += "\n\n정기적인 검사를 통해 건강한 삶을 유지하시기 바랍니다."

        return CompressedVersion(
            content=compressed_text,
            character_count=len(compressed_text)
        )