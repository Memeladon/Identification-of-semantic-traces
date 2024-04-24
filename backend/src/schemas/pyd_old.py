from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SiteUserBase(BaseModel):
    username: str = Field(..., max_length=32)
    password: str
    created_at: datetime
    modified_at: Optional[datetime]


class SiteUserCreate(SiteUserBase):
    pass


class SiteUser(SiteUserBase):
    id: int
    user_of_interests: List['UserOfInterest'] = []
    chat_of_interests: List['ChatOfInterest'] = []

    class Config:
        orm_mode = True


class ChatOfInterestBase(BaseModel):
    name: Optional[str]


class ChatOfInterestCreate(ChatOfInterestBase):
    pass


class ChatOfInterest(ChatOfInterestBase):
    id: int
    site_user: SiteUser
    chats: List['Chat'] = []

    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    title: str
    type: str
    last_message: Optional[str]
    chatPhoto: Optional[str]
    interest_status: int


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    chat_of_interest: Optional[ChatOfInterest]

    class Config:
        orm_mode = True


class UserOfInterestBase(BaseModel):
    name: Optional[str]


class UserOfInterestCreate(UserOfInterestBase):
    pass


class UserOfInterest(UserOfInterestBase):
    id: int
    site_user: SiteUser
    users: List['User'] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    phone_number: Optional[str]
    profilePhoto: Optional[str]
    interest_status: int


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    user_of_interest: Optional[UserOfInterest]

    class Config:
        orm_mode = True
