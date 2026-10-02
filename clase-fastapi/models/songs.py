from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    id: int
    title: str
    artist: str
    genre: str
    year: int

class GetSongsResponse(BaseModel):
    songs: List[Song]   


class CreateSongResponse(BaseModel):
    message: str


class UpdateSongResponse(BaseModel):
    message: str


class DeleteSongResponse(BaseModel):
    message: str

