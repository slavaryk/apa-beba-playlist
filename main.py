from fastapi import FastAPI
from yandex_music import ClientAsync # type: ignore
from fastapi.middleware.cors import CORSMiddleware

import os

token = os.getenv("API_TOKEN")

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add_track")
async def add_track(track_id: str, album_id: str):
    PLAYLIST_ID = "1000"
    USER_ID = "slawaryk"

    client = await ClientAsync(token).init()
    playlist = await client.users_playlists(PLAYLIST_ID, USER_ID)

    await client.users_playlists_insert_track(
        PLAYLIST_ID,
        track_id,
        album_id,
        0,
        playlist.revision,
        USER_ID,
    )

@app.get("/search")
async def search(track_name: str, page: int):
    client = await ClientAsync(token).init()
    result = await client.search(track_name, True, "track", page)
    response = []

    if result.tracks != None:
        index = 0
        for track in result.tracks.results:
            response.append({
                "id": track.id,
                "title": track.title,
                "albums": [],
            })

            for album in track.albums:
                response[index]["albums"].append({
                    "id": album.id,
                    "title": album.title,
                    "cover": album.cover_uri,
                })

            index = index + 1

    return response
