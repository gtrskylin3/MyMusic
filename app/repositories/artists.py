from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.artists import ArtistCreate, ArtistUpdate
from app.models import Artist
from app.repositories.genres import genre_repository

class ArtistRepository:
    def __init__(self) -> None:
        self.genre_rep = genre_repository

    async def create(self, db: AsyncSession, genres: list[str] | None, artist_data: dict):
        genres_obj = None
        if genres:
            genres_obj = await genre_repository.get_or_create(db, genres)   
        artist = Artist(**artist_data, genres=genres_obj)
        db.add(artist)
        await db.commit()
        stmt = select(Artist).options(selectinload(Artist.genres)).where(Artist.id == artist.id)
        result = await db.scalar(stmt)
        return result
    
    
    
    async def get_by_id(self, db: AsyncSession, id: int):
        stmt = select(Artist).options(selectinload(Artist.genres)).where(Artist.id == id)
        result = await db.scalar(stmt)
        return result

    async def get_by_username(self, db: AsyncSession, username):
        stmt = select(Artist).options(selectinload(Artist.genres)).where(Artist.username == username)
        result = await db.scalar(stmt)
        return result
        
    
    async def update(self, db: AsyncSession, to_update: ArtistUpdate, id: int):
        update_data = to_update.model_dump()
        artist = self.get_by_id(db, id)
        for key, value in update_data.items():
            if value:
                if getattr(artist, key):
                    setattr(artist, key, value)
        await db.commit()
        await db.refresh(artist)
        return artist
    

artist_repository = ArtistRepository()