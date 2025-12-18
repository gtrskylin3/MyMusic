from .base import Base
from pathlib import Path
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .artists import Artist
    from .genres import Genre
    


class Track(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] 
    description: Mapped[str | None]
    filepath: Mapped[str]
    # TODO
    # listening: Mapped[int]
    # likes: Mapped[int]
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'))
    artist = relationship("Artist", back_populates='tracks')
    genres: Mapped[list["Genre"]] = relationship("Genre", secondary="track_genres", back_populates="tracks")    


class TrackGenres(Base):
    __tablename__ = 'track_genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))


