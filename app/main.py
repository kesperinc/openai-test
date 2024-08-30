from fastapi import FastAPI
from app.api.v1.endpoints import data, user

app = FastAPI()

# API 엔드포인트 등록
app.include_router(data.router, prefix="/api/v1/data", tags=["data"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}

