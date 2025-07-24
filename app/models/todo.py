from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DATE, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    priority = Column(String, default='medium')
    due_date = Column(DATE)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    
    # back_populates는 Users 모델의 todos 속성과 연결됨을 의미
    users = relationship("Users", back_populates="todos")
    
    # 3. 기능(메소드) 구현
    def __repr__(self):
        return f"<User(id={self.id}, title='{self.title}')>"