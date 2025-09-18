from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
from enum import Enum

class TestResultValue(str, Enum):
    NORMAL = "정상"
    HIGH = "높음"
    LOW = "낮음"

class HeavyMetalValue(str, Enum):
    NORMAL = "정상"
    HIGH = "높음"

class PersonalInfo(BaseModel):
    name: str = Field(..., description="검사자 이름")
    age: int = Field(..., ge=1, le=120, description="만 나이")
    special_notes: str = Field(default="없음", description="특이사항 (염색/펌/질환/직업 등)")

class HeavyMetals(BaseModel):
    mercury: HeavyMetalValue = Field(..., description="수은")
    arsenic: HeavyMetalValue = Field(..., description="비소")
    cadmium: HeavyMetalValue = Field(..., description="카드뮴")
    lead: HeavyMetalValue = Field(..., description="납")
    aluminum: HeavyMetalValue = Field(..., description="알루미늄")
    barium: HeavyMetalValue = Field(..., description="바륨")
    nickel: HeavyMetalValue = Field(..., description="니켈")
    uranium: HeavyMetalValue = Field(..., description="우라늄")
    bismuth: HeavyMetalValue = Field(..., description="비스무트")

class NutritionalMinerals(BaseModel):
    calcium: TestResultValue = Field(..., description="칼슘")
    magnesium: TestResultValue = Field(..., description="마그네슘")
    sodium: TestResultValue = Field(..., description="나트륨")
    potassium: TestResultValue = Field(..., description="칼륨")
    copper: TestResultValue = Field(..., description="구리")
    zinc: TestResultValue = Field(..., description="아연")
    phosphorus: TestResultValue = Field(..., description="인")
    iron: TestResultValue = Field(..., description="철")
    manganese: TestResultValue = Field(..., description="망간")
    chromium: TestResultValue = Field(..., description="크롬")
    selenium: TestResultValue = Field(..., description="셀레늄")

class HealthIndicators(BaseModel):
    insulin_sensitivity: TestResultValue = Field(..., description="인슐린 민감도")
    autonomic_nervous_system: TestResultValue = Field(..., description="자율신경계")
    stress_state: TestResultValue = Field(..., description="스트레스 상태")
    immune_skin_health: TestResultValue = Field(..., description="면역 및 피부 건강")
    adrenal_activity: TestResultValue = Field(..., description="부신 활성도")
    thyroid_activity: TestResultValue = Field(..., description="갑상선 활성도")

class HairAnalysisInput(BaseModel):
    personal_info: PersonalInfo
    heavy_metals: HeavyMetals
    nutritional_minerals: NutritionalMinerals
    health_indicators: HealthIndicators

    @validator('personal_info')
    def validate_personal_info(cls, v):
        if not v.name or not v.name.strip():
            raise ValueError('이름은 필수 입력 항목입니다.')
        return v

    class Config:
        json_encoders = {
            TestResultValue: lambda v: v.value,
            HeavyMetalValue: lambda v: v.value
        }
        schema_extra = {
            "example": {
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
        }