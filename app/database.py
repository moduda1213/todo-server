'''
`database.py`는 데이터베이스 연결을 위한 설정을 중앙에서 관리하고,  
   애플리케이션의 다른 부분들이 필요할 때마다 표준화된 방법(주로 의존성 
  주입)으로 데이터베이스 세션을 빌려 쓰고 반납할 수 있도록 해주는 공장(Factory)   
  같은 역할을 합니다.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 데이터베이스 엔진 생성
engine = create_engine(settings.db_url)

# 데이터베이스 세션 생성을 위한 SessionLocal 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델이 상속받을 Base 클래스 생성
Base = declarative_base()

# get_db로 만든 이유 https://moduda1213.tistory.com/16
def get_db():
    db = SessionLocal() # 새로운 세션 생성
    try:
        yield db # 세션을 라우트 함수에 제공
    finally:
        db.close() # 요청 처리 끝나면 세션 닫기
    
    

if __name__ == "__main__" :
    print("데이터베이스 연결 테스트 시작...")
    print(f"데이터베이스 URL : {settings.db_url}")
    try:
        # with engine.connect() as connection: # SQLAlchemy 2.0 style
        session = engine.connect()
        print("✅ 데이터베이스 연결 성공!" )
        session.close()
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패:  {e}")
        