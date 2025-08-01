# **1.3: 환경 설정 관리**
# .env 파일에 환경변수 로드하도록 설정

from pydantic import Field, AliasChoices, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus
from typing import List
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / '.env'

class Settings(BaseSettings) :
    db_user: str = Field(validation_alias=AliasChoices("DEV_DB_USER","PRD_DB_URL"))
    db_password: str = Field(alias="DEV_DB_PASSWORD")
    db_host: str = Field(alias="DEV_DB_HOST")
    db_name: str = Field(alias="DEV_DB_NAME")
    
    secret_key : str = Field(alias="JWT_SECRET_KEY")
    algorithm : str = Field(alias="ALGORITHM")
    access_expire_time : int = Field(alias="ACCESS_TOKEN_EXPIRE_SECONDS")
    refresh_expire_time : int = Field(alias="REFRESH_TOKEN_EXPIRE_SECONDS")
    
    cors_origins : List[str] = Field(alias="DEV_CORS_ORIGINS")
    
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file = env_path,
        env_file_encoding='utf-8',
        extra= 'allow'
    )
    
    @property
    def db_url(self) -> str :
        encoded_password = quote_plus(self.db_password)
        return f"postgresql+asyncpg://{self.db_user}:{encoded_password}@{self.db_host}/{self.db_name}"
        # return f"postgresql+psycopg2://{self.db_user}:{encoded_password}@{self.db_host}/{self.db_name}" psycopg2 : 동기
    

settings = Settings()
    
if __name__ == "__main__" :
    try:
        print()
        print(settings.db_url)
    except ValidationError as exc:
        print(repr(exc))

'''
    처음 동작했을 때   
    env_file path 설정을 위해 최상위 폴더에 .env와 core폴더에 .env파일을 만들고 TEST = > "missing" 출력
    최상위 .env const key = value로 잘못 기입된 부분 수정 => key=value
    다시 진행 => 'extra_forbidden' => BaseSetting에 작성한 feild와 .env field가 일치하지 않아서 error
    DB_URL을 테스트하기 위해 JWT_SECRET_KEY를 작성하지 않은 것이 ERROR를 유발한 것으로 보임
    
    env_file의 path는 최상위 폴더부터 시작함을 알았고
    불러올 환경변수 field를 빠짐없이 기입해야 한다는 것을 숙지 또는 extra= 'allow'|'ignore'로 넘어갈수 있음
    
'''
    
