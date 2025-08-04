from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas import user as user_schema
from app.models import user as user_model
from app.core.security import pwd_hashing, verify_password, create_access_token, create_refresh_token
from app import UserAlreadyExistsError, UserDoesNotExist, PasswordDoesNotMatch

# 인증 비즈니스 로직 구현
class Auth_service() :
    
    '''
        새로운 사용자를 생성하는 서비스 함수
        - 이메일 중복 여부 확인
        - 비밀번호 해싱 후 DB에 저장
    '''
    async def user_create(self, db : AsyncSession, user : user_schema.UserCreate) -> user_model.Users :
        
        # 1. 이메일 중복 여부 확인
        # DB에서 요청된 이메일과 일치하는 사용자가 있는지 조회
        query = select(user_model.Users).filter(user_model.Users.email == user.email)
        result = await db.execute(query)
        db_user = result.scalar()
        #db_user = result.scalars().first()
        
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
        
        # 4. DB 세션에 사용자 객체를 추가
        db.add(db_user)     
        await db.flush() # flush를 사용하여 db_user 객체에 id와 같은 기본 정보를 채웁니다.
        await db.refresh(db_user)
        
        return db_user
    
    '''
        로그인 함수
        - 이메일 검증 & 패스워드 검증
        - access, refresh token 발급
    '''
    async def user_login(self, db : AsyncSession, user : user_schema.UserLogin) -> list[dict] :
        # 1. 가입된 회원인지 확인
        query = select(user_model.Users).filter(user_model.Users.email == user.email)
        result = await db.execute(query)
        db_user = result.scalar()
        
        if db_user is None : 
            # 이메일이 일치하지 않을 경우
            raise UserDoesNotExist()
        
        # 2. 패스워드 검증
        decode_password = verify_password(user.password, db_user.hashed_password)
        
        # 2-1. 성공시 access_token + refresh_token 발급
        if decode_password :
            access_token = create_access_token(db_user.email, db_user.username)
            refresh_token = create_refresh_token(db_user.email, db_user.username)
            return {
                "access" : access_token, 
                "refresh" : refresh_token
            }
        else :
            # 패스워드가 일치하지 않을 경우
            raise PasswordDoesNotMatch()
    
    async def get_user_by_email(self, db: AsyncSession, email : str) -> user_schema.User :
        query = select(user_model.Users).filter(user_model.Users.email == email)
        result = await db.execute(query)
        user = result.scalar()
        
        if user == None :
            raise UserDoesNotExist()
        
        return user
    
if __name__ == "__main__" : 
    pass

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