import os


def find_audio_files(start_dir: str, file_ending) -> list[str]:
    abs_start_dir = os.path.abspath(start_dir)
    wav_files = []
    for root, dirs, files in os.walk(abs_start_dir):
        for file in files:
            if file.endswith(file_ending):
                wav_files.append(os.path.join(root, file))

    return wav_files
