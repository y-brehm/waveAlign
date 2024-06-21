from numpy import ndarray

from wavealign.loudness_processing.compressed_file_processor import (
    CompressedFileProcessor,
)
from wavealign.loudness_processing.uncompressed_file_processor import (
    UncompressedFileProcessor,
)
from wavealign.data_collection.audio_property_set import AudioPropertySet


class AudioFileProcessor:
    def __init__(self) -> None:
        self.__uncompressed_file_processor = UncompressedFileProcessor()
        self.__compressed_file_processor = CompressedFileProcessor()

    def process(
        self,
        audio_property_set: AudioPropertySet,
        target_level: int,
        output_path: str,
        audio_data: ndarray,
    ) -> None:

        if audio_property_set.metadata.codec_name == "mp3":
            self.__compressed_file_processor.process(
                audio_property_set, target_level, output_path
            )
        else:
            self.__uncompressed_file_processor.process(
                audio_property_set, target_level, output_path, audio_data
            )
