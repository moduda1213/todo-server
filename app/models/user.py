# SQLAlchemy 모델 클래스 정의
# https://moduda1213.tistory.com/18

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, LargeBinary
from sqlalchemy.orm import relationship
from app.database import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    
    # back_populates는 Todos 모델의 users 속성과 연결됨을 의미
    todos = relationship("Todos", back_populates="users")
    
    # 3. 기능(메소드) 구현
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    def verify_password(self, plain_password):
        # 실제로는 여기에 비밀번호 해시 검증 로직이 들어갑니다.
        return self.hashed_password == plain_password + "_hashed" # 예시
