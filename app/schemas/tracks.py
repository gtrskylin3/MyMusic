from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.schemas.genres import GenreRead


class TrackBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the track")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the track")
    filename: str = Field(..., description="File name of the track")


class TrackCreate(TrackBase):
    """Schema for creating a new track"""
    genres: Optional[List[str]]
    file_url: str = Field(..., description="File url of the track")


class TrackUpdate(BaseModel):
    """Schema for updating an existing track"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Title of the track")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the track")
    filename: Optional[str] = Field(None, description="File name of the track")
    genres: Optional[List[str]] = Field(None, description="List of genre names to associate with the track")


class TrackScheme(BaseModel):
    """Base schema with ORM mode enabled"""
    model_config = ConfigDict(from_attributes=True)


class TrackRead(TrackScheme):
    """Schema for reading track data with ID"""
    id: int
    title: str
    description: Optional[str]
    filename: str
    file_url: str
    artist_id: int
    genres: List[GenreRead] = []







