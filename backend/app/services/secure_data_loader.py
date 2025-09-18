"""
보안 데이터 로더 - 환경변수나 외부 소스에서 참조 노트를 로드
"""
import os
import base64
from typing import Dict
from pathlib import Path

try:
    import boto3
except ImportError:
    boto3 = None

class SecureDataLoader:
    """민감한 데이터를 안전하게 로드하는 클래스"""

    @staticmethod
    def load_from_env() -> Dict[str, str]:
        """환경변수에서 Base64 인코딩된 노트 내용을 로드"""
        notes = {}
        for i in range(1, 6):
            env_key = f"NOTE{i}_CONTENT"
            encoded_content = os.getenv(env_key)
            if encoded_content:
                decoded = base64.b64decode(encoded_content).decode('utf-8')
                notes[f"note{i}"] = decoded
        return notes

    @staticmethod
    def load_from_s3() -> Dict[str, str]:
        """AWS S3에서 노트 파일을 로드"""
        notes = {}

        if not boto3:
            return notes

        bucket_name = os.getenv("AWS_BUCKET_NAME")

        if not bucket_name:
            return notes

        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        for i in range(1, 6):
            try:
                obj = s3.get_object(
                    Bucket=bucket_name,
                    Key=f"notes/note{i}.md"
                )
                notes[f"note{i}"] = obj['Body'].read().decode('utf-8')
            except Exception as e:
                print(f"Error loading note{i} from S3: {e}")

        return notes

    @staticmethod
    def load_from_local() -> Dict[str, str]:
        """로컬 파일 시스템에서 노트를 로드 (개발용)"""
        notes = {}
        data_dir = Path(__file__).parent.parent / "data"

        note_files = {
            "note1": "note1_basic.md",
            "note2": "note2_heavy_metals.md",
            "note3": "note3_minerals.md",
            "note4": "note4_health_indicators.md",
            "note5": "note5_summary.md"
        }

        for key, filename in note_files.items():
            file_path = data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    notes[key] = f.read()

        return notes

    @classmethod
    def load_notes(cls) -> Dict[str, str]:
        """
        우선순위에 따라 노트를 로드:
        1. 환경변수 (프로덕션)
        2. S3 (프로덕션 대안)
        3. 로컬 파일 (개발)
        """
        # 환경변수 확인
        notes = cls.load_from_env()
        if notes:
            print("Loaded notes from environment variables")
            return notes

        # S3 확인
        if os.getenv("AWS_BUCKET_NAME"):
            notes = cls.load_from_s3()
            if notes:
                print("Loaded notes from S3")
                return notes

        # 로컬 파일 (개발 환경)
        notes = cls.load_from_local()
        if notes:
            print("Loaded notes from local files")
            return notes

        raise Exception("No notes data source available!")