# app/api/v1/endpoints.py
from fastapi import APIRouter
from app.service.data_processing.text_processor import TextProcessor
from app.service.models.word2vec_trainer import Word2VecTrainer
from app.service.models.tfidf_trainer import TFIDFTrainer
from app.service.inference.inference import InferenceService

router = APIRouter()

# 전처리 엔드포인트
@router.post("/preprocess")
async def preprocess():
    # TextProcessor 인스턴스 생성 및 전처리 실행
    file_list = ['data/raw/1gapja.txt', 'data/raw/2gapsul.txt', 'data/raw/3gapsin.txt', 'data/raw/4gapo.txt', 'data/raw/5gapjin.txt', 'data/raw/6gapin.txt']
    processor = TextProcessor(file_list)
    processor.preprocess_text()
    processor.save_processed_files()
    return {"status": "success", "message": "Text preprocessing completed."}

# 훈련 엔드포인트 (Word2Vec 예시)
@router.post("/train/word2vec")
async def train_word2vec():
    file_list = ['data/normalized/normalized_1gapja.txt', 'data/normalized/normalized_2gapsul.txt']
    trainer = Word2VecTrainer(file_list)
    trainer.train()
    return {"status": "success", "message": "Word2Vec training completed."}

# 추론 엔드포인트
@router.post("/inference")
async def inference(input_text: str):
    inference_service = InferenceService()
    result = inference_service.predict(input_text)
    return {"status": "success", "result": result}
