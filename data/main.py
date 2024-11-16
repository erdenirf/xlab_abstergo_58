import pandas as pd

import os
import argparse

from script_generator import generate_script_from_playlist
from vocal_extractor import create_vocal_set
from yandex_pipeline import search_playlists


def main(queries: list, limit: int = 10, use_cuda=False):
    for query in queries:
        results = search_playlists(query, limit=limit, fetch_tracks=True)
        print(f"Found {len(results)} tracks for {query}")
        paths = [result["path"] for result in results]
        create_vocal_set(paths, "demucs/vocals", use_cuda)

    music_df = pd.read_csv("yandex.csv",
                           names=["id", "title", "artists", "album", "album_id", "time", "playlist", "lyrics", "path"])
    music_df = music_df.drop_duplicates(subset=["id"])
    music_df = music_df[
        music_df["path"].apply(lambda x: os.path.exists(f"vocals/{x.split('/')[-1].split('.')[0]}_vocals.mp3"))]

    playlists_unique = music_df["playlist"].unique()
    playlist_scripts_map = {playlist: generate_script_from_playlist(playlist) for playlist in playlists_unique}
    music_df["script"] = music_df["playlist"].apply(lambda x: playlist_scripts_map[x])
    music_df.to_csv("dataset.csv", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some queries.")
    parser.add_argument('--limit', type=int, default=10, help='Limit the number of tracks to fetch')
    parser.add_argument('--use_cuda', type=bool, default=False, help='Use CUDA for processing')

    args = parser.parse_args()
    with open("queries.txt", encoding="utf-8") as file:
        queries = file.readlines()
    queries = [query.strip() for query in queries]

    main(queries, limit=args.limit, use_cuda=args.use_cuda)
