from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .schemas.user import UserLogin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins, # origins 리스트에 있는 출처에서의 요청을 허용한다
    allow_credentials=True, # 쿠키, 인증 헤더 등을 포함한 요청을 허용
    allow_methods=["*"],    # 모든 HTTP 메소드(get, post, put, delete 등)를 허옹
    allow_headers=["*"],     # 모든 요청 헤더를 허용
)

@app.get("/")
def home() :
    return {"home" : "home!!!"}

@app.post("/login/")
async def login(userInfo : UserLogin) :
    return userInfo
