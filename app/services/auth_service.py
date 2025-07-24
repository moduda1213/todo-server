from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas import user as user_schema
from app.models import user as user_model
from app.core.security import pwd_hashing, verify_password
from app import UserAlreadyExistsError

# 인증 비즈니스 로직 구현
class Auth_service() :
    
    '''
        새로운 사용자를 생성하는 서비스 함수
        - 이메일 중복 여부 확인
        - 비밀번호 해싱 후 DB에 저장
    '''
    def user_create(self, db : Session, user : user_schema.UserCreate) :
        
        # 1. 이메일 중복 여부 확인
        # DB에서 요청된 이메일과 일치하는 사용자가 있는지 조회
        db_user = db.query(user_model.Users).filter(user_model.Users.email == user.email).first()
        
        if db_user :
            raise UserAlreadyExistsError(username=user.username)
        
        
        # 2. 비밀번호 해싱 
        hashed_password = pwd_hashing(user.password)
        
        # 3. User 모델 객체 생성
        # Pydantic 스키마(user)에서 받은 정보와 해싱된 비밀번호로 SQLAlchemy 모델(db_user) 객체를 만듭니다.
        db_user = user_model.Users(
            username = user.username,
            email = user.email,
            hashed_password = hashed_password
        )
        
        # 4. DB에 추가 및 저장
        db.add(db_user)     # DB 세션에 사용자 객체를 추가
        
        return db_user
        
    def user_login(self, db : Session, user : user_schema.UserLogin) :
        
        # 1. 가입된 회원인지 확인
        db_user = db.query(user_model.Users).filter(user_model.Users.email == user.email).first()
        print(f"{db_user}")
        if db_user : 
            pass
        else :
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail = "이메일 또는 패스워드가 일치하지 않습니다."
            )
            
        # 2. 패스워드 검증
        decode_password = verify_password(user.password, db_user.hashed_password)
        if decode_password :
            return db_user
        else :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 패스워드가 일치하지 않습니다."
            )
            
        
    
if __name__ == "__main__" : 
    '''
            서비스 계층 : 데이터 유효성 검사, 계산, DB와 상호작용하는 비즈니스로직을 처리하는 곳
            => HTTP에 대해서는 처리하는 곳이 아니기 때문에 
            
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용중인 이메일입니다."
            )
            ---------------------
             raise UserAlreadyExistsError(username=user.username) 처리
        '''
    pass