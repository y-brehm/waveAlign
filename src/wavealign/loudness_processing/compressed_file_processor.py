import shutil
import subprocess

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.loudness_processing.get_aacgain_executable_path import (
    get_aacgain_executable_path,
)


class CompressedFileProcessor:
    def __init__(self) -> None:
        self.__aacgain_executable_path = get_aacgain_executable_path()
        self.__aacgain_offset = 0.71

    def process(
        self,
        audio_property_set: AudioPropertySet,
        target_level: int,
        output_file_path: str,
    ) -> None:
        gain_adjustment = str(
            self.__aacgain_offset
            * (target_level - audio_property_set.original_lufs_level)
        )

        if output_file_path != audio_property_set.file_path:
            shutil.copy(audio_property_set.file_path, output_file_path)

        result = subprocess.run(
            [
                self.__aacgain_executable_path,
                "-q",
                "-g",
                gain_adjustment,
                output_file_path,
            ]
        )

        if result.returncode != 0:
            raise Exception(
                "AACGAIN: Failed to process compressed file:"
                + audio_property_set.file_path
            )
