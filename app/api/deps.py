# JWT 토큰 검증 && 현재 사용자 정보 가져오는 의존성함수 구현
from fastapi import Depends, Cookie, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user as user_schema
from app.core.security import decode_access_token
from app.database import get_db
from app.services.auth_service import Auth_service
from app import UserDoesNotExist

import jwt

# JWT 토큰을 검증하고 현재 사용자 정보를 가져오는 의존성 함수
async def get_current_user(
    db : AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(None)
    ) -> user_schema.User :
    print(f"access_token : {access_token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    if access_token is None : # is : 참조, == : 값
        raise credentials_exception
    
    # 액세스 토큰 디코딩
    try :
        payload = decode_access_token(access_token)
        
        user_email : str | None =  payload.get("email")
        if user_email is None :
            raise credentials_exception
        
        auth_service = Auth_service()
        user = await auth_service.get_user_by_email(db, user_email)
        
        return user
    
    # jwt 만료 에러
    except jwt.ExpiredSignatureError : 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다.",
            headers={"WWW-Authenticate" : "Bearer"},
        )
        
    # 만료 에러 외 모든 JWT에러
    except jwt.InvalidTokenError :
        raise credentials_exception
    
    except UserDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 이메일입니다."
        )
    except SQLAlchemyError : 
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생하였습니다."
        )


# async def는 'I/O 작업'을 할 때 사용합니다.
'''
I/O (Input/Output) 작업이란?
   * 네트워크 요청: 다른 서버의 API를 호출하고 응답을 기다리는 것 (예: DB 조회, 외부 API 호출)
   * 파일 시스템 접근: 디스크에서 파일을 읽거나 쓰는 것
   * 데이터베이스 쿼리: 데이터베이스에 쿼리를 보내고 결과를 기다리는 것이
'''

# 의존성 함수
'''
    - 일반 함수 (경로 작동 함수): API의 최종 목적지. 핵심 기능을 수행.
    - 의존성 함수: 최종 목적지에 도달하기 전에 거쳐야 하는 검문소. 필요한 자원(DB 세션)을 준비하거나, 통과 자격(인증)을 확인하는 역할을 합니다
      의존성 함수는 왜 사용할까요?


   1. 코드 중복 제거 (Don't Repeat Yourself)
       - 여러 API 엔드포인트에서 공통적으로 사용되는 로직(예: 현재 로그인된 사용자 정보 가져오기)을 하나의 함수로 만들어 재사용할 수 있습니다.


   2. 관심사 분리 (Separation of Concerns)
       - 비즈니스 로직과 인증/인가, 데이터베이스 연결 같은 부가적인 로직을 분리하여 코드를 더 깔끔하고 유지보수하기 쉽게 만듭니다.


   3. 쉬운 테스트
       - 의존성을 사용하는 함수를 테스트할 때, 실제 의존성 대신 테스트용 가짜(mock) 의존성을 주입하여 단위 테스트를 더 쉽게 만들 수 있습니다
'''
