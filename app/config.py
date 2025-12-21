from pydantic_settings import BaseSettings
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
CERT_DIR = APP_DIR / 'cert'
MEDIA_DIR = APP_DIR / 'media'



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

class TrackSettings(BaseSettings):
    
    TRACK_DIR: Path = MEDIA_DIR / 'tracks'
    MAX_SIZE: int = 10 * 8 * 1024 * 1024
    ALLOWED_CONTENT_TYPES: set = {
       "audio/mpeg",    # MP3
       "audio/flac",    # FLAC
       "audio/wav",     # WAV
       "audio/x-wav",   # WAV (альтернативный)
       "audio/aac",     # AAC
       "audio/mp4",     # MP4 Audio
    }

    ALLOWED_EXTENSIONS: set = {".mp3", ".flac", ".wav", ".aac", ".m4a"}


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
track_setting = TrackSettings()
