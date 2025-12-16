from pydantic_settings import BaseSettings
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
CERT_DIR = APP_DIR / 'cert'

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./music.db"
    COOKIE_SETTINGS: dict = {
        "httponly": True,  # Защита от XSS атак (JS не может прочитать cookie)
        "secure": True,    # Только HTTPS (в продакшене должно быть True)
        "samesite": "none", # Защита от CSRF атак
        "max_age": 3600,   # Время жизни в секундах (для access token)
    }
    REFRESH_COOKIE_SETTINGS: dict = {
        **COOKIE_SETTINGS,
        "max_age": 30 * 24 * 3600,  # 30 дней для refresh token
    }

class JWTSettings(BaseSettings):
    EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 
    PRIVATE_KEY: Path = CERT_DIR / 'private_key.pem'
    PUBLIC_KEY: Path = CERT_DIR / 'public_key.pem'
    ALGORITHM: str = 'RS256'

class RedisSettings(BaseSettings):
    HOST: str = 'localhost'
    PORT: int = 6379
    PASSWORD: str | None = None

redis_settings = RedisSettings()
settings = Settings()
jwt_settings = JWTSettings()