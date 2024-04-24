from pydantic import BaseModel
from typing import List, Optional


class UserOfInterest(BaseModel):
    id: int
    site_user: int
    name: Optional[str] = None
    users: List[int] = []
