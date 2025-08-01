from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import APIRouter, status, Depends, HTTPException, Response
from app.schemas import user as user_schema

from app.database import get_db
from app.services.auth_service import Auth_service

from app import UserAlreadyExistsError, UserDoesNotExist, PasswordDoesNotMatch

# APIRouter 객체 생성
# tags : API 문서에서 엔드포인트를 그룹화하는데 사용
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
    #dependencies=[Depends()]  # 인증할때에 유효 / 데이터가져오려면 def param에 명시해야함
)

auth_service = Auth_service()

@router.post("/sign-up", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def signup(
    user : user_schema.UserCreate, 
    db : AsyncSession = Depends(get_db)) :
    
    print("----------------- Sign-Up Endpoint Start --------------------------")
    try :
        new_user = await auth_service.user_create(db = db, user = user)
        
        await db.commit()         # 변경사항을 DB에 커밋
        # db.refresh(new_user) # DB에 저장된 사용자 정보를 객체에 반영
        
        return new_user
    
    # DB내에서 UNIQUE 컬럼에 동일한 데이터가 있을 경우
    except IntegrityError : 
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용중인 이메일입니다."
        )
    # 나중에 로깅처리
    except SQLAlchemyError : 
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생하였습니다."
        )
    except UserAlreadyExistsError as e :
        # 에러 객체에 담긴 추가 정보를 로깅하거나 활용할 수 있음
        print(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용중인 이메일입니다."
        )

@router.post("/login", response_model=user_schema.Total_Token, status_code=status.HTTP_200_OK)
async def login(
    response : Response, 
    user : user_schema.UserLogin, 
    db : AsyncSession = Depends(get_db)) : 
    
    print("----------------- Login Endpoint Start --------------------------")
    
    try : 
        # 인증 성공 시 Token 정보 저장
        jwt_token = await auth_service.user_login(db = db, user = user)
        
        # refresh token
        response.set_cookie(
            key="refresh_token",  # 쿠키의 이름
            value=jwt_token.get("refresh").get("refresh_token"), # 실제 토큰 값
            httponly=True, # javascript에서 접근 불가(XSS 방지)
            samesite="lax", # CSRF방지를 위한 설정 ('strict' or 'lax')
            #secure=True, # HTTPS환경에서만 쿠키 전송 (배포 시)
            max_age=jwt_token.get("refresh").get("expire_time") # 쿠키만료 시간
        )
        
        # access token
        response.set_cookie(
            key="access_token",  # 쿠키의 이름
            value=jwt_token.get("access").get("access_token"),
            samesite="lax",
            #secure=True,
            max_age=jwt_token.get("access").get("expire_time")
        )
        
        return jwt_token
    
    except UserDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="이메일 또는 패스워드가 일치하지 않습니다."
        )
    except PasswordDoesNotMatch:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 패스워드가 일치하지 않습니다."
        )
     # --- 가장 중요한 수정 부분 ---
    except Exception as e:
        # 예상치 못한 에러가 발생하면, 로그를 남기고 500 에러를 발생시킵니다.
        print(f"예상치 못한 에러가 발생하였습니다: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다. 관리자에게 문의하세요."
        )
    
        