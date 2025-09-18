# 데이터 디렉토리

이 폴더에는 모발검사 분석을 위한 5개의 참조 노트 파일이 필요합니다:

## 필요한 파일들

1. **note1_basic.md** - 기본 인사말 템플릿
2. **note2_heavy_metals.md** - 중금속 분석 (연령별)
3. **note3_minerals.md** - 영양 미네랄 분석
4. **note4_health_indicators.md** - 건강 지표 분석
5. **note5_summary.md** - 요약 규칙 및 권장사항

## 배포 시 설정 방법

### 방법 1: 환경변수로 관리
```python
# 환경변수에 노트 내용을 Base64로 인코딩하여 저장
NOTE1_CONTENT=base64_encoded_content
NOTE2_CONTENT=base64_encoded_content
...
```

### 방법 2: 외부 데이터베이스 사용
```python
# PostgreSQL, MongoDB 등에 노트 내용 저장
DATABASE_URL=your_database_url
```

### 방법 3: 프라이빗 S3/클라우드 스토리지
```python
# AWS S3, Google Cloud Storage 등 사용
AWS_BUCKET_NAME=your_private_bucket
```

## 로컬 개발 시

로컬 개발 환경에서는 실제 `.md` 파일들을 이 디렉토리에 배치하여 사용하세요.
이 파일들은 `.gitignore`에 의해 git에 커밋되지 않습니다.