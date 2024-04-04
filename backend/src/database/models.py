from datetime import datetime
from pony.orm import *

db = Database()


class Site_user(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_of_interests = Set('User_of_interest')
    chat_of_interests = Set('Chat_of_interest')
    username = Required(str, 32)
    full_name = Optional(str)
    password = Required(str)
    created_at = Required(datetime)
    modified_at = Optional(datetime)


class Chat_of_interest(db.Entity):
    id = PrimaryKey(int, auto=True)
    site_user = Required(Site_user)
    name = Optional(str)
    chats = Set('Chat')


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    chat_of_interest = Optional(Chat_of_interest)
    title = Required(str)
    type = Required(str)
    last_message = Optional(LongStr)
    chatPhoto = Optional(str)
    interest_status = Required(int)


class User_of_interest(db.Entity):
    id = PrimaryKey(int)
    site_user = Required(Site_user)
    name = Optional(str)
    users = Set('User')


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_of_interest = Optional(User_of_interest)
    first_name = Optional(str)
    last_name = Optional(str)
    username = Required(str)
    phone_number = Optional(str)
    profilePhoto = Optional(str)
    interest_status = Required(int)


