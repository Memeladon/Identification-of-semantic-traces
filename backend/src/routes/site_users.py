from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pony.orm import ObjectNotFound

import backend.src.database.crud as crud
from backend.src.auth.jwthandler import (
    create_access_token,
    get_current_site_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from..auth.site_users import validate_site_user
from..schemas.site_user import Site_userInSchema, Site_userOutSchema
from..schemas.token import Status

router = APIRouter()


@router.post("/register", response_model=Site_userOutSchema)
async def create_user(user: Site_userInSchema) -> Site_userOutSchema:
    return await crud.create_site_user(user)


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    user = await validate_site_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=18000,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

    return response

# usage:
@router.get(
    "/users/whoami", response_model=Site_userOutSchema, dependencies=[Depends(get_current_site_user)]
)
async def read_users_me(current_user: Site_userOutSchema = Depends(get_current_site_user)):
    return current_user


@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": ObjectNotFound}},
    dependencies=[Depends(get_current_site_user)],
)
async def delete_user(
    user_id: int, current_user: Site_userOutSchema = Depends(get_current_site_user)
) -> Status:
    return await crud.delete_site_user(user_id, current_user)
