from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.schemas.genres import GenreRead


class TrackBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the track")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the track")
    filepath: str = Field(..., description="File path of the track")
    artist_id: int = Field(..., gt=0, description="ID of the artist")


class TrackCreate(TrackBase):
    """Schema for creating a new track"""
    genre_names: Optional[List[str]] = Field(None, description="List of genre names to associate with the track")


class TrackUpdate(BaseModel):
    """Schema for updating an existing track"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Title of the track")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the track")
    filepath: Optional[str] = Field(None, description="File path of the track")
    artist_id: Optional[int] = Field(None, gt=0, description="ID of the artist")
    genre_names: Optional[List[str]] = Field(None, description="List of genre names to associate with the track")


class TrackScheme(BaseModel):
    """Base schema with ORM mode enabled"""
    model_config = ConfigDict(from_attributes=True)


class TrackRead(TrackScheme):
    """Schema for reading track data with ID"""
    id: int
    title: str
    description: Optional[str]
    filepath: str
    artist_id: int
    genres: List[GenreRead] = []







