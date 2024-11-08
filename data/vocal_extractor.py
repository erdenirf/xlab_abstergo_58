import os

import demucs.separate


def vocal_extractor(input_path, output_dir_path, use_cuda=False):
    vocal_track = demucs.separate.main(
        ["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", "--device", "cuda" if use_cuda else "cpu", "-o",
         output_dir_path, input_path])


def create_vocal_set(songs_path: list, output_dir_path: str, use_cuda=False):
    for song_path in songs_path:
        vocal_extractor(song_path, output_dir_path, use_cuda)
        title = song_path.split("/")[-1]
        os.rename(f"{output_dir_path}/mdx_extra/{title}/vocals.mp3", f"{song_path}_vocals.mp3")
