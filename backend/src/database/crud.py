from fastapi import HTTPException
from passlib.context import CryptContext
from pony.orm import commit, IntegrityError, ObjectNotFound, select
from bcrypt import gensalt, hashpw
from typing import Union, Optional, List

from .models import Site_user, Chat_of_interest, Chat, User_of_interest, User
from..schemas.site_user import Site_userInSchema, Site_userOutSchema
from..schemas.user import User
from..schemas.user_of_interest import UserOfInterest
from..schemas.chat import ChatInSchema, ChatOutSchema
from..schemas.chat_of_interest import ChatOfInterest
from..schemas.token import Status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# TODO: Update all models/crud (like site_user models/functions)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- CREATE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
def create_site_user(user: Site_userInSchema) -> Site_userOutSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = Site_user(**user.dict(exclude_unset=True))
        commit()
        return Site_userOutSchema.from_orm(user_obj)
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")


def create_chat_of_interest(site_user_id: int, name: Optional[str]) -> Union[Chat_of_interest, str]:
    try:
        user = Site_user.get(id=site_user_id)
        chat_of_interest = Chat_of_interest(site_user=user, name=name)
        commit()
        return chat_of_interest
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Site user not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_chat(chat: ChatInSchema, site_user: Site_userOutSchema) -> ChatOutSchema:
    try:
        chat = Chat(**chat.dict(exclude_unset=True), site_user=site_user.id)
        commit()
        return chat
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Chat already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_user_of_interest(site_user_id: int, name: Optional[str]) -> Union[User_of_interest, str]:
    try:
        user = Site_user.get(id=site_user_id)
        user_of_interest = User_of_interest(site_user=user, name=name)
        commit()
        return user_of_interest
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Site user not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_user(user_of_interest_id: int, first_name: Optional[str], last_name: Optional[str], username: str,
                phone_number: Optional[str], profilePhoto: Optional[str], interest_status: int) -> Union[User, str]:
    try:
        user_of_interest = User_of_interest.get(id=user_of_interest_id)
        user = User(user_of_interest=user_of_interest, first_name=first_name, last_name=last_name, username=username,
                    phone_number=phone_number, profilePhoto=profilePhoto, interest_status=interest_status)
        commit()
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User of interest not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ----------------------------------------------------- READ ----------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def get_site_user(id: int) -> Site_userOutSchema:
    try:
        user_obj = Site_user[id]
        return Site_userOutSchema.from_orm(user_obj)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_chat_of_interest(id: int) -> Union[ChatOfInterest, str]:
    try:
        chat_of_interest = Chat_of_interest[id]
        return ChatOfInterest(id=chat_of_interest.id, site_user=chat_of_interest.site_user.id,
                              name=chat_of_interest.name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Chat of interest not found")


def get_chat(id: int) -> ChatOutSchema:
    try:
        chat = Chat[id]
        return ChatOutSchema.from_orm(chat)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Chat not found")


def get_all_chats() -> List[ChatOutSchema]:
    try:
        chats = select(chat for chat in Chat)[:]
        return [ChatOutSchema(id=chat.id, title=chat.title, type=chat.type, last_message=chat.last_message,
                              chatPhoto=chat.chatPhoto, interest_status=chat.interest_status,
                              created_at=chat.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                for chat in chats]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user_of_interest(id: int) -> Union[UserOfInterest, str]:
    try:
        user_of_interest = User_of_interest[id]
        return UserOfInterest(id=user_of_interest.id, site_user=user_of_interest.site_user.id,
                              name=user_of_interest.name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="User of interest not found")


def get_user(id: int) -> Union[User, str]:
    try:
        user = User[id]
        return User(id=user.id, user_of_interest=user.user_of_interest.id if user.user_of_interest else None,
                    first_name=user.first_name, last_name=user.last_name, username=user.username,
                    phone_number=user.phone_number, profilePhoto=user.profilePhoto,
                    interest_status=user.interest_status)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="User not found")


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- UPDATE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def update_site_user(id: int, user: Site_userInSchema) -> Site_userOutSchema:
    try:
        user_obj = Site_user[id]
        for key, value in user.dict(exclude_unset=True).items():
            setattr(user_obj, key, value)
        commit()
        return Site_userOutSchema.from_orm(user_obj)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_chat(id: int, title: Optional[str] = None, type: Optional[str] = None, last_message: Optional[str] = None,
                chatPhoto: Optional[str] = None, interest_status: Optional[int] = None) -> Union[Chat, str]:
    try:
        chat = Chat[id]
        if title:
            chat.title = title
        if type:
            chat.type = type
        if last_message:
            chat.last_message = last_message
        if chatPhoto:
            chat.chatPhoto = chatPhoto
        if interest_status is not None:
            chat.interest_status = interest_status
        commit()
        return Chat.from_orm(chat)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Chat not found")


def update_user_of_interest(id: int, name: Optional[str] = None) -> Union[UserOfInterest, str]:
    try:
        user_of_interest = User_of_interest[id]
        if name:
            user_of_interest.name = name
        commit()
        return UserOfInterest.from_orm(user_of_interest)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="User of interest not found")


def update_user(id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                username: Optional[str] = None, phone_number: Optional[str] = None, profilePhoto: Optional[str] = None,
                interest_status: Optional[int] = None) -> Union[User, str]:
    try:
        user = User[id]
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        if phone_number:
            user.phone_number = phone_number
        if profilePhoto:
            user.profilePhoto = profilePhoto
        if interest_status is not None:
            user.interest_status = interest_status
        commit()
        return User.from_orm(user)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="User not found")


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- DELETE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def delete_site_user(user_id: int, current_user: Site_userOutSchema) -> Status:
    try:
        db_user = Site_user[user_id]
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        db_user.delete()
        commit()
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


def delete_chat_of_interest(id: int) -> Union[str, None]:
    try:
        chat_of_interest = Chat_of_interest[id]
        chat_of_interest.delete()
        commit()
        return "Chat of interest deleted"
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Chat of interest not found")


def delete_chat(id: int) -> Union[str, None]:
    try:
        chat = Chat[id]
        chat.delete()
        commit()
        return "Chat deleted"
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Chat not found")


def delete_user_of_interest(id: int) -> Union[str, None]:
    try:
        user_of_interest = User_of_interest[id]
        user_of_interest.delete()
        commit()
        return "User of interest deleted"
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="User of interest not found")


def delete_user(id: int) -> Union[str, None]:
    try:
        user = User[id]
        user.delete()
        commit()
        return "User deleted"
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="User not found")
