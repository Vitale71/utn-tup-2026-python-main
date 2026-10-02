
from fastapi import APIRouter, HTTPException, status
from models.songs import (
    UpdateSongResponse,
    Song,
    CreateSongResponse,
    DeleteSongResponse,
    GetSongsResponse
)


router = APIRouter()

canciones: list[Song] = [
    Song(id=1, title="Barbra Streisand", artist="Duck Sauce", genre="Electronica", year=2010),
    Song(id=2, title="Welcome to the Jungle", artist="AC/DC", genre="Rock", year=1987),
]

@router.post("/songs")
def create_song(song: Song) -> CreateSongResponse:
    canciones.append(song)
    return CreateSongResponse(message="cancion creada")

@router.get("/songs")
def get_songs() -> GetSongsResponse:
    r = GetSongsResponse(songs=canciones)
    return r

@router.get("/songs/search")
def search_songs(title: str | None = None, artist: str | None = None, genre: str | None = None, year: int | None = None) -> GetSongsResponse:
    filtered_songs = [
        song for song in canciones
        if (title is None or title.lower() in song.title.lower()) and
           (artist is None or artist.lower() in song.artist.lower()) and
           (genre is None or genre.lower() in song.genre.lower()) and
           (year is None or year == song.year)
    ]
    return GetSongsResponse(songs=filtered_songs)

@router.get("/songs/{id}")
def get_song(id: int) -> Song:
    for song in canciones:
        if song.id == id:
            return song

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cancion no encontrada"
    )

@router.put("/songs/{id}")
def update_song(id: int, song: Song) -> UpdateSongResponse:
    for i, s in enumerate(canciones):
        if s.id == id:
            canciones[i] = song
            return UpdateSongResponse(message="cancion actualizada")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cancion no encontrada"
    )

@router.delete("/songs/{id}")
def delete_song(id: int) -> DeleteSongResponse:
    for song in canciones:
        if song.id == id:
            canciones.remove(song)
            return DeleteSongResponse(message="cancion borrada")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cancion no encontrada"
    )
