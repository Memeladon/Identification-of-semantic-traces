from pony.orm import commit, IntegrityError, ObjectNotFound
from bcrypt import gensalt, hashpw
from typing import Union, Optional

from .models import Site_user, Chat_of_interest, Chat, User_of_interest, User
from .schemas.site_user import Site_userInSchema, Site_userOutSchema
from .schemas.user import User
from .schemas.user_of_interest import UserOfInterest
from .schemas.chat import Chat
from .schemas.chat_of_interest import ChatOfInterest


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- CREATE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
def create_site_user(username: str, full_name: Optional[str], password: str) -> Union[Site_user, str]:
    try:
        # Валидация входных данных с помощью Pydantic модели
        user_data = Site_userInSchema(username=username, full_name=full_name, password=password)
        # Хеширование пароля
        hashed_password = hashpw(user_data.password.encode(), gensalt())
        # Создание нового пользователя с валидированными данными
        user = Site_user(username=user_data.username, full_name=user_data.full_name, password=hashed_password)
        commit()
        return user
    except IntegrityError:
        return "Username already exists"
    except Exception as e:
        return f"Error creating user: {e}"


def create_chat_of_interest(site_user_id: int, name: Optional[str]) -> Union[Chat_of_interest, str]:
    try:
        user = Site_user.get(id=site_user_id)
        chat_of_interest = Chat_of_interest(site_user=user, name=name)
        commit()
        return chat_of_interest
    except IntegrityError:
        return "Site user not found"
    except Exception as e:
        return f"Error creating chat of interest: {e}"


def create_chat(chat_of_interest_id: int, title: str, type: str, last_message: Optional[str],
                chatPhoto: Optional[str], interest_status: int) -> Union[Chat, str]:
    try:
        chat_of_interest = Chat_of_interest.get(id=chat_of_interest_id)
        chat = Chat(chat_of_interest=chat_of_interest, title=title, type=type, last_message=last_message,
                    chatPhoto=chatPhoto, interest_status=interest_status)
        commit()
        return chat
    except IntegrityError:
        return "Chat of interest not found"
    except Exception as e:
        return f"Error creating chat: {e}"


def create_user_of_interest(site_user_id: int, name: Optional[str]) -> Union[User_of_interest, str]:
    try:
        user = Site_user.get(id=site_user_id)
        user_of_interest = User_of_interest(site_user=user, name=name)
        commit()
        return user_of_interest
    except IntegrityError:
        return "Site user not found"
    except Exception as e:
        return f"Error creating user of interest: {e}"


def create_user(user_of_interest_id: int, first_name: Optional[str], last_name: Optional[str], username: str,
                phone_number: Optional[str], profilePhoto: Optional[str], interest_status: int) -> Union[User, str]:
    try:
        user_of_interest = User_of_interest.get(id=user_of_interest_id)
        user = User(user_of_interest=user_of_interest, first_name=first_name, last_name=last_name, username=username,
                    phone_number=phone_number, profilePhoto=profilePhoto, interest_status=interest_status)
        commit()
        return user
    except IntegrityError:
        return "User of interest not found"
    except Exception as e:
        return f"Error creating user: {e}"


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ----------------------------------------------------- READ ----------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def get_site_user(id: int) -> Union[Site_userOutSchema, str]:
    try:
        user = Site_user.get(id=id)
        return Site_userOutSchema(id=user.id, username=user.username, full_name=user.full_name,
                                  created_at=user.created_at.isoformat())
    except ObjectNotFound:
        return "User not found"


def get_chat_of_interest(id: int) -> Union[ChatOfInterest, str]:
    try:
        chat_of_interest = Chat_of_interest.get(id=id)
        return ChatOfInterest(id=chat_of_interest.id, site_user=chat_of_interest.site_user.id,
                              name=chat_of_interest.name)
    except ObjectNotFound:
        return "Chat of interest not found"


