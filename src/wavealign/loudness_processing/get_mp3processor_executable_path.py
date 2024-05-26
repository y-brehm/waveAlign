import os


def get_mp3processor_executable_path() -> str:
    root_dir = os.path.realpath(__file__)

    for _ in range(4):
        root_dir = os.path.dirname(root_dir)

    return os.path.join(root_dir, "mp3processor", "bin", "Mac", "mp3processor")
