from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from service.data_processing.text_processor import TextProcessor
from service.models.word2vec_trainer import Word2VecTrainer
from service.inference.inference import InferenceService

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# 전처리, 훈련, 추론 엔드포인트는 위와 동일
