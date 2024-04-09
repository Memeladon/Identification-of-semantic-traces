from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# для создания новых пользователей
class Site_userInSchema(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None


# для возврата информации о пользователе
class Site_userOutSchema(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    created_at: str


# для внутренней проверки пользователей
class Site_userDatabaseSchema(BaseModel):
    id: int
    username: str
    password: str
    full_name: Optional[str] = None
    created_at: str
    modified_at: Optional[str] = None


class SiteUser(BaseModel):
    id: int
    user_of_interests: List[int] = []
    chat_of_interests: List[int] = []
    username: str
    full_name: Optional[str] = None
    password: str
    created_at: datetime
    modified_at: Optional[datetime] = None
