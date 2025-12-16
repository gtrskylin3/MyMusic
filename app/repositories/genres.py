from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.artists import ArtistCreate, ArtistUpdate
from app.models import Genre

class GenreRepository:
    async def get_or_create(self, db: AsyncSession, genres: list[str] | None) -> list[Genre]:
        gen = []
        if genres:
            for genre_name in genres:
                stmt = select(Genre).where(Genre.name == genre_name)
                result = await db.execute(stmt)
                genre = result.scalar_one_or_none()
                if not genre:
                    genre = Genre(name=genre_name)
                    db.add(genre)
                gen.append(genre)
            await db.flush()
        return gen 
    
genre_repository = GenreRepository()