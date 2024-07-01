import os
import platform


def retrieve_mp3processor_executable_path() -> str:
    root_dir = os.path.realpath(__file__)

    for _ in range(2):
        root_dir = os.path.dirname(root_dir)

    bin_folder_path = os.path.join(root_dir, "mp3processor", "bin")

    if platform.system() == "Windows":
        return os.path.join(bin_folder_path, "Win", "Release", "mp3processor.exe")
    if platform.system() == "Darwin":
        return os.path.join(bin_folder_path, "Mac", "mp3processor")
    else:
        raise SystemError(f"Unsupported platform: {platform.system()}")
