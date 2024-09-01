# app/api/v1/endpoints.py

from fastapi import APIRouter
from service.data_processing.text_processor import TextProcessor
import os

router = APIRouter()

@router.post("/preprocess")
async def preprocess():
    # 원본 데이터 경로 설정
    data_dir = "data/origin"
    
    # 디렉토리에서 파일 목록 가져오기
    file_list = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.txt')]
    
    # TextProcessor 인스턴스 생성 및 전처리 수행
    text_processor = TextProcessor(file_list)
    text_processor.preprocess_text()
    
    return {"message": "전처리가 완료되었습니다."}