from datetime import timedelta, datetime, timezone
from typing import Dict
import jwt
from app.config import jwt_settings
import bcrypt
import uuid


def encode_jwt(
    payload: dict,
    private_key: str = jwt_settings.PRIVATE_KEY.read_text(),
    algorithm: str = jwt_settings.ALGORITHM,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = jwt_settings.EXPIRE_MINUTES,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4().hex))
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = jwt_settings.PUBLIC_KEY.read_text(),
    algorithm: str = jwt_settings.ALGORITHM,
):
    decoded = jwt.decode(token, public_key, algorithm)
    return decoded
    

def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
    
def validate_password(
    password: str,
    hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
    
