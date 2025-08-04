from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth
import sys

app = FastAPI()

app.include_router(auth.router)

# --- 디버깅 코드 추가 ---
print("="*50, file=sys.stderr)
print(f"CORS Origins Loaded in main.py: {settings.cors_origins}", file=sys.stderr)
print(f"Type of CORS Origins: {type(settings.cors_origins)}", file=sys.stderr)
print("="*50, file=sys.stderr)
# -------------------------
   
app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins, # origins 리스트에 있는 출처에서의 요청을 허용한다
    allow_credentials=True, # 쿠키, 인증 헤더 등을 포함한 요청을 허용
    allow_methods=["*"],    # 모든 HTTP 메소드(get, post, put, delete 등)를 허옹
    allow_headers=["*"],    # 모든 요청 헤더를 허용
)

@app.get("/")
def home() :
    return {"home" : "home!!!"}

