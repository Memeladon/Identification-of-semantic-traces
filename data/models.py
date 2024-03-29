from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    status: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    chats: list

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    chat: str
    text: str
    author_id: int
    timestamp: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    author: Author

    class Config:
        orm_mode = True
