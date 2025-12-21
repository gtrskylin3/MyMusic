from app.repositories.tracks import tracks_repository
from app.schemas.tracks import TrackRead, TrackCreate, TrackUpdate
from sqlalchemy.ext.asyncio import AsyncSession



class TrackService:
    async def create_track(self, db: AsyncSession, tracks_in: TrackCreate):
        pass