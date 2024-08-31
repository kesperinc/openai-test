from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# 정적 파일을 /static 경로로 서빙합니다.
app.mount("templates", StaticFiles(directory="templates"), name="static")

# / 경로에서 index.html을 제공
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join("templates", "index.html")) as f:
        return f.read()
