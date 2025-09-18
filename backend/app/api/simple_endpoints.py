from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import traceback

from ..models.input_models import HairAnalysisInput
from ..models.simple_output import SimpleAPIResponse
from ..services.simple_analysis_service import SimpleHairAnalysisService

router = APIRouter()

# 서비스 인스턴스 생성
analysis_service = SimpleHairAnalysisService()

@router.post("/analyze", response_model=SimpleAPIResponse)
async def analyze_hair_test(input_data: HairAnalysisInput):
    """모발검사 결과 분석 및 종합멘트 생성"""
    try:
        # 분석 수행
        result = analysis_service.analyze(input_data)

        return SimpleAPIResponse(
            success=True,
            message="큐모발검사 종합멘트가 성공적으로 생성되었습니다.",
            data=result
        )

    except Exception as e:
        # 에러 로깅
        error_details = traceback.format_exc()
        print(f"Analysis error: {error_details}")

        return SimpleAPIResponse(
            success=False,
            message="분석 중 오류가 발생했습니다.",
            errors=[str(e)]
        )

@router.get("/test-data")
async def get_test_data():
    """테스트용 데이터 반환"""
    return {
        "personal_info": {
            "name": "홍길동",
            "age": 35,
            "special_notes": "없음"
        },
        "heavy_metals": {
            "mercury": "높음",
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
            "calcium": "낮음",
            "magnesium": "정상",
            "sodium": "정상",
            "potassium": "정상",
            "copper": "정상",
            "zinc": "낮음",
            "phosphorus": "정상",
            "iron": "정상",
            "manganese": "정상",
            "chromium": "정상",
            "selenium": "정상"
        },
        "health_indicators": {
            "insulin_sensitivity": "정상",
            "autonomic_nervous_system": "정상",
            "stress_state": "높음",
            "immune_skin_health": "정상",
            "adrenal_activity": "낮음",
            "thyroid_activity": "정상"
        }
    }

@router.get("/health")
async def health_check():
    """서비스 상태 확인"""
    return {
        "status": "healthy",
        "message": "큐모발검사 분석 서비스가 정상 작동 중입니다.",
        "notes_loaded": len(analysis_service.notes_cache)
    }