from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import uuid4

from app.database.db import get_session
from app.config import track_setting
from app.schemas.tracks import TrackUpdate, TrackRead, TrackCreate, TrackCreateData
from app.schemas.artists import ArtistRead
from app.auth.validation import get_current_active_user
from app.repositories.tracks import tracks_repository

router = APIRouter(prefix="/tracks")
sessionDep = Annotated[AsyncSession, Depends(get_session)]
# @router.post('/create')
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}

async def save_file(file: UploadFile) -> Path:
     
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail='No file uploaded')
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in track_setting.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extensions: {file_ext}")

    if not file.content_type in track_setting.ALLOWED_CONTENT_TYPES:
         raise HTTPException(status_code=400, detail=f"Invalid content type: {file.content_type}")
    
    upload_id = str(uuid4())
    file_path = track_setting.TRACK_DIR / f"{upload_id}{file_ext}"
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    return file_path
    

@router.post('/upload')
async def upload_track(
    file: Annotated[UploadFile, File()],
    artist: ArtistRead = Depends(get_current_active_user),
    ):
    file_path = await save_file(file)
    return {
        "artist_id": artist.id,
        "file_path": file_path
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

    

