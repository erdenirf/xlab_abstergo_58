import os
import argparse
from data.vocal_extractor import create_vocal_set
from data.yandex_pipeline import search_playlists


def main(queries: list, limit: int = 10, use_cuda=False):
    for query in queries:
        results = search_playlists(query, limit=limit, fetch_tracks=True)
        print(f"Found {len(results)} tracks for {query}")
        paths = [result["path"] for result in results]
        create_vocal_set(paths, "demucs/vocals", use_cuda)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some queries.")
    parser.add_argument('--limit', type=int, default=10, help='Limit the number of tracks to fetch')
    parser.add_argument('--use_cuda', type=bool, default=False, help='Use CUDA for processing')

    args = parser.parse_args()
    with open("queries.txt", encoding="utf-8") as file:
        queries = file.readlines()
    queries = [query.strip() for query in queries]

    main(queries, limit=args.limit, use_cuda=args.use_cuda)
