from .base import Base
from pathlib import Path
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .artists import Artist
    


class Track(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] 
    description: Mapped[str | None]
    filepath: Mapped[str]
    listening: Mapped[int]
    likes: Mapped[int]
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'))
    artist = relationship("Artist", back_populates='tracks')



