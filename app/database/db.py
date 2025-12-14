from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Base

engine = create_async_engine('sqlite+aiosqlite:///music.db')

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with async_session_maker() as session:
        yield session