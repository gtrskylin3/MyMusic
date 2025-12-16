from datetime import timedelta
from app.auth import utils
from app.config import jwt_settings
from app.schemas.artists import ArtistRead, ArtistScheme

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_token(
    token_type: str,
    token_data: dict,
    expire_minutes: int = jwt_settings.EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None
):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return utils.encode_jwt(
        jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )
    
def create_access_token(
    user: ArtistScheme
) -> str:
    jwt_payload = {
        'sub': str(user.id),
        'username': user.username,
    }
    return create_token(
        token_type = ACCESS_TOKEN_TYPE,
        token_data = jwt_payload,
    )

def create_refresh_token(
    user: ArtistScheme
) -> str:
    jwt_payload = {
        'sub': str(user.id),
    }
    return create_token(
        token_type = REFRESH_TOKEN_TYPE,
        token_data = jwt_payload,
        expire_timedelta=timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    

    

