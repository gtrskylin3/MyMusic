from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import uuid4
import json

from app.database.db import get_session
from app.config import track_setting
from app.schemas.tracks import TrackUpdate, TrackRead, TrackCreate
from app.schemas.artists import ArtistRead
from app.auth.validation import get_current_active_user
from app.repositories.tracks import tracks_repository

router = APIRouter(prefix="/tracks")
sessionDep = Annotated[AsyncSession, Depends(get_session)]
# @router.post('/create')
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}

async def save_file(file: UploadFile) -> tuple[Path, str, str]:
     
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail='No file uploaded')
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in track_setting.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extensions: {file_ext}")

    if not file.content_type in track_setting.ALLOWED_CONTENT_TYPES:
         raise HTTPException(status_code=400, detail=f"Invalid content type: {file.content_type}")
    
    filename = str(uuid4())
    file_path = track_setting.TRACK_DIR / f"{filename}{file_ext}"
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    return file_path, filename, file_ext
    

@router.post('/upload')
async def upload_track(
    file: Annotated[UploadFile, File()],
    artist: ArtistRead = Depends(get_current_active_user),
    ):
    file_path, filename, file_ext = await save_file(file)
    if not file_path.exists():
        raise HTTPException(500, detail="Server can't save file")
    return {
        "artist_id": artist.id,
        "filename": filename,
        "file_url": f"media/tracks/{filename}{file_ext}"
    }


@router.post('/create', response_model=TrackRead)
async def create_uploaded_file(
    db: sessionDep,
    track_create: TrackCreate,
    artist: ArtistRead = Depends(get_current_active_user),
    ):
    genres = track_create.genres
    create_data = track_create.model_dump(exclude={"genres"})
    create_data.update({"artist_id": artist.id})
    track = await tracks_repository.create(db, genres, create_data)
    return TrackRead.model_validate(track)


@router.get('/find/{title}', response_model=TrackRead)
async def get_track_by_title(
    title: str,
    db: sessionDep
):
    track = await tracks_repository.get_by_title(db, title)    
    if not track:
        raise HTTPException(status_code=404, detail="Track with this title not found")
    return TrackRead.model_validate(track)