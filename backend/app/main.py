import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .models.input_models import HairAnalysisInput
from .models.output_models import APIResponse, HairAnalysisOutput, FullAnalysisResponse
from .models.simple_output import SimpleAPIResponse
from .services.analysis_service import HairAnalysisService
from .services.simple_analysis_service import SimpleHairAnalysisService
from .services.prompt_based_analysis_service import PromptBasedAnalysisService

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="큐모발검사 종합멘트 자동 생성 API",
    description="모발검사 결과를 입력받아 개인 맞춤형 종합멘트를 자동 생성하는 API",
    version="1.0.0"
)

# CORS 설정 - 환경변수로 관리
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 인스턴스 생성
analysis_service = HairAnalysisService()
simple_analysis_service = SimpleHairAnalysisService()
prompt_based_analysis_service = PromptBasedAnalysisService()

@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "큐모발검사 종합멘트 자동 생성 API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analysis": "/analyze",
            "full_analysis": "/api/hair-analysis/full",
            "simple_analysis": "/simple/analyze",
            "prompt_based_analysis": "/prompt/analyze",
            "test_data": "/test-data",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "message": "API is running normally"}

@app.post("/analyze", response_model=APIResponse)
async def analyze_hair_test(input_data: HairAnalysisInput):
    """
    모발검사 결과 분석 및 종합멘트 생성

    - **input_data**: 모발검사 입력 데이터
        - personal_info: 개인정보 (이름, 나이, 특이사항)
        - heavy_metals: 유해 중금속 검사 결과 (9종)
        - nutritional_minerals: 영양 미네랄 검사 결과 (11종)
        - health_indicators: 건강 상태 지표 검사 결과 (6종)

    - **return**: 생성된 종합멘트 (7단계 분석 결과)
    """
    try:
        # 입력 데이터 검증
        if not input_data.personal_info.name.strip():
            raise HTTPException(
                status_code=400,
                detail="이름은 필수 입력 항목입니다."
            )

        # 분석 수행
        result = analysis_service.analyze(input_data)

        return APIResponse(
            success=True,
            message="큐모발검사 종합멘트가 성공적으로 생성되었습니다.",
            data=result
        )

    except ValidationError as e:
        # Pydantic 검증 오류
        error_messages = []
        for error in e.errors():
            field = " -> ".join([str(loc) for loc in error["loc"]])
            message = error["msg"]
            error_messages.append(f"{field}: {message}")

        return APIResponse(
            success=False,
            message="입력 데이터 검증 실패",
            errors=error_messages
        )

    except Exception as e:
        # 기타 서버 오류
        return APIResponse(
            success=False,
            message="서버 내부 오류가 발생했습니다.",
            errors=[str(e)]
        )

@app.get("/test-data")
async def get_test_data():
    """테스트용 샘플 데이터 반환"""
    return {
        "personal_info": {
            "name": "홍길동",
            "age": 30,
            "special_notes": "없음"
        },
        "heavy_metals": {
            "mercury": "정상",
            "arsenic": "정상",
            "cadmium": "정상",
            "lead": "높음",
            "aluminum": "정상",
            "barium": "정상",
            "nickel": "정상",
            "uranium": "정상",
            "bismuth": "정상"
        },
        "nutritional_minerals": {
            "calcium": "정상",
            "magnesium": "낮음",
            "sodium": "높음",
            "potassium": "높음",
            "copper": "정상",
            "zinc": "정상",
            "phosphorus": "정상",
            "iron": "정상",
            "manganese": "정상",
            "chromium": "정상",
            "selenium": "정상"
        },
        "health_indicators": {
            "insulin_sensitivity": "정상",
            "autonomic_nervous_system": "낮음",
            "stress_state": "높음",
            "immune_skin_health": "정상",
            "adrenal_activity": "높음",
            "thyroid_activity": "낮음"
        }
    }

@app.post("/simple/analyze", response_model=SimpleAPIResponse)
async def simple_analyze_hair_test(input_data: HairAnalysisInput):
    """
    간단한 모발검사 결과 분석 및 종합멘트 생성 (프론트엔드용)

    실제 노트 파일에서 템플릿을 추출하여 멘트 생성
    """
    try:
        # 입력 데이터 검증
        if not input_data.personal_info.name.strip():
            raise HTTPException(
                status_code=400,
                detail="이름은 필수 입력 항목입니다."
            )

        # 간단한 분석 수행
        result = simple_analysis_service.analyze(input_data)

        return SimpleAPIResponse(
            success=True,
            message="큐모발검사 종합멘트가 성공적으로 생성되었습니다.",
            data=result
        )

    except Exception as e:
        # 에러 처리
        import traceback
        print(f"Simple analysis error: {traceback.format_exc()}")

        return SimpleAPIResponse(
            success=False,
            message="분석 중 오류가 발생했습니다.",
            errors=[str(e)]
        )

@app.post("/prompt/analyze", response_model=SimpleAPIResponse)
async def prompt_based_analyze_hair_test(input_data: HairAnalysisInput):
    """
    프롬프트 기반 모발검사 결과 분석 및 종합멘트 생성 (100% 프롬프트 요구사항 반영)

    5개 노트에서 조건별 멘트를 정확히 추출하여 7단계 순차적 분석 수행
    """
    try:
        # 입력 데이터 검증
        if not input_data.personal_info.name.strip():
            raise HTTPException(
                status_code=400,
                detail="이름은 필수 입력 항목입니다."
            )

        # 프롬프트 기반 분석 수행
        result = prompt_based_analysis_service.analyze(input_data)

        return SimpleAPIResponse(
            success=True,
            message="프롬프트 기반 큐모발검사 종합멘트가 성공적으로 생성되었습니다.",
            data=result
        )

    except Exception as e:
        # 에러 처리
        import traceback
        print(f"Prompt-based analysis error: {traceback.format_exc()}")

        return SimpleAPIResponse(
            success=False,
            message="프롬프트 기반 분석 중 오류가 발생했습니다.",
            errors=[str(e)]
        )

