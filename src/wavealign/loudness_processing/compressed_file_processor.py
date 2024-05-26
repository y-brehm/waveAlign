import shutil
import subprocess

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.loudness_processing.get_mp3processor_executable_path import (
    get_mp3processor_executable_path,
)


class CompressedFileProcessor:
    def __init__(self) -> None:
        self.__mp3processor_executable_path = get_mp3processor_executable_path()
        self.__mp3processor_offset = 0.71

    def process(
        self,
        audio_property_set: AudioPropertySet,
        target_level: int,
        output_file_path: str,
    ) -> None:
        gain_adjustment = str(
            self.__mp3processor_offset
            * (target_level - audio_property_set.original_lufs_level)
        )

        if output_file_path != audio_property_set.file_path:
            shutil.copy(audio_property_set.file_path, output_file_path)

        result = subprocess.run(
            [
                self.__mp3processor_executable_path,
                "i",
                output_file_path,
                "-g",
                gain_adjustment,
            ]
        )

        if result.returncode != 0:
            raise Exception(
                "mp3processor: Failed to process compressed file:"
                + audio_property_set.file_path
            )
