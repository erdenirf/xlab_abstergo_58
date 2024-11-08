from data.vocal_extractor import create_vocal_set
from data.yandex_pipeline import search_playlists


def main(queries: list, limit: int = 10):
    for query in queries:
        results = search_playlists(query, limit=limit, fetch_tracks=True)
        print(f"Found {len(results)} tracks for {query}")
        paths = [result["path"] for result in results]
        create_vocal_set(paths, "demucs/vocals")


if __name__ == '__main__':
    with open("queries.txt", encoding="utf-8") as file:
        queries = file.readlines()
    queries = [query.strip() for query in queries]
    main(queries, limit=10)
