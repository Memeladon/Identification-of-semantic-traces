from fastapi import APIRouter

from data import get_db, create_author, get_author, create_message, MessageCreate, AuthorCreate, Author, Message, \
    get_message

crudRouter = APIRouter(
    # prefix='/weather',
    tags=['crud'],
    responses={404: {"description": "Not found"}}
)


@crudRouter.post("/authors/", response_model=Author)
def create_author_endpoint(author: AuthorCreate):
    with get_db() as db:
        return create_author(db, author)


@crudRouter.get("/authors/{author_id}", response_model=Author)
def read_author_endpoint(author_id: int):
    with get_db() as db:
        return get_author(db, author_id)


@crudRouter.post("/messages/", response_model=Message)
def create_message_endpoint(message: MessageCreate):
    with get_db() as db:
        return create_message(db, message)


@crudRouter.get("/messages/{message_id}", response_model=Message)
def read_message_endpoint(message_id: int):
    with get_db() as db:
        return get_message(db, message_id)
