import os


class AudioFileFinder:
    def find(self, start_dir: str) -> list[str]:
        abs_start_dir = os.path.abspath(start_dir)
        audio_file_paths = []
        for root, _, files in os.walk(abs_start_dir):
            for file_name in files:
                if self.__is_supported_audio_file(file_name):
                    audio_file_paths.append(os.path.join(root, file_name))

        return audio_file_paths

    @staticmethod
    def __is_supported_audio_file(file_name: str) -> bool:
        file_extension = os.path.splitext(file_name)[1]
        supported_file_extensions = [".wav", ".aiff", ".aif", ".mp3", ".flac"]

        return file_extension in supported_file_extensions
