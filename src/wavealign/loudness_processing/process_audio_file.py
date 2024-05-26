from wavealign.loudness_processing.process_compressed_file import (
    process_compressed_file,
)
from wavealign.loudness_processing.process_uncompressed_file import (
    process_uncompressed_file,
)
from wavealign.data_collection.audio_property_set import AudioPropertySet


def process_audio_file(
    audio_property_set: AudioPropertySet,
    target_level: int,
    file_output_path: str,
    audio_data: bytes,
) -> None:
    if audio_property_set.metadata.codec_name == "mp3":
        process_compressed_file(audio_property_set, target_level, file_output_path)
    else:
        process_uncompressed_file(
            audio_property_set, target_level, file_output_path, audio_data
        )
