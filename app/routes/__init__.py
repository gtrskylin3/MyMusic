__all__ = [
    "auth_router",
    "tracks_router"
]

from .auth import router as auth_router
from .tracks import router as tracks_router