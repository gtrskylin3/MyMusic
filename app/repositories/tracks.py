from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.tracks import TrackCreate, TrackUpdate
from app.models import Track
from app.repositories.genres import genre_repository


class TrackRepository:
    def __init__(self) -> None:
        self.genre_repository = genre_repository

    async def create(self, db: AsyncSession, genres, create_data: dict):
        genres_obj = None
        if genres:
            genres_obj = await genre_repository.get_or_create(db, genres)
        track = Track(**create_data, genres=genres_obj)
        db.add(track)
        await db.commit()
        stmt = (
            select(Track)
            .options(selectinload(Track.genres))
            .where(Track.id == track.id)
        )
        result = await db.scalar(stmt)
        return result

    async def get_by_id(self, db: AsyncSession, id: int):
        stmt = select(Track).options(selectinload(Track.genres)).where(Track.id == id)
        result = await db.scalar(stmt)
        return result

    async def get_by_title(self, db: AsyncSession, title: str):
        stmt = (
            select(Track)
            .options(selectinload(Track.genres))
            .where(Track.title == title)
        )
        result = await db.scalar(stmt)
        return result

    async def update(self, db: AsyncSession, track_id: int, to_update: TrackUpdate):
        data = to_update.model_dump()
        track_to_update = self.get_by_id(db, track_id)
        if not track_to_update:
            return

        for field, value in data.items():
            if hasattr(track_to_update, field):
                setattr(track_to_update, field, value)
        await db.commit()
        updated_track = await db.refresh(track_to_update)
        return updated_track


artist_repository = TrackRepository()
