from pydantic import BaseModel, Field
from typing import List

class HairAnalysisResult(BaseModel):
    """간단한 분석 결과 모델 - 프론트엔드와 직접 연결"""

    personal_info_section: str = Field(..., description="개인정보 섹션")
    summary_section: str = Field(..., description="요약 정보 섹션")
    comprehensive_analysis: str = Field(..., description="종합 분석 결과")
    nutritional_recommendations: str = Field(..., description="영양 권장사항")
    lifestyle_recommendations: str = Field(..., description="생활 개선 권장사항")
    additional_test_recommendations: str = Field(..., description="추가 검사 권장사항")
    precautions: str = Field(..., description="주의사항")
    closing_remarks: str = Field(..., description="맺음말")

class SimpleAPIResponse(BaseModel):
    success: bool = Field(default=True, description="성공 여부")
    message: str = Field(default="", description="응답 메시지")
    data: HairAnalysisResult = Field(None, description="분석 결과")
    errors: List[str] = Field(default=[], description="에러 목록")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "큐모발검사 종합멘트가 성공적으로 생성되었습니다.",
                "data": {
                    "personal_info_section": "홍길동님 (30세)의 모발검사결과",
                    "summary_section": "홍길동님께서는 전체적으로 중금속과 항산화 관리가 요구됩니다...",
                    "comprehensive_analysis": "홍길동님의 모발검사결과, 유해 중금속은 모두 정상 수치 입니다...",
                    "nutritional_recommendations": "견과류, 달걀, 녹색 잎 채소 등을 권장합니다.",
                    "lifestyle_recommendations": "충분한 수면과 규칙적인 운동을 권장합니다.",
                    "additional_test_recommendations": "3-6개월 후 재검사를 권장합니다.",
                    "precautions": "가공식품 섭취를 줄이시기 바랍니다.",
                    "closing_remarks": "꾸준한 관리를 통해 건강한 삶을 유지하시기 바랍니다."
                },
                "errors": []
            }
        }