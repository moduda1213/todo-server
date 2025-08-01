from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

# Refresh_Token 모델
class RefreshToken(Base) :
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String, index=True, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_revoked = Column(Boolean, default=False) # 토큰 무효화 여부

    users = relationship("Users", back_populates="refresh_tokens")
    
    def __repr__(self) :
        return f"[refresh_token : {self.refresh_token} , is_revoked : {self.is_revoked}]"