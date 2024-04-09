from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    user_of_interest: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    phone_number: Optional[str] = None
    profilePhoto: Optional[str] = None
    interest_status: int
