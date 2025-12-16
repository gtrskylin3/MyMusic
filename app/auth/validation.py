from typing import Any
from fastapi import Cookie, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import utils
from app.schemas.artists import ArtistScheme, ArtistRead
from app.auth.jwt_helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.repositories.artists import artist_repository
from app.database.db import get_session


def get_access_token_from_cookie(
    access_token: str | None = Cookie(default=None, alias="access_token"),
) -> str:
    """
    Извлекает access токен из cookie.
    Raises:
        HTTPException: Если токен отсутствует
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found in cookies",
        )
    return access_token


def get_refresh_token_from_cookie(
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
) -> str:
    """
    Извлекает refresh токен из cookie.
    Raises:
        HTTPException: Если токен отсутствует
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found in cookies",
        )
    return refresh_token


def decode_token(token: str) -> dict:
    """
    Декодирует JWT токен и возвращает payload.

    Args:
        token: JWT токен строкой

    Returns:
        dict: Payload токена с полями {sub, type, exp, iat, jti, ...}

    Raises:
        HTTPException: Если токен невалидный или истек
    """
    try:
        payload = utils.decode_jwt(token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )


def validate_token_type(payload: dict, expected_type: str) -> None:
    """
    Проверяет, что тип токена соответствует ожидаемому.

    Args:
        payload: Декодированный payload токена
        expected_type: Ожидаемый тип ('access' или 'refresh')

    Raises:
        HTTPException: Если тип токена не совпадает
    """
    actual_type = payload.get(TOKEN_TYPE_FIELD)

    if actual_type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token type. Expected "{expected_type}", got "{actual_type}"',
        )


async def get_user_from_payload(db: AsyncSession, payload: dict) -> ArtistRead:
    """
    Извлекает пользователя из БД по user_id из payload.

    Args:
        payload: Декодированный payload токена (должен содержать 'sub' с user_id)

    Returns:
        UserScheme: Схема пользователя

    Raises:
        HTTPException: Если пользователь не найден
    """

    user_id_str: str | None = payload.get("sub")

    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing 'sub' field",
        )
        
    user_id = int(user_id_str)
    user = await artist_repository.get_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return ArtistRead.model_validate(user)


async def get_current_user_from_access_token(
    token: str = Depends(get_access_token_from_cookie),
    db: AsyncSession = Depends(get_session),
) -> ArtistScheme:
    """
    Полная цепочка валидации для access токена.

    1. Извлекает токен из cookie
    2. Декодирует JWT
    3. Проверяет тип токена (должен быть 'access')
    4. Получает пользователя из БД

    Returns:
        UserScheme: Аутентифицированный пользователь
    """
    payload = decode_token(token)
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    user = await get_user_from_payload(db, payload)
    return ArtistScheme.model_validate(user)


async def get_current_user_from_refresh_token(
    token: str = Depends(get_refresh_token_from_cookie),
    db: AsyncSession = Depends(get_session),
) -> ArtistScheme:
    """
    Полная цепочка валидации для refresh токена.

    1. Извлекает токен из cookie
    2. Декодирует JWT
    3. Проверяет тип токена (должен быть 'refresh')
    4. Получает пользователя из БД

    Returns:
        UserScheme: Аутентифицированный пользователь
    """
    payload = decode_token(token)
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    user = await get_user_from_payload(db, payload)
    return ArtistScheme.model_validate(user)
    
async def get_current_active_user(
    user: ArtistScheme = Depends(get_current_user_from_access_token)
) -> ArtistRead:
    if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
    return ArtistRead.model_validate(user)