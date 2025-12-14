from .base import Base
from .tracks import Track
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Artist(Base):
    __tablename__ = 'artists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    username: Mapped[str] 
    description: Mapped[str | None]
    genres: Mapped[str | None]

    tracks = relationship("Track", back_populates='artist')
    
    

