from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import Track
    from .genres import Genre

class Artist(Base):
    __tablename__ = 'artists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    username: Mapped[str] = mapped_column(index=True, unique=True)
    hash_password: Mapped[bytes]
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None]
    genres: Mapped[list["Genre"]] = relationship("Genre", secondary="artist_genres", back_populates="artists")
    tracks = relationship("Track", back_populates='artist')
    
class ArtistGenres(Base):
    __tablename__ = 'artist_genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'))
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'))