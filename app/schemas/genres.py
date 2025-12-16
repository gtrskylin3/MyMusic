from pydantic import BaseModel
from pydantic import ConfigDict

class GenreBase(BaseModel):
    name: str 

class GenreRead(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)