@app.post("/api/hair-analysis/full", response_model=FullAnalysisResponse)
async def full_analysis_hair_test(input_data: HairAnalysisInput):
    """
    7단계 모발검사 결과 분석 (프론트엔드용 플랫 구조)

    기존 /analyze 엔드포인트의 결과를 프론트엔드가 사용하기 쉬운 문자열 형태로 변환
    """
    try:
        # 입력 데이터 검증
        if not input_data.personal_info.name.strip():
            raise HTTPException(
                status_code=400,
                detail="이름은 필수 입력 항목입니다."
            )

        # 기존 분석 서비스 사용
        result = analysis_service.analyze(input_data)

        # 복잡한 구조를 플랫 문자열로 변환
        flat_result = _convert_to_flat_structure(result)

        return flat_result

    except Exception as e:
        # 에러 처리
        import traceback
        print(f"Full analysis error: {traceback.format_exc()}")

        raise HTTPException(
            status_code=500,
            detail=f"분석 중 오류가 발생했습니다: {str(e)}"
        )

def _convert_to_flat_structure(analysis_output: HairAnalysisOutput) -> FullAnalysisResponse:
    """복잡한 분석 결과를 프론트엔드용 플랫 구조로 변환"""

    # 1. 맞춤 건강상담 인사말 섹션
    personal_info = analysis_output.personal_info_section
    personal_info_text = f"""{personal_info.name}님 맞춤 건강 상담

안녕하세요. 큐모발검사 영양전문가입니다. {personal_info.name}님의 사전 설문 내용과 모발 검사 결과를 참고하여 맞춤 영양상담지를 작성하였으니, 꼼꼼히 읽어보시길 바랍니다. 더 건강해질 {personal_info.name}님을 응원합니다!

[유해 중금속 검사 결과]
• 정상 수치 ({personal_info.heavy_metals_normal_count}개): {', '.join(personal_info.heavy_metals_normal)}
• 높은 수치 ({personal_info.heavy_metals_high_count}개): {', '.join(personal_info.heavy_metals_high)}

[영양 미네랄 검사 결과]
• 정상 수치 ({personal_info.minerals_normal_count}개): {', '.join(personal_info.minerals_normal)}
• 높은 수치 ({personal_info.minerals_high_count}개): {', '.join(personal_info.minerals_high)}
• 낮은 수치 ({personal_info.minerals_low_count}개): {', '.join(personal_info.minerals_low)}

[건강 상태 지표 검사 결과]
• 정상 수치 ({personal_info.health_normal_count}개): {', '.join(personal_info.health_normal)}
• 높은 수치 ({personal_info.health_high_count}개): {', '.join(personal_info.health_high)}
• 낮은 수치 ({personal_info.health_low_count}개): {', '.join(personal_info.health_low)}"""

    # 2. 종합 분석 변환
    comp_analysis = analysis_output.comprehensive_analysis
    comprehensive_text = f"""{comp_analysis.first_paragraph}

[유해 중금속 분석]
{comp_analysis.heavy_metals_analysis}

[영양 미네랄 분석]
{comp_analysis.minerals_analysis}

[건강 상태 지표 분석]
{comp_analysis.health_indicators_analysis}"""

    # 3. 통계 분석 변환
    stats = analysis_output.statistics_analysis
    statistics_text = f"""[종합멘트 통계 정보]
• 총 글자수: {stats.total_characters:,}자
• 총 단어수: {stats.total_words:,}개
• 단락 수: {stats.paragraph_count}개
• 평균 단락 길이: {stats.average_paragraph_length}자

[섹션별 비율]
• 첫 번째 단락: {stats.first_paragraph_ratio:.1%}
• 중금속 분석: {stats.heavy_metals_ratio:.1%}
• 영양 미네랄 분석: {stats.minerals_ratio:.1%}
• 건강 지표 분석: {stats.health_indicators_ratio:.1%}"""

    # 4. 종합 요약 변환 (Note 5 규칙)
    summary = analysis_output.summary_explanation
    comp_summary = analysis_output.comprehensive_summary
    summary_text = f"""[{summary.title}]

[추천 식품 (정확히 5개)]
{chr(10).join([f'• {food}' for food in summary.recommended_foods])}

[추천 영양제]
{summary.recommended_supplements}

[재검사 기간]
{summary.recheck_period}

[주요 문제점]
{chr(10).join([f'• {problem}' for problem in comp_summary.main_problems])}

[핵심 관리 방향]
{chr(10).join([f'• {direction}' for direction in comp_summary.key_management_directions])}

[주의사항]
{chr(10).join([f'• {precaution}' for precaution in comp_summary.precautions])}

[기대 효과]
{comp_summary.expected_effects}"""

    # 5. 영양사 요약 변환
    nutritionist = analysis_output.nutritionist_summary
    nutritionist_text = f"""[전문가 관점의 요약]
{nutritionist.professional_summary}

[우선순위 관리방안]
{nutritionist.priority_management}

[영양제 전략]
{nutritionist.supplement_strategy}

[예후 분석]
{nutritionist.prognosis_analysis}"""

    # 6. 압축 버전
    compressed = analysis_output.compressed_version
    compressed_text = f"{compressed.content}\n\n(글자수: {compressed.character_count}자)"

    return FullAnalysisResponse(
        personal_info_section=personal_info_text,
        comprehensive_analysis=comprehensive_text,
        statistics_analysis=statistics_text,
        summary_analysis=summary_text,
        nutritionist_summary=nutritionist_text,
        compressed_version=compressed_text
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)