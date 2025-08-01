import bcrypt
import jwt
import time
from .config import settings
from datetime import datetime, timedelta
'''
    bcrypt는 문자열이 아닌 바이트 데이터를 받아 연산합니다
        => 암호화 알고리즘은 '문자(text)'라는 추상적인 개념을 직접 다루지 못하고, 
            '바이트(bytes)'라는 구체적인 데이터 단위를 다루기 때문
'''
_algorithm = settings.algorithm
_secret_key = settings.secret_key
_access_expire_time = settings.access_expire_time
_refresh_expire_time = settings.refresh_expire_time

# 비밀번호 해싱 (bcrypt)
# bcrypt.haspw( bytes, bytes )
def pwd_hashing(pwd : str) -> bytes :
    password = pwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password, salt)
    return hashed_pwd

# 비밀번호 검증
def verify_password(pwd : str, hashed_pwd : bytes) -> bool :
    password = pwd.encode('utf-8')
    result = bcrypt.checkpw(password, hashed_pwd) 
    return result
    
# ACCESS_JWT 토큰 생성 
def create_access_token(email : str, username : str) -> dict: 
    
    expiration_time = datetime.now() + timedelta(seconds=_access_expire_time)
    expiration_timestamp = int(time.mktime(expiration_time.timetuple()))
    payload = {
        "email" : email,
        "username" : username,
        "exp" : expiration_timestamp
    }
    '''
        HS256 사용 이유
        1. 널리 사용되고 있음
        2. 단일 서버에서 JWT를 발급하고 검증하는 경우, HS256과 같은 대칭 키 알고리즘을 사용해도 충분
    '''
    
    token = jwt.encode(payload, _secret_key, _algorithm)
    
    token_info = {
        "access_token": token,
        "token_type": "bearer",
        "expire_time": _access_expire_time
    }
    return token_info
    

# ACCESS_JWT 디코딩 함수 구현
def decode_access_token(token : str) -> dict : 
    try :
        decode_payload = jwt.decode(token, _secret_key, algorithms=_algorithm)
    except :
        decode_payload = None
        
    return decode_payload


# REFRESH_TOKEN 생성
def create_refresh_token(email:str, username:str) -> dict :
    expiration_time = datetime.now() + timedelta(seconds=_refresh_expire_time)
    expiration_timestamp = int(time.mktime(expiration_time.timetuple()))
    payload = {
        "email" : email,
        "username" : username,
        "exp" : expiration_timestamp
    }
    token = jwt.encode(payload, _secret_key, _algorithm)
    token_info = {
        "refresh_token": token,
        "expire_time": _refresh_expire_time
    }
    return token_info

if __name__ == '__main__' : 
    test_pwd = "super password"
    test_hashed_pwd = pwd_hashing(test_pwd)
    print(test_hashed_pwd)
    print(verify_password(test_pwd, test_hashed_pwd))
    
    print(f"datetime : {datetime}")
    print(f"datetime now  : {datetime.now()}") # 2025-07-19 10:37:38.046425
    print(f"timedelta : {timedelta(minutes=1)}") # 0:01:00
    print(f"timetuple : {(datetime.now() + timedelta(minutes=1)).timetuple()}") # time.struct_time(tm_year=2025, tm_mon=7, tm_mday=19, tm_hour=10, tm_min=38, tm_sec=38, tm_wday=5, tm_yday=200, tm_isdst=-1)
    print(f"time.mktime : {int(time.mktime((datetime.now() + timedelta(minutes=1)).timetuple()))}") # datetime : 1752889118
    
    test_token = create_access_token("test", "testtest")
    print(f"test_access_token : {test_token} , {test_token.__class__}")
    dec_test_token = decode_access_token(test_token.get("access_token"))
    print(f"test_decode_access_token : {dec_test_token} , {dec_test_token.__class__}")
    # {'email': 'test', 'username': 'testtest', 'exp': 1754025630}
    test_token = create_refresh_token("test", "testtest")
    print(f"test_decode_refresh_token : {test_token} , {test_token.__class__}")
    
    
'''
    로그인 ( 엑세스토큰(수명 짧음) / 리프레시 토큰(수명 김) ) 
        ->  api요청 *(엑세스토큰)
            -> 엑세스토큰 만료 시 리프레시 토큰 검증 
                -> 검증 성공 시 새로운 엑세스 토큰 + 리프레시 토큰 재발금 (기존 리프레시토큰 무효화)
                    -> 다시 api요청
'''