def get_chat(id: int) -> Union[Chat, str]:
    try:
        chat = Chat.get(id=id)
        return Chat(id=chat.id, chat_of_interest=chat.chat_of_interest.id if chat.chat_of_interest else None,
                    title=chat.title, type=chat.type, last_message=chat.last_message, chatPhoto=chat.chatPhoto,
                    interest_status=chat.interest_status)
    except ObjectNotFound:
        return "Chat not found"


def get_user_of_interest(id: int) -> Union[UserOfInterest, str]:
    try:
        user_of_interest = User_of_interest.get(id=id)
        return UserOfInterest(id=user_of_interest.id, site_user=user_of_interest.site_user.id,
                              name=user_of_interest.name)
    except ObjectNotFound:
        return "User of interest not found"


def get_user(id: int) -> Union[User, str]:
    try:
        user = User.get(id=id)
        return User(id=user.id, user_of_interest=user.user_of_interest.id if user.user_of_interest else None,
                    first_name=user.first_name, last_name=user.last_name, username=user.username,
                    phone_number=user.phone_number, profilePhoto=user.profilePhoto,
                    interest_status=user.interest_status)
    except ObjectNotFound:
        return "User not found"


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- UPDATE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def update_site_user(id: int, username: Optional[str] = None, full_name: Optional[str] = None,
                     password: Optional[str] = None) -> Union[Site_user, str]:
    try:
        user = Site_user.get(id=id)
        if username:
            user.username = username
        if full_name:
            user.full_name = full_name
        if password:
            user.password = password
        commit()
        return user
    except ObjectNotFound:
        return "User not found"


def update_chat_of_interest(id: int, name: Optional[str] = None) -> Union[ChatOfInterest, str]:
    try:
        chat_of_interest = Chat_of_interest.get(id=id)
        if name:
            chat_of_interest.name = name
        commit()
        return chat_of_interest
    except ObjectNotFound:
        return "Chat of interest not found"


def update_chat(id: int, title: Optional[str] = None, type: Optional[str] = None, last_message: Optional[str] = None,
                chatPhoto: Optional[str] = None, interest_status: Optional[int] = None) -> Union[Chat, str]:
    try:
        chat = Chat.get(id=id)
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
        return chat
    except ObjectNotFound:
        return "Chat not found"


def update_user_of_interest(id: int, name: Optional[str] = None) -> Union[UserOfInterest, str]:
    try:
        user_of_interest = User_of_interest.get(id=id)
        if name:
            user_of_interest.name = name
        commit()
        return user_of_interest
    except ObjectNotFound:
        return "User of interest not found"


def update_user(id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                username: Optional[str] = None, phone_number: Optional[str] = None, profilePhoto: Optional[str] = None,
                interest_status: Optional[int] = None) -> Union[User, str]:
    try:
        user = User.get(id=id)
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
        return user
    except ObjectNotFound:
        return "User not found"


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- DELETE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def delete_site_user(id: int) -> Union[str, None]:
    try:
        user = Site_user.get(id=id)
        user.delete()
        commit()
        return "User deleted"
    except ObjectNotFound:
        return "User not found"


def delete_chat_of_interest(id: int) -> Union[str, None]:
    try:
        chat_of_interest = Chat_of_interest.get(id=id)
        chat_of_interest.delete()
        commit()
        return "Chat of interest deleted"
    except ObjectNotFound:
        return "Chat of interest not found"


def delete_chat(id: int) -> Union[str, None]:
    try:
        chat = Chat.get(id=id)
        chat.delete()
        commit()
        return "Chat deleted"
    except ObjectNotFound:
        return "Chat not found"


def delete_user_of_interest(id: int) -> Union[str, None]:
    try:
        user_of_interest = User_of_interest.get(id=id)
        user_of_interest.delete()
        commit()
        return "User of interest deleted"
    except ObjectNotFound:
        return "User of interest not found"


def delete_user(id: int) -> Union[str, None]:
    try:
        user = User.get(id=id)
        user.delete()
        commit()
        return "User deleted"
    except ObjectNotFound:
        return "User not found"
