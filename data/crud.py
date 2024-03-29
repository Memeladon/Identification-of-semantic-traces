from sqlalchemy.orm import Session
from . import models, database


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_author(db: Session, author: models.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_message(db: Session, message: models.MessageCreate):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()
