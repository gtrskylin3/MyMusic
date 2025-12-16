from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.validation import (
    get_current_active_user,
    get_current_user_from_refresh_token,
)
from app.auth.jwt_helpers import create_access_token, create_refresh_token
from app.schemas.artists import ArtistCreate, ArtistRead, ArtistScheme
from app.services.artist_service import artist_service
from fastapi.security import OAuth2PasswordRequestForm
from app.database.db import get_session
from app.config import settings
from typing import Annotated

sessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/api/auth")


@router.post("/register", response_model=ArtistRead)
async def register_user(db: sessionDep, user_data: ArtistCreate):
    return await artist_service.create_artist(db, artist_in=user_data)


@router.post("/login", response_model=ArtistRead)
async def login(
    db: sessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    username = form_data.username
    user = await artist_service.get_artist_by_username(db, username)
    user_validate = await artist_service.validate_artist_credentials(
        db, user.username, form_data.password
    )
    response.set_cookie(
        key="access_token",
        value=create_access_token(user_validate),
        **settings.COOKIE_SETTINGS,
    )
    response.set_cookie(
        key="refresh_token",
        value=create_refresh_token(user_validate),
        **settings.REFRESH_COOKIE_SETTINGS,
    )
    return user


@router.post("/refresh")
async def refresh_tokens(
    response: Response,
    user: ArtistScheme = Depends(get_current_user_from_refresh_token)
):
    # Создаем новый access token
    new_access_token = create_access_token(user)

    # Опционально: создаем новый refresh token (refresh token rotation)
    # Это повышает безопасность, но требует более сложной логики
    new_refresh_token = create_refresh_token(user)

    # Устанавливаем новые токены
    response.set_cookie(
        key="access_token", value=new_access_token, **settings.COOKIE_SETTINGS
    )

    response.set_cookie(
        key="refresh_token", value=new_refresh_token, **settings.REFRESH_COOKIE_SETTINGS
    )

    return {"message": "Tokens refreshed successfully"}


@router.post("/logout")
async def logout(
    response: Response,
    user: ArtistRead = Depends(get_current_active_user),
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logout successful"}

@router.post("/me")
async def get_current_user_info(
    response: Response,
    user: ArtistRead = Depends(get_current_active_user),
): 
    return user


@router.get("/validate")
async def validate_token(
    user: ArtistScheme = Depends(get_current_active_user)
):
    """
    Проверка валидности access токена.
    
    Полезно для frontend'а, чтобы проверить, залогинен ли пользователь.
    
    Returns:
        dict: Статус валидности токена
    """
    return {
        "valid": True,
        "user_id": user.id
    } 