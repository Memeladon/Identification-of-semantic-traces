from pydantic import BaseModel
from typing import List, Optional


class ChatOfInterest(BaseModel):
    id: int
    site_user: int
    name: Optional[str] = None
    chats: List[int] = []
