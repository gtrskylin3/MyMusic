from pydantic import BaseModel, Field, ConfigDict

from app.schemas.genres import GenreRead


class ArtistBase(BaseModel):
    username: str = Field(max_length=15)


class ArtistCreate(ArtistBase):
    password: str = Field(min_length=8, max_length=32)
    name: str | None = Field(..., max_length=32)
    description: str | None = Field(..., max_length=255)
    genres: list[str] | None = Field(..., max_length=10)

class ArtistUpdate(ArtistBase):
    name: str | None = Field(..., max_length=32)
    description: str | None = Field(..., max_length=255)
    genres: list[str] | None = Field(..., max_length=10)

class ArtistScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    is_active: bool

class ArtistRead(ArtistScheme):
    name: str | None
    description: str | None 
    genres: list[GenreRead] | None


    




