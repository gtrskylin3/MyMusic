from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from contextlib import asynccontextmanager
import uvicorn
from app.database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

MEDIA_PATH = Path("app/media/tracks")

@app.get('/media/tracks/{filename}')
def get_track(filename: str):
    return FileResponse(MEDIA_PATH / filename)

if __name__ == "__main__":
    uvicorn.run('app.main:app', reload=True)
