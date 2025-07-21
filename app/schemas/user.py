from pydantic import BaseModel, Field, ValidationError, ConfigDict, EmailStr
from typing import Annotated
from datetime import datetime

class UserBase(BaseModel) : 
    email : Annotated[EmailStr, Field(max_length=100, description="사용자 이메일")]
    username : Annotated[str, Field(max_length=50, description="사용자 이름")]
    
class UserCreate(UserBase) :
    password : Annotated[str, Field(max_length=255, description="사용자 패스워드")]

class User(UserBase):
    id : int
    is_active : Annotated[bool, Field(description="활동 계정")]
    created_at : Annotated[datetime, Field(description="유저 가입 날짜")]
    updated_at : Annotated[datetime, Field(description="유저 정보 업데이트 날짜")]
    
    model_config = ConfigDict(
        # orm_mode => from_attributes
        from_attributes=True,
        title = "사용자 정보",
        description = "API 응답용 스키마",
        json_schema_extra={
            "example" : {
                "id": 1,
                "username": "gim",
                "email": "gim@example.com",
                "is_active": True,
                "created_at": "2025-07-12T10:00:00Z",
                "updated_at": "2025-07-12T11:30:00Z"
            }
        }       
    )
 
class UserInDB(UserBase) : 
    id : int
    password : Annotated[str, Field(max_length=255, description="사용자 패스워드")]
    is_active : Annotated[bool, Field(description="활동 계정")]
    created_at : Annotated[datetime, Field(description="유저 가입 날짜")]
    updated_at : Annotated[datetime, Field(description="유저 정보 업데이트 날짜")]

    model_config = ConfigDict(
        # orm_mode => from_attributes
        title = "사용자 정보",
        description = "내부 로직용 API",
        from_attributes=True,
        json_schema_extra = {
            "example" : {
                "id": 1,
                "username": "gim",
                "password" : "hashed_password",
                "email": "gim@example.com",
                "is_active": True,
                "created_at": "2025-07-12T10:00:00Z",
                "updated_at": "2025-07-12T11:30:00Z"
            }
        }       
    )
    
'''
TokenData 스키마는 JWT(JSON Web Token) 액세스 토큰 안에 저장되는 데이터의       
  형식을 정의하는 역할을 합니다.

  조금 더 자세히 설명해 드릴게요.


   1. 로그인 성공 및 토큰 생성:
       * 사용자가 아이디와 비밀번호로 로그인을 성공하면, 서버는
         access_token을 생성해서 Token 스키마에 담아 응답으로 보내줍니다.
       * 이 access_token은 단순한 문자열이 아니라, 내부에 정보를 담고 있는
         암호화된 토큰(JWT)입니다.
       * 서버는 이 토큰을 생성할 때, 토큰의 소유자를 식별할 수 있는
         정보(예: 사용자의 username)를 토큰 안에 넣어둡니다.


   2. 인증이 필요한 API 요청:
       * 사용자는 로그인 후 access_token을 가지고, 인증이 필요한 다른
         API(예: '내 할일 목록 보기')를 요청합니다. 이때 보통 HTTP Header에       
         토큰을 담아 보냅니다.
       * 서버는 요청을 받으면 헤더에서 access_token을 꺼내 해독(decode)하여       
         그 안에 어떤 정보가 들어있는지 확인합니다.


   3. `TokenData`의 역할:
       * 바로 이 단계에서 TokenData가 사용됩니다. 서버가 토큰을 해독했을 때
         나오는 데이터가 TokenData 스키마에 정의된 형식과 일치하는지
         검증하는 것입니다.
       * TokenData(username: str | None = None)는 "토큰을 해독하면
         username이라는 필드가 있고, 그 값은 문자열(str)이어야 한다"라는
         규칙을 정의한 것입니다.
       * 이 검증을 통과해야만 서버는 "아, 이 토큰은 유효하고, 소유자는
         'gemini'구나"라고 신뢰하고 요청된 작업을 처리해 줄 수 있습니다.

  요약:


   * Token: 클라이언트에게 전달되는 최종 응답의 전체적인 구조 (로그인 시).
   * TokenData: 그 응답 안의 access_token 내부에 숨겨진 데이터의 구조.


  따라서 TokenData는 서버가 토큰의 유효성을 검사하고 토큰 소유자를
  식별하기 위한 내부용 데이터 검증 모델이라고 생각하시면 됩니다.
'''
class UserLogin(BaseModel):
    email: Annotated[str, Field(max_length=50, description="사용자 이름")]
    password: Annotated[str, Field(max_length=255, description="사용자 패스워드")]

    model_config = ConfigDict(
        title="사용자 로그인",
        description="로그인 요청 스키마",
        json_schema_extra={
            "example": {
                "email": "gim",
                "password": "gimpassword" 
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

    model_config = ConfigDict(
        title="인증 토큰",
        description="API 응답용 토큰 스키마",
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }
    )


class TokenData(BaseModel):
    username: str | None = None
    email : str | None = None


if __name__ == "__main__" : 
    import json
    try:
        user_data = {
            "id": 1,
            "username": "gim",
            "email": "gim@example.com",
            "is_active": True,
            "created_at": "2025-07-12T10:00:00Z",
            "updated_at": "2025-07-12T11:30:00Z"
        }
        user = User.model_validate(user_data)
        # model_dump_json() 테스트 -> 인스턴스의 '데이터'를 출력
        print("--- 1. model_dump_json() 결과 (실제 데이터) ---")
        print(user.model_dump_json(indent=2)) # indent => 들여쓰기
        
        # model_json_schema() 테스트 -> 클래스의 '설계도'를 출력
        print("--- 2. model_json_schema() 결과 (구조와 규칙) ---")
        print("\n" + "="*50 + "\n") # 구분선
        schema_dict = User.model_json_schema()
        print(json.dumps(schema_dict, indent=2, ensure_ascii=False))
        '''
            ensure_ascii=False를 안하면 "title": "사용자 정보" => "\uc0ac\uc6a9\uc790 \uc815\ubcf4" 아스키 코드로 출력됨
        '''
    except ValidationError as e :
        print("--- Validation Error ---")
        print(e)