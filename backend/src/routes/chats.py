from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pony.orm import ObjectNotFound

from..database import crud as crud
from..auth.jwthandler import get_current_site_user
from..schemas.chat import ChatOutSchema, ChatInSchema, UpdateChat
from..schemas.token import Status
from..schemas.site_user import Site_userOutSchema



router = APIRouter()


@router.get(
    "/chats",
    response_model=List[ChatOutSchema],
    dependencies=[Depends(get_current_site_user)],
)
async def get_notes():
    return await crud.get_all_chats()


@router.get(
    "/chat/{chat_id}",
    response_model=ChatOutSchema,
    dependencies=[Depends(get_current_site_user)],
)
async def get_note(note_id: int) -> ChatOutSchema:
    try:
        return await crud.get_chat(note_id)
    except ObjectNotFound:
        raise HTTPException(
            status_code=404,
            detail="Note does not exist",
        )


@router.post(
    "/chats", response_model=ChatOutSchema, dependencies=[Depends(get_current_site_user)]
)
async def create_note(
    note: ChatInSchema, current_user: Site_userOutSchema = Depends(get_current_site_user)
) -> ChatOutSchema:
    return await crud.create_chat(note, current_user)


@router.patch(
    "/chat/{chat_id}",
    dependencies=[Depends(get_current_site_user)],
    response_model=ChatOutSchema,
    responses={404: {"model": 'Resource not found'}},
)
async def update_note(
    chat_id: int,
    chat: UpdateChat,
    current_user: Site_userOutSchema = Depends(get_current_site_user),
) -> ChatOutSchema:
    return await crud.update_chat(chat_id, chat, current_user)


@router.delete(
    "/chat/{chat_id}",
    response_model=Status,
    responses={404: {"model": 'Resource not found'}},
    dependencies=[Depends(get_current_site_user)],
)
async def delete_note(
    note_id: int, current_user: Site_userOutSchema = Depends(get_current_site_user)
):
    return await crud.delete_note(note_id, current_user)