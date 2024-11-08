import csv
import datetime
import json
import os

import requests
from yandex_music import Client
from yandex_music.exceptions import NotFoundError


with open('auth.json', 'r') as fp:
    TOKEN = json.load(fp)["yandex_token"]

client = Client(TOKEN).init()

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}


def search_playlists(query: str, fetch_tracks: bool = True, limit: int = 10):
    search_result = client.search(query).playlists
    results = []
    writer = csv.writer(open("yandex.csv", "a+", newline="", encoding="utf-8"))

    count = 0

    for result in search_result.results:
        playlist = result.fetch_tracks()
        # create a dir for each playlist

        if fetch_tracks:
            playlist_dir = f"playlists/{result.title}"
            try:
                os.makedirs(playlist_dir)
            except FileExistsError:
                pass
        for track_short in playlist:
            if count >= limit:
                return results

            track = track_short.track
            artists = track.artists
            album = track.albums[0]
            try:
                lyrics_info = track.get_lyrics()
                lyrics = requests.get(lyrics_info["download_url"]).text
            except NotFoundError:
                lyrics = None

            info = {
                "id": track.id,
                "title": track.title,
                "artists": ', '.join(artist.name for artist in artists),
                "album": album.title,
                "album_id": album.id,
                "time": datetime.datetime.now(),
                "playlist": result.title,
                "lyrics": lyrics,
            }
            if fetch_tracks:
                fetched_track = track_short.fetch_track()
                fetched_track.download(f"{playlist_dir}/{track.title}.mp3")

            writer.writerow(list(info.values()))
            results.append(info)
            count += 1

    return results


if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        search_playlists(input_query, limit=10, fetch_tracks=True)