'''
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE
    priority VARCHAR(10) DEFAULT 'medium', -- low, medium, high
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 );
'''

from pydantic import BaseModel, Field, ValidationError, ConfigDict, EmailStr
from typing import Annotated, Literal
from datetime import datetime, date

# datetime.datetime : YYYY-MM-DD HH:MM:SS
# datetime.date     : YYYY-MM-DD

class TodoBase(BaseModel) :
    title : Annotated[str, Field(max_length=200, description="할 일 제목")]
    description : Annotated[str | None, Field(default=None, description="할 일 상세 설명")]
    priority : Annotated[Literal['low', 'medium', 'high'], Field(default='medium', description="작업의 중요도")]
    due_date : Annotated[date | None, Field(default=None, description="작업 기한")]
    
class TodoCreate(TodoBase) :
    pass

class TodoUpdate(BaseModel) : 
    title : Annotated[str | None, Field(default=None, max_length=200, description="할 일 제목")]
    description : Annotated[str | None, Field(default=None, description="할 일 상세 설명")]
    priority : Annotated[Literal['low', 'medium', 'high'] | None, Field(default=None, description="작업의 중요도")]
    due_date : Annotated[date | None, Field(default=None, description="작업 기한")]
    is_completed : Annotated[bool | None, Field(default=None, description="작업완료여부")]
    
class Todo(TodoBase) : 
    id : int
    user_id : Annotated[int, Field(default=False, description="할 일 생성한 사용자 ID")]
    is_completed : Annotated[bool, Field(description="작업완료여부")]
    created_at : Annotated[datetime, Field(description="할 일 등록 날짜")]
    updated_at : Annotated[datetime, Field(description="할 일 업데이트 날짜")]
    
    model_config = ConfigDict(
        from_attributes=True,
        title = "할 일 정보",
        decription = "API 응답용 할 일 상세 정보 스키마"
    )