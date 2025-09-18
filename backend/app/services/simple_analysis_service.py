import os
import re
from typing import Dict, List
from pathlib import Path

from ..models.input_models import HairAnalysisInput, TestResultValue, HeavyMetalValue
from ..models.simple_output import HairAnalysisResult

class SimpleHairAnalysisService:
    """간단화된 모발검사 분석 서비스 - 노트에서 직접 추출"""

    def __init__(self):
        self.notes_cache = {}
        self._load_note_files()

    def _load_note_files(self):
        """5개 핵심 노트 파일을 캐시에 로드"""
        note_files = {
            "note1_basic": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/1. 기본 구성_첫번째 단락.md",
            "note2_heavy_metals": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/2. 중금속 종류별 최종 멘트.md",
            "note3_minerals": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/3. 영양 미네랄 상세 조건별 최종 멘트.md",
            "note4_health_indicators": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/4. 건강 상태 지표별 최종 멘트.md",
            "note5_summary": "/Users/yujineom/Documents/Obsidian/2025/00. Inbox/큐모발검사 종합멘트/5. 요약 설명 파트 정리.md"
        }

        for key, file_path in note_files.items():
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.notes_cache[key] = f.read()

    def analyze(self, input_data: HairAnalysisInput) -> HairAnalysisResult:
        """메인 분석 함수"""

        # 1. 개인정보 섹션 생성
        personal_info_section = self._create_personal_info_section(input_data)

        # 2. 요약 정보 섹션 생성 (종합 분석 전에 표시)
        summary_section = self._create_summary_section(input_data)

        # 3. 종합 분석 결과 생성 (노트 1-4번에서 추출, 요약 제외)
        comprehensive_analysis = self._create_comprehensive_analysis_without_summary(input_data)

        # 4. 영양 권장사항
        nutritional_recommendations = self._create_nutritional_recommendations(input_data)

        # 5. 생활 개선 권장사항
        lifestyle_recommendations = self._create_lifestyle_recommendations(input_data)

        # 6. 추가 검사 권장사항
        additional_test_recommendations = self._create_test_recommendations(input_data)

        # 7. 주의사항
        precautions = self._create_precautions(input_data)

        # 8. 맺음말
        closing_remarks = self._create_closing_remarks(input_data)

        return HairAnalysisResult(
            personal_info_section=personal_info_section,
            summary_section=summary_section,
            comprehensive_analysis=comprehensive_analysis,
            nutritional_recommendations=nutritional_recommendations,
            lifestyle_recommendations=lifestyle_recommendations,
            additional_test_recommendations=additional_test_recommendations,
            precautions=precautions,
            closing_remarks=closing_remarks
        )

    def _create_personal_info_section(self, input_data: HairAnalysisInput) -> str:
        """맞춤 건강정보 제목 및 인사말 섹션 생성"""
        name = input_data.personal_info.name

        section = f"""<div style="text-align: center; margin-bottom: 40px; padding: 30px 0;">
    <h1 style="font-size: 32px; font-weight: bold; color: #1a365d; margin-bottom: 30px; letter-spacing: -0.5px;">
        {name}님의 맞춤 건강 정보
    </h1>
    <div style="line-height: 1.6; color: #4a5568; font-size: 16px; max-width: 800px; margin: 0 auto;">
        <p style="margin-bottom: 8px;">안녕하세요. 큐모발검사 영양전문가입니다.</p>
        <p style="margin-bottom: 8px;">{name}님의 사전 설문 내용과 모발 검사 결과를 참고하여 맞춤 영양상담지를 작성하였으니, 꼼꼼히 읽어보시길 바랍니다.</p>
        <p style="margin-bottom: 0; font-weight: 600; color: #2d3748;">더 건강해질 {name}님을 응원합니다!</p>
    </div>
</div>"""

        return section

    def _create_summary_section(self, input_data: HairAnalysisInput) -> str:
        """요약 정보 섹션 생성 (종합 분석 전에 표시)"""
        # 임시 종합 분석 생성 (요약 분석을 위해)
        temp_analysis_parts = []

        # 1단계: 첫 번째 단락 (노트1번)
        first_paragraph = self._extract_first_paragraph(input_data)
        temp_analysis_parts.append(first_paragraph)

        # 2단계: 중금속 분석 (노트2번)
        heavy_metals_analysis = self._extract_heavy_metals_analysis(input_data)
        if heavy_metals_analysis:
            temp_analysis_parts.append(heavy_metals_analysis)

        # 3단계: 영양 미네랄 분석 (노트3번)
        minerals_analysis = self._extract_minerals_analysis(input_data)
        if minerals_analysis:
            temp_analysis_parts.append(minerals_analysis)

        # 4단계: 건강 지표 분석 (노트4번)
        health_analysis = self._extract_health_analysis(input_data)
        if health_analysis:
            temp_analysis_parts.append(health_analysis)

        temp_comprehensive_analysis = "\n\n".join(temp_analysis_parts)

        # 5단계: 요약 설명 파트 (노트5번) - 종합멘트를 기반으로 생성
        summary_analysis = self._extract_summary_analysis(input_data, temp_comprehensive_analysis)

        return summary_analysis

    def _create_comprehensive_analysis_without_summary(self, input_data: HairAnalysisInput) -> str:
        """종합 분석 결과 생성 (노트 1-4번 기반, 요약 제외)"""

        # 1단계: 첫 번째 단락 (노트1번)
        first_paragraph = self._extract_first_paragraph(input_data)

        # 2단계: 중금속 분석 (노트2번)
        heavy_metals_analysis = self._extract_heavy_metals_analysis(input_data)

        # 3단계: 영양 미네랄 분석 (노트3번)
        minerals_analysis = self._extract_minerals_analysis(input_data)

        # 4단계: 건강 지표 분석 (노트4번)
        health_analysis = self._extract_health_analysis(input_data)

        # 결합하여 종합 분석 생성 (요약 제외)
        analysis_parts = [first_paragraph]

        if heavy_metals_analysis:
            analysis_parts.append(heavy_metals_analysis)

        if minerals_analysis:
            analysis_parts.append(minerals_analysis)

        if health_analysis:
            analysis_parts.append(health_analysis)

        comprehensive_result = "\n\n".join(analysis_parts)

        # 한국어 문법 검사 및 자연스러운 문장으로 변환
        improved_result = self._improve_korean_grammar(comprehensive_result)

        # 키워드 볼드 처리 적용 (현재 비활성화)
        return improved_result

    def _create_comprehensive_analysis(self, input_data: HairAnalysisInput) -> str:
        """종합 분석 결과 생성 (노트 1-4번 기반)"""

        # 1단계: 첫 번째 단락 (노트1번)
        first_paragraph = self._extract_first_paragraph(input_data)

        # 2단계: 중금속 분석 (노트2번)
        heavy_metals_analysis = self._extract_heavy_metals_analysis(input_data)

        # 3단계: 영양 미네랄 분석 (노트3번)
        minerals_analysis = self._extract_minerals_analysis(input_data)

        # 4단계: 건강 지표 분석 (노트4번)
        health_analysis = self._extract_health_analysis(input_data)

        # 임시 종합 분석 생성 (요약 분석을 위해)
        temp_analysis_parts = [first_paragraph]
        if heavy_metals_analysis:
            temp_analysis_parts.append(heavy_metals_analysis)
        if minerals_analysis:
            temp_analysis_parts.append(minerals_analysis)
        if health_analysis:
            temp_analysis_parts.append(health_analysis)

        temp_comprehensive_analysis = "\n\n".join(temp_analysis_parts)

        # 5단계: 요약 설명 파트 (노트5번) - 종합멘트를 기반으로 생성
        summary_analysis = self._extract_summary_analysis(input_data, temp_comprehensive_analysis)

        # 결합하여 최종 종합 분석 생성
        analysis_parts = [first_paragraph]

        if heavy_metals_analysis:
            analysis_parts.append(heavy_metals_analysis)

        if minerals_analysis:
            analysis_parts.append(minerals_analysis)

        if health_analysis:
            analysis_parts.append(health_analysis)

        if summary_analysis:
            analysis_parts.append(summary_analysis)

        comprehensive_result = "\n\n".join(analysis_parts)

        # 한국어 문법 검사 및 자연스러운 문장으로 변환
        return self._improve_korean_grammar(comprehensive_result)

    def _extract_first_paragraph(self, input_data: HairAnalysisInput) -> str:
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

        # 일반적인 경우: 테이블 규칙 적용
        return self._generate_first_paragraph_from_table(input_data)

    def _check_all_normal(self, input_data: HairAnalysisInput) -> bool:
        """모든 항목이 정상인지 확인"""
        heavy_metals_normal = all(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.NORMAL
            for field in input_data.heavy_metals.__fields__
        )
        minerals_normal = all(
            getattr(input_data.nutritional_minerals, field) == TestResultValue.NORMAL
            for field in input_data.nutritional_minerals.__fields__
        )
        health_normal = all(
            getattr(input_data.health_indicators, field) == TestResultValue.NORMAL
            for field in input_data.health_indicators.__fields__
        )
        return heavy_metals_normal and minerals_normal and health_normal

    def _generate_first_paragraph_from_table(self, input_data: HairAnalysisInput) -> str:
        """테이블 규칙에 따른 첫 번째 단락 생성"""
        name = input_data.personal_info.name

        # 유해 중금속 상태
        heavy_metals_high = []
        for field_name in input_data.heavy_metals.__fields__:
            if getattr(input_data.heavy_metals, field_name) == HeavyMetalValue.HIGH:
                korean_name = self._get_korean_metal_name(field_name)
                heavy_metals_high.append(korean_name)

        if heavy_metals_high:
            metals_str = ", ".join(heavy_metals_high)
            metal_text = f"유해 중금속은 {metals_str}이 축적되었습니다."
        else:
            metal_text = "유해 중금속은 모두 정상 수치 입니다."

        # 영양 미네랄 상태
        minerals_abnormal = []
        for field_name in input_data.nutritional_minerals.__fields__:
            if getattr(input_data.nutritional_minerals, field_name) != TestResultValue.NORMAL:
                korean_name = self._get_korean_mineral_name(field_name)
                minerals_abnormal.append(korean_name)

        if minerals_abnormal:
            minerals_str = ", ".join(minerals_abnormal)
            mineral_text = f"영양 미네랄은 {minerals_str}이 불균형 상태입니다."
        else:
            mineral_text = "영양 미네랄은 모두 정상 수치입니다."

        # 건강 상태 지표
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

        # 중금속과 영양 미네랄이 모두 정상인 경우 자연스럽게 결합
        if "모두 정상 수치" in metal_text and "모두 정상 수치" in mineral_text:
            combined_text = "유해 중금속과 영양 미네랄은 모두 정상 수치입니다."
            return f"{name}님의 모발검사결과, {combined_text} {health_text}"
        else:
            return f"{name}님의 모발검사결과, {metal_text} {mineral_text} {health_text}"

    def _extract_heavy_metals_analysis(self, input_data: HairAnalysisInput) -> str:
        """노트2번에서 중금속 분석 추출"""
        note2_content = self.notes_cache.get("note2_heavy_metals", "")
        analysis_parts = []

        # 높음인 중금속만 처리
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
                metal_analysis = self._extract_metal_content(note2_content, korean_name, input_data)
                if metal_analysis:
                    analysis_parts.append(metal_analysis)

        return "\n\n".join(analysis_parts)

    def _extract_metal_content(self, note_content: str, metal_name: str, input_data: HairAnalysisInput) -> str:
        """특정 중금속 멘트 추출 (수정된 정규식 사용)"""
        age = input_data.personal_info.age
        name = input_data.personal_info.name

        # 연령대 결정 (노트2번의 구조에 따라)
        if age <= 19:
            age_section = "19세 이하"
        else:
            age_section = "20세 이상"

        # 중금속 섹션 찾기 (다음 ## 섹션까지 전체 내용 추출)
        metal_pattern = f"## {metal_name}.*?(?=^## |\\Z)"
        metal_match = re.search(metal_pattern, note_content, re.DOTALL | re.MULTILINE)

        if not metal_match:
            return ""

        metal_section = metal_match.group(0)

        # 연령대 섹션 추출 (--- 구분자까지 또는 다음 ### 섹션까지)
        age_pattern = f"### {age_section}\\s*([\\s\\S]*?)(?=### |^---+|\\Z)"
        age_match = re.search(age_pattern, metal_section, re.MULTILINE)

        if age_match:
            content = age_match.group(1).strip()
            # [이름] 치환
            content = content.replace("[이름]", name)

            # 바륨/칼슘/마그네슘 + 파마/염색 케이스 - disclaimer 추가
            if metal_name in ["바륨", "칼슘", "마그네슘"] and self._is_perm_dye_treatment(input_data.personal_info.special_notes):
                disclaimer = self._add_perm_dye_disclaimer(metal_name, input_data)
                if disclaimer:
                    content += f"\n\n{disclaimer}"

            return content

        return ""

    def _extract_minerals_analysis(self, input_data: HairAnalysisInput) -> str:
        """노트3번에서 영양 미네랄 분석 추출 (실제 노트 내용 사용)"""
        note3_content = self.notes_cache.get("note3_minerals", "")
        minerals = input_data.nutritional_minerals
        age = input_data.personal_info.age
        name = input_data.personal_info.name

        content_parts = []
        minerals_to_skip = []

        # 복합조건 우선 처리 (칼슘+마그네슘)
        if minerals.calcium == TestResultValue.HIGH and minerals.magnesium == TestResultValue.HIGH:
            pattern = r"### 칼슘과 마그네슘 높음 \(복합조건\)\s*\*\*최종 멘트:\*\*\s*> (.+?)(?=\n\n|\*\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('magnesium')

        elif minerals.calcium == TestResultValue.LOW and minerals.magnesium == TestResultValue.LOW:
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 칼슘과 마그네슘 낮음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('magnesium')

        # 나트륨+칼륨 복합조건
        if minerals.sodium == TestResultValue.HIGH and minerals.potassium == TestResultValue.HIGH:
            age_condition = "10세 이하" if age <= 10 else "11세 이상 19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 나트륨과 칼륨 높음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('potassium')

        elif minerals.sodium == TestResultValue.LOW and minerals.potassium == TestResultValue.LOW:
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 나트륨과 칼륨 낮음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.append('potassium')

        # 아연+구리 복합조건
        if minerals.zinc == TestResultValue.HIGH and minerals.copper == TestResultValue.LOW:
            age_condition = "19세 이하" if age <= 19 else "20세 이상"
            pattern = f"### 아연 높음 \\+ 구리 낮음 \\+ {age_condition} \\(복합조건\\)\\s*\\*\\*최종 멘트:\\*\\*\\s*> (.+?)(?=\\n\\n|\\*\\*⚠️)"
            match = re.search(pattern, note3_content, re.DOTALL)
            if match:
                mineral_content = match.group(1).strip()
                content_parts.append(f"{mineral_content.replace('[이름]', name)}")
                minerals_to_skip.extend(['copper', 'zinc'])

        # 개별 미네랄 처리 (복합조건에서 생략되지 않은 것들만)
        mineral_map = {
            'calcium': '칼슘', 'magnesium': '마그네슘', 'sodium': '나트륨', 'potassium': '칼륨',
            'copper': '구리', 'zinc': '아연', 'phosphorus': '인', 'iron': '철분',
            'manganese': '망간', 'chromium': '크롬', 'selenium': '셀레늄'
        }

        for mineral_key, mineral_name in mineral_map.items():
            if mineral_key in minerals_to_skip:
                continue

            mineral_value = getattr(minerals, mineral_key)
            if mineral_value in [TestResultValue.HIGH, TestResultValue.LOW]:
                value_str = "높음" if mineral_value == TestResultValue.HIGH else "낮음"
                mineral_content = self._extract_mineral_condition(note3_content, mineral_name, value_str, age, name)
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

    def _extract_health_analysis(self, input_data: HairAnalysisInput) -> str:
        """노트4번에서 건강 지표 분석 추출 (실제 노트 내용 사용)"""
        note4_content = self.notes_cache.get("note4_health_indicators", "")
        health = input_data.health_indicators
        age = input_data.personal_info.age
        name = input_data.personal_info.name

        content_parts = []
        indicators_to_skip = []

        # 복합조건 우선 처리 (부신 + 갑상선)
        if health.adrenal_activity == TestResultValue.HIGH and health.thyroid_activity == TestResultValue.LOW:
            age_condition = "10세 이하" if age <= 10 else "11세 이상 19세 이하" if 11 <= age <= 19 else "20세 이상"

            # 수은 높음 조건도 함께 확인
            mercury_high = input_data.heavy_metals.mercury == HeavyMetalValue.HIGH
            if mercury_high:
                pattern = f"### 부신 활성도 - 높음 \\({age_condition} \\+ 수은 높음\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\n\\n|###)"
            else:
                pattern = f"### 부신 활성도 - 높음 \\({age_condition} \\+ 갑상선 활성도 낮음\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*: (.+?)(?=\\*\\*특이사항|\\n\\n|###)"

            match = re.search(pattern, note4_content, re.DOTALL)
            if match:
                health_content = match.group(1).strip()
                content_parts.append(f"{health_content.replace('[이름]', name)}")
                indicators_to_skip.extend(['adrenal_activity', 'thyroid_activity'])

        elif health.adrenal_activity == TestResultValue.LOW and health.thyroid_activity == TestResultValue.HIGH:
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
            if health_value in [TestResultValue.HIGH, TestResultValue.LOW]:
                value_str = "높음" if health_value == TestResultValue.HIGH else "낮음"
                health_content = self._extract_health_condition(note4_content, health_name, value_str, age, name, input_data)
                if health_content:
                    content_parts.append(f"{health_content}")

        return "\n\n".join(content_parts)

    def _extract_health_condition(self, note4_content: str, health_name: str, value: str, age: int, name: str, input_data: HairAnalysisInput) -> str:
        """특정 건강 지표의 조건별 멘트 추출"""
        patterns_to_try = []

        # 특별 조건들 - 부신 활성도 높음 처리
        if health_name == "부신 활성도" and value == "높음":
            # 수은이 높지 않은 경우 -> "일반" 조건 사용
            mercury_high = input_data.heavy_metals.mercury == HeavyMetalValue.HIGH
            if not mercury_high:
                # 일반 부신 높음 조건 우선 시도
                patterns_to_try.append(f"### 부신 활성도 - 높음 \\(일반\\)\\s*\\*\\*조건\\*\\*.*?\\*\\*최종 멘트\\*\\*:\\s*(.*?)(?=\\n### |\\n---|\Z)")

        elif health_name == "면역 및 피부 건강" and value == "높음":
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

    def _create_nutritional_recommendations(self, input_data: HairAnalysisInput) -> str:
        """영양 권장사항 생성"""
        recommendations = []

        # 기본 권장 식품
        basic_foods = ["견과류", "달걀", "녹색 잎 채소", "등 푸른 생선", "가공하지 않은 곡류"]

        # 중금속이 있는 경우
        has_heavy_metals = any(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH
            for field in input_data.heavy_metals.__fields__
        )

        if has_heavy_metals:
            recommendations.append("항산화 작용이 뛰어난 식품들을 섭취해주세요:")
            recommendations.append("- 브로콜리, 시금치 등의 녹색 채소")
            recommendations.append("- 블루베리, 토마토 등의 항산화 과일")
            recommendations.append("- 견과류 (아몬드, 호두 등)")

        recommendations.append(f"\n권장 식품 5가지: {', '.join(basic_foods)}")

        return "\n".join(recommendations)

    def _create_lifestyle_recommendations(self, input_data: HairAnalysisInput) -> str:
        """생활 개선 권장사항 생성"""
        recommendations = []

        # 스트레스 관련
        if input_data.health_indicators.stress_state == TestResultValue.HIGH:
            recommendations.append("스트레스 관리를 위한 명상이나 요가를 권장합니다.")

        # 부신 관련
        if input_data.health_indicators.adrenal_activity != TestResultValue.NORMAL:
            recommendations.append("충분한 수면(7-8시간)과 규칙적인 운동을 권장합니다.")

        # 기본 권장사항
        recommendations.extend([
            "규칙적인 운동 (주 3-4회, 30분 이상)",
            "충분한 수면 (7-8시간)",
            "금연 및 금주",
            "스트레스 관리"
        ])

        return "\n".join(recommendations)

    def _create_test_recommendations(self, input_data: HairAnalysisInput) -> str:
        """추가 검사 권장사항 생성"""
        # 중금속 유무에 따른 재검사 기간 결정
        has_heavy_metals = any(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH
            for field in input_data.heavy_metals.__fields__
        )

        if has_heavy_metals:
            return "중금속 축적이 확인되어 3개월 후 재검사를 권장합니다.\n정기적인 검사를 통해 개선 상황을 모니터링하시기 바랍니다."
        else:
            return "현재 상태 유지를 위해 6개월 후 정기 검사를 권장합니다.\n예방 차원에서의 지속적인 관리가 중요합니다."

    def _create_precautions(self, input_data: HairAnalysisInput) -> str:
        """주의사항 생성"""
        precautions = []

        # 중금속 관련 주의사항
        has_heavy_metals = any(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH
            for field in input_data.heavy_metals.__fields__
        )

        if has_heavy_metals:
            precautions.extend([
                "가공식품 및 인스턴트 식품 섭취를 제한해주세요.",
                "환경 오염 노출을 최소화해주세요.",
                "충분한 수분 섭취로 체내 해독을 도와주세요."
            ])

        # 기본 주의사항
        precautions.extend([
            "균형 잡힌 식단을 유지해주세요.",
            "과도한 다이어트나 음주는 피해주세요."
        ])

        return "\n".join(precautions)

    def _create_closing_remarks(self, input_data: HairAnalysisInput) -> str:
        """맺음말 생성"""
        name = input_data.personal_info.name

        return f"""{name}님께서는 위의 권장사항을 참고하시어 꾸준히 관리해주시기 바랍니다.

모발검사는 현재 상태를 파악하는 도구이며, 적절한 관리를 통해 충분히 개선될 수 있습니다.

건강한 생활습관과 균형 잡힌 식단을 통해 더 나은 건강 상태를 만들어 가시길 바랍니다.

정기적인 검사를 통해 지속적인 건강 관리를 하시기 바랍니다."""

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

    def _extract_summary_analysis(self, input_data: HairAnalysisInput, comprehensive_analysis: str) -> str:
        """노트5번에서 요약 설명 파트 추출 (노트5 완전 규칙 적용)"""
        note5_content = self.notes_cache.get("note5_summary", "")
        name = input_data.personal_info.name

        # 노트5 완전 규칙 기반 요약 설명 제목 생성
        summary_title = self._generate_summary_title(input_data)

        # 노트5 완전 규칙 기반 추천 식품 생성 (5개)
        recommended_foods = self._generate_recommended_foods(input_data, comprehensive_analysis)

        # 노트5 완전 규칙 기반 추천 영양제 생성
        recommended_supplements = self._generate_recommended_supplements(input_data, comprehensive_analysis)

        # 노트5 완전 규칙 기반 재검사 권장 기간 생성
        reexam_period = self._generate_reexam_period(input_data)

        # 요약 설명 파트 조합
        summary_parts = []

        if summary_title:
            summary_parts.append(summary_title)

        if recommended_foods:
            summary_parts.append(f"1. {recommended_foods}")

        if recommended_supplements:
            summary_parts.append(f"2. {recommended_supplements}")

        if reexam_period:
            summary_parts.append(f"3. {reexam_period}")

        return "\n\n".join(summary_parts)





    def _is_perm_dye_treatment(self, special_notes: str) -> bool:
        """파마/염색/탈색 여부 확인"""
        perm_dye_keywords = ["파마", "염색", "탈색"]
        return any(keyword in special_notes for keyword in perm_dye_keywords)

    def _add_perm_dye_disclaimer(self, metal_name: str, input_data: HairAnalysisInput) -> str:
        """바륨/칼슘/마그네슘+파마/염색 케이스용 disclaimer 생성"""
        if metal_name in ["바륨", "칼슘", "마그네슘"]:
            # 높음인 원소들 확인
            affected_elements = []

            # 바륨이 높음이면 항상 포함
            if input_data.heavy_metals.barium == HeavyMetalValue.HIGH:
                affected_elements.append("바륨")

            # 칼슘이 높음이면 포함
            if input_data.nutritional_minerals.calcium == TestResultValue.HIGH:
                affected_elements.append("칼슘")

            # 마그네슘이 높음이면 포함
            if input_data.nutritional_minerals.magnesium == TestResultValue.HIGH:
                affected_elements.append("마그네슘")

            if affected_elements:
                elements_str = ", ".join(affected_elements)
                if len(affected_elements) == 1:
                    return f"> 다만, {elements_str} 수치는 최근 펌이나 염색에 사용된 제품의 영향으로 일시적으로 높아졌을 가능성이 있으므로 크게 걱정하지 않으셔도 됩니다."
                else:
                    return f"> 다만, {elements_str} 수치는 최근 펌이나 염색에 사용된 제품의 영향으로 일시적으로 높아졌을 가능성이 있으므로 크게 걱정하지 않으셔도 됩니다."
        return ""

    # ===== 노트 5 완전 규칙 적용한 새로운 메서드들 =====

    def _generate_summary_title(self, input_data: HairAnalysisInput) -> str:
        """요약 설명 제목 생성 (노트5 완전 규칙 적용)"""
        name = input_data.personal_info.name

        # 파마/염색 처리 여부 확인
        is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

        # 1순위: 유해 중금속 축적 (파마/염색으로 인한 바륨 제외)
        heavy_metals_high = []
        for field in input_data.heavy_metals.__fields__:
            value = getattr(input_data.heavy_metals, field)
            if value == HeavyMetalValue.HIGH:
                # 파마/염색시 바륨은 실질적 건강 문제가 아니므로 제외
                if not (is_perm_dye and field == "barium"):
                    heavy_metals_high.append(field)

        if heavy_metals_high:
            # 추가 문제가 있는지 확인
            other_issues = []
            # 부신 기능 저하 확인
            if input_data.health_indicators.adrenal_activity == TestResultValue.LOW:
                other_issues.append("피로도")
            # 항산화 영양소 결핍 확인 (망간, 셀레늄, 구리 등)
            antioxidant_deficiency = (
                input_data.nutritional_minerals.selenium == TestResultValue.LOW or
                input_data.nutritional_minerals.manganese == TestResultValue.LOW or
                input_data.nutritional_minerals.copper == TestResultValue.LOW
            )
            if antioxidant_deficiency:
                other_issues.append("항산화")

            if other_issues:
                return f"{name}님께서는 전체적으로 중금속과 {other_issues[0]} 관리가 요구됩니다."
            else:
                return f"{name}님께서는 전체적으로 중금속 배출 관리가 요구됩니다."

        # 2순위: 부신 기능 저하 + 피로감
        if input_data.health_indicators.adrenal_activity == TestResultValue.LOW:
            return f"{name}님께서는 전체적으로 부신 피로도 관리가 요구됩니다."

        # 3순위: 스트레스 지표 높음
        if input_data.health_indicators.stress_state == TestResultValue.HIGH:
            return f"{name}님께서는 전체적으로 스트레스 관리가 요구됩니다."

        # 4순위: 혈당 관련 지표
        if input_data.health_indicators.insulin_sensitivity == TestResultValue.HIGH:
            return f"{name}님께서는 전체적으로 혈당 관리와 피로감 개선이 요구됩니다."

        # 5순위: 면역력 관련
        if input_data.health_indicators.immune_skin_health == TestResultValue.LOW:
            return f"{name}님께서는 전체적으로 면역력 강화가 요구됩니다."

        # 기본: 영양 균형 관리
        return f"{name}님께서는 전체적으로 영양 균형 관리가 요구됩니다."

    def _generate_recommended_foods(self, input_data: HairAnalysisInput, comprehensive_analysis: str) -> str:
        """추천 식품 5개 생성 (노트5 완전 규칙 적용 - 종합멘트 기반)"""
        # 1단계: 종합멘트에서 구체적으로 언급된 식품들 추출
        mentioned_foods = []

        # 종합멘트에서 자주 언급되는 식품들과 매칭
        food_keywords = {
            "견과류": ["견과류", "아몬드", "호두"],
            "달걀": ["달걀", "계란"],
            "브로콜리": ["브로콜리"],
            "시금치": ["시금치"],
            "등 푸른 생선": ["등 푸른 생선", "등푸른생선", "연어", "고등어"],
            "녹색 잎 채소": ["녹색 잎 채소", "녹색 채소", "시금치"],
            "가공하지 않은 곡류": ["가공하지 않은 곡류", "현미", "귀리"],
            "콩류": ["콩류", "콩", "두부"],
            "익힌 채소": ["익힌 채소", "채소"],
            "채소": ["채소"]
        }

        # 종합멘트에서 언급된 식품 찾기
        for food_name, keywords in food_keywords.items():
            for keyword in keywords:
                if keyword in comprehensive_analysis:
                    if food_name not in mentioned_foods:
                        mentioned_foods.append(food_name)
                    break

        # 2단계: 노트5 우선순위 적용 (샘플 분석 기반)
        priority_foods = ["견과류", "달걀", "녹색 잎 채소", "등 푸른 생선", "가공하지 않은 곡류"]

        # 3단계: 5개 완성
        final_foods = []

        # 우선순위 식품 중 언급된 것들 먼저 추가
        for food in priority_foods:
            if food in mentioned_foods and len(final_foods) < 5:
                final_foods.append(food)

        # 언급된 다른 식품들 추가
        for food in mentioned_foods:
            if food not in final_foods and len(final_foods) < 5:
                final_foods.append(food)

        # 4단계: 부족분을 건강 상태에 맞는 식품으로 보완
        if len(final_foods) < 5:
            # 파마/염색 여부 확인
            is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

            # 중금속 배출이 필요한 경우
            heavy_metals_high = any(
                getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH and not (is_perm_dye and field == "barium")
                for field in input_data.heavy_metals.__fields__
            )

            supplement_foods = []
            if heavy_metals_high:
                supplement_foods = ["브로콜리", "마늘", "양파", "시금치", "해조류"]
            elif input_data.health_indicators.adrenal_activity == TestResultValue.LOW:
                supplement_foods = ["아보카도", "바나나", "고구마", "현미"]
            elif input_data.health_indicators.stress_state == TestResultValue.HIGH:
                supplement_foods = ["콩류", "두부", "아몬드", "연어"]
            elif input_data.health_indicators.insulin_sensitivity == TestResultValue.HIGH:
                supplement_foods = ["귀리", "퀴노아", "렌틸콩", "블루베리"]
            else:
                supplement_foods = ["브로콜리", "시금치", "견과류", "등 푸른 생선", "달걀"]

            for food in supplement_foods:
                if food not in final_foods and len(final_foods) < 5:
                    final_foods.append(food)

        # 정확히 5개 맞추기
        if len(final_foods) > 5:
            final_foods = final_foods[:5]
        elif len(final_foods) < 5:
            default_foods = ["견과류", "달걀", "녹색 잎 채소", "등 푸른 생선", "브로콜리"]
            for food in default_foods:
                if food not in final_foods and len(final_foods) < 5:
                    final_foods.append(food)

        return f"{', '.join(final_foods)} 등의 보충과 균형 잡힌 식사가 권장됩니다."

    def _generate_recommended_supplements(self, input_data: HairAnalysisInput, comprehensive_analysis: str) -> str:
        """추천 영양제 생성 (노트5 완전 규칙 적용 - 종합멘트 기반)"""
        # 1단계: 종합멘트에서 구체적으로 언급된 영양제 추출
        mentioned_supplements = []

        # 영양제 키워드 매칭
        supplement_patterns = {
            "항산화 영양제": ["항산화 영양제", "비타민C", "비타민E", "셀레늄"],
            "비타민B": ["비타민B", "비타민B군"],
            "비타민D": ["비타민D"],
            "칼마디": ["칼슘", "마그네슘", "칼마디"],
            "종합 영양제": ["종합 영양제", "종합비타민"]
        }

        for supplement, keywords in supplement_patterns.items():
            for keyword in keywords:
                if keyword in comprehensive_analysis:
                    if supplement not in mentioned_supplements:
                        mentioned_supplements.append(supplement)
                    break

        # 2단계: 제목 기반 영양제 매칭
        management_point = self._generate_summary_title(input_data)

        # 파마/염색 여부 확인
        is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

        # 중금속 축적 확인 (파마/염색시 바륨 제외)
        heavy_metals_high = any(
            getattr(input_data.heavy_metals, field) == HeavyMetalValue.HIGH and not (is_perm_dye and field == "barium")
            for field in input_data.heavy_metals.__fields__
        )

        # 3단계: 종합멘트 기반 영양제 선정
        if mentioned_supplements:
            # 종합멘트에서 언급된 영양제 우선 반영
            if "중금속" in management_point and "항산화 영양제" in mentioned_supplements:
                # 복합 영양제인 경우
                if "비타민B" in mentioned_supplements:
                    problem = "중금속 배출과 부신 피로 개선"
                    supplement = "비타민C, E, 셀레늄이 함유된 항산화 영양제와 비타민B"
                elif "칼마디" in mentioned_supplements:
                    problem = "중금속 배출과 미네랄 불균형 개선"
                    supplement = "비타민C, E, 셀레늄이 함유된 항산화 영양제와 칼마디(칼슘, 마그네슘, 비타민D) 영양제"
                else:
                    problem = "중금속 배출"
                    supplement = "비타민C, E, 셀레늄이 함유된 항산화 영양제"
            elif "부신" in management_point and "비타민B" in mentioned_supplements:
                problem = "부신 피로도 개선"
                supplement = "비타민B 영양제"
            elif "스트레스" in management_point and "비타민D" in mentioned_supplements:
                problem = "스트레스 개선"
                supplement = "비타민D"
            elif "혈당" in management_point and "비타민B" in mentioned_supplements:
                problem = "부신 활성과 느끼시는 피로감 개선"
                supplement = "비타민B 영양제"
            else:
                # 첫 번째 언급된 영양제 사용
                problem = "전체적인 건강 관리"
                supplement = mentioned_supplements[0]
        else:
            # 4단계: 영양제 언급이 없는 경우 처리
            if "중금속" in management_point:
                # 특별 조건: 중금속 배출 관리 + 영양제 언급 없음 → 항산화 영양제 기본 추천
                problem = "중금속 배출"
                supplement = "항산화 영양제"
            elif "부신" in management_point:
                problem = "부신 피로도 개선"
                supplement = "비타민B 영양제"
            elif "스트레스" in management_point:
                problem = "스트레스 완화"
                supplement = "비타민D"
            elif "혈당" in management_point:
                problem = "혈당 관리와 피로감 개선"
                supplement = "비타민B 영양제"
            elif "면역" in management_point:
                problem = "면역력 강화"
                supplement = "비타민C와 아연이 함유된 영양제"
            else:
                problem = "전체적인 건강 관리"
                supplement = "종합 영양제"

        return f"{problem}을 위해 {supplement}를 추천 드립니다."

    def _generate_reexam_period(self, input_data: HairAnalysisInput) -> str:
        """재검사 권장 기간 생성 (노트5 완전 규칙 적용)"""
        name = input_data.personal_info.name
        age = input_data.personal_info.age

        # 파마/염색 처리 여부 확인
        is_perm_dye = self._is_perm_dye_treatment(input_data.personal_info.special_notes)

        # 유해 중금속 높음 확인 (파마/염색시 바륨 제외)
        heavy_metals_high = []
        for field in input_data.heavy_metals.__fields__:
            value = getattr(input_data.heavy_metals, field)
            if value == HeavyMetalValue.HIGH:
                if not (is_perm_dye and field == "barium"):
                    heavy_metals_high.append(field)

        # 영양 미네랄 불균형 확인 (노트5 세부 조건 적용)
        nutritional_minerals_abnormal = []
        for field in input_data.nutritional_minerals.__fields__:
            value = getattr(input_data.nutritional_minerals, field)
            if value != TestResultValue.NORMAL:
                # 파마/염색시 칼슘 높음, 마그네슘 높음 제외
                if is_perm_dye and field in ["calcium", "magnesium"] and value == TestResultValue.HIGH:
                    continue
                # 10세 이하 나트륨/칼륨 높음은 정상으로 해석
                if age <= 10 and field in ["sodium", "potassium"] and value == TestResultValue.HIGH:
                    continue
                nutritional_minerals_abnormal.append(field)

        # 조건별 재검사 기간 결정 (샘플 기반 간소화)
        if heavy_metals_high and not nutritional_minerals_abnormal:
            # 조건 1: 유해 중금속 높음 + 영양 미네랄 정상 → 3개월
            metal_names = self._get_korean_metal_names(heavy_metals_high)
            return f"{name}님께서는 {metal_names} 배출을 위한 영양 관리 후, 약 3개월 뒤 재검사를 통한 확인이 필요합니다."

        elif heavy_metals_high and nutritional_minerals_abnormal:
            # 조건 2: 유해 중금속 높음 + 영양 미네랄 불균형 → 3개월
            metal_names = self._get_korean_metal_names(heavy_metals_high)
            return f"{name}님께서는 {metal_names} 배출과 전반적인 영양 관리 후, 약 3개월 뒤 재검사를 통한 확인이 필요합니다."

        elif not heavy_metals_high and nutritional_minerals_abnormal:
            # 조건 3: 유해 중금속 정상 + 영양 미네랄 불균형 → 3-4개월
            # 관리점 기반으로 표현 결정
            management_point = self._generate_summary_title(input_data)
            if "스트레스" in management_point:
                return f"{name}님께서는 스트레스 및 영양 관리 후, 약 3~4개월 뒤 재검사를 통한 확인이 필요합니다."
            elif "부신" in management_point:
                return f"{name}님께서는 부신 피로감 개선 후, 약 3~4개월 뒤 재검사를 통한 확인이 필요합니다."
            else:
                return f"{name}님께서는 영양 관리 후, 약 3~4개월 뒤 재검사를 통한 확인이 필요합니다."

        else:
            # 조건 4: 모든 항목 정상 → 5-6개월
            # 관리점 기반으로 표현 및 기간 결정
            management_point = self._generate_summary_title(input_data)
            if "부신" in management_point:
                return f"{name}님께서는 부신 피로감 개선 후, 약 5개월 뒤 재검사를 통한 확인이 필요합니다."
            elif "혈당" in management_point or "피로감" in management_point:
                return f"{name}님께서는 영양 관리 후, 약 6개월 뒤 재검사를 통한 확인이 필요합니다."
            else:
                return f"{name}님께서는 영양 관리 후, 약 5~6개월 뒤 재검사를 통한 확인이 필요합니다."

    def _get_korean_metal_names(self, metal_fields: list) -> str:
        """영어 중금속 필드명을 한국어로 변환"""
        metal_map = {
            "mercury": "수은", "arsenic": "비소", "cadmium": "카드뮴", "lead": "납",
            "aluminum": "알루미늄", "barium": "바륨", "nickel": "니켈",
            "uranium": "우라늄", "bismuth": "비스무트"
        }
        korean_names = [metal_map.get(field, field) for field in metal_fields]
        return korean_names[0] if len(korean_names) == 1 else "과 ".join(korean_names)

    def _get_korean_mineral_names(self, mineral_fields: list) -> str:
        """영어 미네랄 필드명을 한국어로 변환"""
        mineral_map = {
            "calcium": "칼슘", "magnesium": "마그네슘", "sodium": "나트륨", "potassium": "칼륨",
            "copper": "구리", "zinc": "아연", "phosphorus": "인", "iron": "철분",
            "manganese": "망간", "chromium": "크롬", "selenium": "셀레늄"
        }
        korean_names = [mineral_map.get(field, field) for field in mineral_fields]
        return korean_names[0] if len(korean_names) == 1 else "과 ".join(korean_names)

    def _improve_korean_grammar(self, text: str) -> str:
        """한국어 문법 검사 및 자연스러운 문장으로 개선"""

        # 0. 오타 수정
        text = text.replace('수는 축적이 심해지면', '수은 축적이 심해지면')
        text = text.replace('관리가는 것이', '관리하는 것이')
        text = text.replace('될 수 있은', '될 수 있는')
        text = text.replace('꼐서는', '께서는')
        text = text.replace('수 있은', '수 있는')

        # 1. 중복 조사 제거 (을/를, 이/가, 은/는 등)
        text = re.sub(r'을/를', '을', text)
        text = re.sub(r'이/가', '이', text)
        text = re.sub(r'은/는', '은', text)
        text = re.sub(r'과/와', '와', text)
        text = re.sub(r'으로/로', '로', text)

        # 2. 불완전한 문장 수정
        # "~과 " 로 끝나는 불완전한 문장 수정
        text = re.sub(r'(\w+)과 \s*(?=\n|$)', r'\1', text)
        text = re.sub(r'(\w+)와 \s*(?=\n|$)', r'\1', text)

        # 3. 중복 단어 제거
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)

        # 4. 띄어쓰기 정리
        # 연속된 공백을 하나로 줄이기
        text = re.sub(r' {2,}', ' ', text)

        # 문장 부호 앞의 불필요한 공백 제거
        text = re.sub(r' +([,.!?])', r'\1', text)

        # 5. 조사 자동 교정 (받침 유무에 따른)
        def fix_particles(match):
            word = match.group(1)
            particle = match.group(2)

            # 마지막 글자의 받침 확인
            last_char = word[-1]
            has_final_consonant = (ord(last_char) - ord('가')) % 28 != 0

            # 조사 교정
            if particle in ['을', '를']:
                return word + ('을' if has_final_consonant else '를')
            elif particle in ['이', '가']:
                return word + ('이' if has_final_consonant else '가')
            elif particle in ['은', '는']:
                return word + ('은' if has_final_consonant else '는')
            elif particle in ['과', '와']:
                return word + ('과' if has_final_consonant else '와')
            else:
                return match.group(0)

        # 조사 패턴 매칭 및 교정
        text = re.sub(r'(\w+)(을|를|이|가|은|는|과|와)', fix_particles, text)

        # 6. 문장 연결 개선
        # "~습니다. 그리고" -> "~하며,"
        text = re.sub(r'습니다\.\s*그리고\s*', '하며, ', text)
        text = re.sub(r'됩니다\.\s*그리고\s*', '되며, ', text)
        text = re.sub(r'있습니다\.\s*그리고\s*', '있으며, ', text)

        # 7. 어색한 표현 수정
        # "~과 같은" 패턴 정리
        text = re.sub(r'(\w+)과 같은\s+(\w+)', r'\1 등의 \2', text)

        # 8. 마지막 정리
        # 연속된 줄바꿈을 두 개로 제한
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 문서 시작과 끝의 공백 제거
        text = text.strip()

        return text

    def _apply_bold_formatting(self, text: str) -> str:
        """종합 분석 결과에 영양 전문가 관점에서 중요한 키워드와 문구에 볼드 처리 적용"""

        # 중요한 키워드와 문구들 (영양 전문가 관점)
        important_keywords = [
            # 건강 상태 평가
            "영양 관리가 매우 잘 되고",
            "지금처럼 관리해주시길",
            "모든.*정상.*수치",

            # 위험 요소
            "중금속.*노출.*축적",
            "영양 불균형",
            "스트레스",
            "생활습관.*변화",

            # 관리 권장사항
            "미리 확인.*중요",
            "재검사.*권장",
            "6개월.*재검사",
            "지속적.*관리",
            "꾸준한 관리",

            # 영양소 관련
            "비타민", "미네랄", "영양제", "보충제",
            "항산화", "오메가-3", "프로바이오틱스",

            # 식품 관련
            "견과류", "녹색 채소", "등 푸른 생선",
            "현미", "퀴노아", "블루베리"
        ]

        import re
        formatted_text = text

        # 각 키워드/문구를 찾아서 볼드 처리
        for keyword in important_keywords:
            pattern = re.compile(keyword, re.IGNORECASE)
            matches = pattern.findall(formatted_text)
            for match in matches:
                if not match.startswith('**'):  # 이미 볼드 처리되지 않은 경우만
                    formatted_text = formatted_text.replace(match, f"**{match}**")

        return formatted_text

    def _new_generate_summary_title(self, input_data: HairAnalysisInput) -> str:
        """새로운 요약 설명 제목 생성 (기존 _generate_summary_title과 동일한 로직)"""
        return self._generate_summary_title(input_data)