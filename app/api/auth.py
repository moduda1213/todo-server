from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas import user as user_schema

from app.database import get_db
from app.services.auth_service import Auth_service

from app import UserAlreadyExistsError

# APIRouter 객체 생성
# tags : API 문서에서 엔드포인트를 그룹화하는데 사용
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_service = Auth_service()

@router.post("/sign-up", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def signup(user : user_schema.UserCreate, db : Session = Depends(get_db)) :
    print("----------------- Sign-Up Endpoint Start --------------------------")
    try :
        new_user = auth_service.user_create(db = db, user = user)
        
        db.commit()         # 변경사항을 DB에 커밋
        db.refresh(new_user) # DB에 저장된 사용자 정보를 객체에 반영
        print("----------------- Sign-Up Endpoint End --------------------------")
        return new_user
    
    # DB내에서 UNIQUE 컬럼에 동일한 데이터가 있을 경우
    except IntegrityError : 
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용중인 이메일입니다."
        )
    # 나중에 로깅처리
    except SQLAlchemyError : 
        db.rollback()
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

@router.post("/login", response_model=user_schema.User, status_code=status.HTTP_200_OK)
def login(user : user_schema.UserLogin, db : Session = Depends(get_db)) : 
    print("----------------- Login Endpoint Start --------------------------")
    try : 
        verified_user = auth_service.user_login(db = db, user = user)
    except HTTPException as e :
        raise e
    
    print("----------------- Login Endpoint End --------------------------")
    return verified_user