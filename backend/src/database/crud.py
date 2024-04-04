from pony.orm import commit, ObjectNotFound, IntegrityError

from models import db, Site_user, Chat_of_interest, Chat, User_of_interest, User
from config import PONY_ORM_CONFIG

# db.bind(**PONY_ORM_CONFIG['connections']['default'])
# db.generate_mapping(create_tables=True)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- CREATE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
def create_site_user(username, full_name, password):
    try:
        user = Site_user(username=username, full_name=full_name, password=password)
        commit()
        return user
    except IntegrityError:
        return "Username already exists"
    except Exception as e:
        return f"Error creating user: {e}"


def create_chat_of_interest(site_user_id, name):
    try:
        user = Site_user.get(id=site_user_id)
        chat_of_interest = Chat_of_interest(site_user=user, name=name)
        commit()
        return chat_of_interest
    except IntegrityError:
        return "Site user not found"
    except Exception as e:
        return f"Error creating chat of interest: {e}"


def create_chat(chat_of_interest_id, title, type, last_message, chatPhoto, interest_status):
    try:
        chat_of_interest = Chat_of_interest.get(id=chat_of_interest_id)
        chat = Chat(chat_of_interest=chat_of_interest, title=title, type=type, last_message=last_message,
                    chatPhoto=chatPhoto, interest_status=interest_status)
        commit()
        return chat
    except IntegrityError:
        return "Username already exists"
    except Exception as e:
        return f"Error creating user: {e}"


def create_user_of_interest(site_user_id, name):
    try:
        user = Site_user.get(id=site_user_id)
        user_of_interest = User_of_interest(site_user=user, name=name)
        commit()
        return user_of_interest
    except IntegrityError:
        return "Username already exists"
    except Exception as e:
        return f"Error creating user: {e}"


def create_user(user_of_interest_id, first_name, last_name, username, phone_number, profilePhoto, interest_status):
    try:
        user_of_interest = User_of_interest.get(id=user_of_interest_id)
        user = User(user_of_interest=user_of_interest, first_name=first_name, last_name=last_name, username=username,
                    phone_number=phone_number, profilePhoto=profilePhoto, interest_status=interest_status)
        commit()
        return user
    except IntegrityError:
        return "Username already exists"
    except Exception as e:
        return f"Error creating user: {e}"


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ----------------------------------------------------- READ ----------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def get_site_user(id):
    try:
        return Site_user.get(id=id)
    except ObjectNotFound:
        return "User not found"


def get_chat_of_interest(id):
    try:
        return Chat_of_interest.get(id=id)
    except ObjectNotFound:
        return "Chat of interest not found"


def get_chat(id):
    try:
        return Chat.get(id=id)
    except ObjectNotFound:
        return "Chat not found"


def get_user_of_interest(id):
    try:
        return User_of_interest.get(id=id)
    except ObjectNotFound:
        return "User of interest not found"


def get_user(id):
    try:
        return User.get(id=id)
    except ObjectNotFound:
        return "User not found"


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# ---------------------------------------------------- UPDATE ---------------------------------------------------- #
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def update_site_user(id, username=None, full_name=None, password=None):
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


def update_chat_of_interest(id, name=None):
    try:
        chat_of_interest = Chat_of_interest.get(id=id)
        if name:
            chat_of_interest.name = name
        commit()
        return chat_of_interest
    except ObjectNotFound:
        return "Chat of interest not found"


def update_chat(id, title=None, type=None, last_message=None, chatPhoto=None, interest_status=None):
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


def update_user_of_interest(id, name=None):
    try:
        user_of_interest = User_of_interest.get(id=id)
        if name:
            user_of_interest.name = name
        commit()
        return user_of_interest
    except ObjectNotFound:
        return "User of interest not found"


def update_user(id, first_name=None, last_name=None, username=None, phone_number=None, profilePhoto=None,
                interest_status=None):
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

def delete_site_user(id):
    try:
        user = Site_user.get(id=id)
        user.delete()
        commit()
        return "User deleted"
    except ObjectNotFound:
        return "User not found"


def delete_chat_of_interest(id):
    try:
        chat_of_interest = Chat_of_interest.get(id=id)
        chat_of_interest.delete()
        commit()
        return "Chat of interest deleted"
    except ObjectNotFound:
        return "Chat of interest not found"


def delete_chat(id):
    try:
        chat = Chat.get(id=id)
        chat.delete()
        commit()
        return "Chat deleted"
    except ObjectNotFound:
        return "Chat not found"


def delete_user_of_interest(id):
    try:
        user_of_interest = User_of_interest.get(id=id)
        user_of_interest.delete()
        commit()
        return "User of interest deleted"
    except ObjectNotFound:
        return "User of interest not found"


def delete_user(id):
    try:
        user = User.get(id=id)
        user.delete()
        commit()
        return "User deleted"
    except ObjectNotFound:
        return "User not found"
