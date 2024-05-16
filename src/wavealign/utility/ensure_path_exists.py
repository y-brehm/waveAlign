import os


def ensure_path_exists(path: str) -> None:
    if path and not os.path.exists(path):
        os.makedirs(path)
