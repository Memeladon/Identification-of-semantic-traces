from pydantic import BaseModel
from typing import Optional


class Chat(BaseModel):
    id: int
    chat_of_interest: Optional[int] = None
    title: str
    type: str
    last_message: Optional[str] = None
    chatPhoto: Optional[str] = None
    interest_status: int
