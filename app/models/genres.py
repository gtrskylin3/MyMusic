from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .artists import Artist
    from .tracks import Track


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    artists = relationship("Artist", secondary="artist_genres", back_populates="genres")
    tracks = relationship("Track", secondary="track_genres", back_populates="genres")


