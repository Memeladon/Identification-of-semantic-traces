from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Для создания новых чатов
class ChatInSchema(BaseModel):
    site_user: int
    title: str
    type: str
    last_message: Optional[str] = None
    chatPhoto: Optional[str] = None
    interest_status: int


# Для возврата информации о чате
class ChatOutSchema(BaseModel):
    id: int
    title: str
    type: str
    last_message: Optional[str] = None
    chatPhoto: Optional[str] = None
    interest_status: int
    created_at: str


# Для внутренней проверки чатов
class ChatDatabaseSchema(BaseModel):
    id: int
    title: str
    type: str
    last_message: Optional[str] = None
    chatPhoto: Optional[str] = None
    interest_status: int
    created_at: str
    modified_at: Optional[str] = None


# Общая модель для использования в приложении
class ChatModel(BaseModel):
    id: int
    site_user: int
    chat_of_interest: Optional[int] = None
    title: str
    type: str
    last_message: Optional[str] = None
    chatPhoto: Optional[str] = None
    interest_status: int
    created_at: datetime
    modified_at: Optional[datetime] = None


# Для обновления информации о чате
class UpdateChat(BaseModel):
    chat_of_interest: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    last_message: Optional[str] = None
    chatPhoto: Optional[str] = None
    interest_status: Optional[int] = None
