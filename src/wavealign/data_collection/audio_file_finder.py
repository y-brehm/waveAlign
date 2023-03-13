import os


class AudioFileFinder:
    def find(self, start_dir: str) -> list[str]:
        abs_start_dir = os.path.abspath(start_dir)
        wav_files = []
        for root, _, files in os.walk(abs_start_dir):
            for file_name in files:
                if self.__is_supported_audio_file(file_name):
                    wav_files.append(os.path.join(root, file_name))

        return wav_files

    def __is_supported_audio_file(self, file_name: str) -> bool:
        file_extension = os.path.splitext(file_name)[1]
        supported_file_extensions = ['.wav', '.aiff']

        return file_extension in supported_file_extensions
