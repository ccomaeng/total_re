from pydantic import BaseModel, Field
from typing import List, Dict, Any

# Import from simple_output for compatibility
from .simple_output import HairAnalysisResult

class PersonalInfoSection(BaseModel):
    name: str = Field(..., description="이름")
    age: int = Field(..., description="나이")
    age_group: str = Field(..., description="연령대 구분")
    special_notes: str = Field(..., description="특이사항")

    heavy_metals_normal: List[str] = Field(default=[], description="정상 중금속")
    heavy_metals_high: List[str] = Field(default=[], description="높은 중금속")
    heavy_metals_normal_count: int = Field(default=0, description="정상 중금속 개수")
    heavy_metals_high_count: int = Field(default=0, description="높은 중금속 개수")

    minerals_normal: List[str] = Field(default=[], description="정상 미네랄")
    minerals_high: List[str] = Field(default=[], description="높은 미네랄")
    minerals_low: List[str] = Field(default=[], description="낮은 미네랄")
    minerals_normal_count: int = Field(default=0, description="정상 미네랄 개수")
    minerals_high_count: int = Field(default=0, description="높은 미네랄 개수")
    minerals_low_count: int = Field(default=0, description="낮은 미네랄 개수")

    health_normal: List[str] = Field(default=[], description="정상 건강지표")
    health_high: List[str] = Field(default=[], description="높은 건강지표")
    health_low: List[str] = Field(default=[], description="낮은 건강지표")
    health_normal_count: int = Field(default=0, description="정상 건강지표 개수")
    health_high_count: int = Field(default=0, description="높은 건강지표 개수")
    health_low_count: int = Field(default=0, description="낮은 건강지표 개수")

class ComprehensiveAnalysis(BaseModel):
    first_paragraph: str = Field(..., description="첫 번째 단락")
    heavy_metals_analysis: str = Field(default="", description="중금속 분석")
    minerals_analysis: str = Field(default="", description="영양 미네랄 분석")
    health_indicators_analysis: str = Field(default="", description="건강 상태 지표 분석")

class SummaryExplanation(BaseModel):
    title: str = Field(..., description="핵심 관리 포인트")
    recommended_foods: List[str] = Field(..., description="추천 식품 5개")
    recommended_supplements: str = Field(..., description="추천 영양제")
    recheck_period: str = Field(..., description="재검사 기간")

class StatisticsAnalysis(BaseModel):
    total_characters: int = Field(..., description="총 글자수")
    total_words: int = Field(..., description="총 단어수")
    paragraph_count: int = Field(..., description="단락 수")
    average_paragraph_length: int = Field(..., description="평균 단락 길이")

    first_paragraph_ratio: float = Field(..., description="첫 번째 단락 비율")
    heavy_metals_ratio: float = Field(..., description="중금속 분석 비율")
    minerals_ratio: float = Field(..., description="영양 미네랄 분석 비율")
    health_indicators_ratio: float = Field(..., description="건강 상태 지표 비율")

class ComprehensiveSummary(BaseModel):
    main_problems: List[str] = Field(..., description="주요 문제점")
    key_management_directions: List[str] = Field(..., description="핵심 관리 방향")
    precautions: List[str] = Field(..., description="주의사항")
    expected_effects: str = Field(..., description="기대 효과")

class NutritionistSummary(BaseModel):
    professional_summary: str = Field(..., description="전문가 관점의 간결한 요약")
    priority_management: str = Field(..., description="우선순위 관리방안")
    supplement_strategy: str = Field(..., description="영양제 전략")
    prognosis_analysis: str = Field(..., description="예후 분석")

class CompressedVersion(BaseModel):
    content: str = Field(..., description="950-1000자 압축 버전")
    character_count: int = Field(..., description="글자수")

class HairAnalysisOutput(BaseModel):
    personal_info_section: PersonalInfoSection
    comprehensive_analysis: ComprehensiveAnalysis
    summary_explanation: SummaryExplanation
    statistics_analysis: StatisticsAnalysis
    comprehensive_summary: ComprehensiveSummary
    nutritionist_summary: NutritionistSummary
    compressed_version: CompressedVersion

# 프론트엔드용 7단계 분석 결과 (플랫 구조)
class FullAnalysisResponse(BaseModel):
    personal_info_section: str = Field(..., description="개인정보 섹션 (텍스트)")
    comprehensive_analysis: str = Field(..., description="종합 분석 (텍스트)")
    statistics_analysis: str = Field(..., description="통계 분석 (텍스트)")
    summary_analysis: str = Field(..., description="종합 요약 (텍스트)")
    nutritionist_summary: str = Field(..., description="영양사 요약 (텍스트)")
    compressed_version: str = Field(..., description="압축 버전 (텍스트)")

class APIResponse(BaseModel):
    success: bool = Field(default=True, description="성공 여부")
    message: str = Field(default="", description="응답 메시지")
    data: HairAnalysisOutput = Field(None, description="분석 결과")
    errors: List[str] = Field(default=[], description="에러 목록")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "큐모발검사 종합멘트가 성공적으로 생성되었습니다.",
                "data": {
                    "personal_info_section": {
                        "name": "홍길동",
                        "age": 30,
                        "age_group": "성인",
                        "special_notes": "없음",
                        "heavy_metals_normal": ["수은", "비소", "카드뮴"],
                        "heavy_metals_high": ["납"],
                        "heavy_metals_normal_count": 8,
                        "heavy_metals_high_count": 1
                    }
                },
                "errors": []
            }
        }