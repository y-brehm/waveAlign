import numpy as np
from ffmpegio import audio

from wavealign.data_collection.pcm_float_converter import PcmFloatConverter
from wavealign.data_collection.audio_metadata import AudioMetadata
from wavealign.data_collection.write_metadata import write_metadata

# TODO: Include full metadata read and write


class AudioFileWriter:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()

    def write(
        self, file_path: str, audio_data: np.ndarray, audio_metadata: AudioMetadata
    ) -> None:
        self.__write_audio(file_path, audio_data, audio_metadata)
        write_metadata(file_path, audio_metadata)

    def __write_audio(
        self, file_path: str, audio_data: np.ndarray, metadata: AudioMetadata
    ) -> None:
        if self.__pcm_float_converter.is_pcm_encoded(audio_data):
            audio_data = self.__pcm_float_converter.float_to_pcm(audio_data)

        audio.write(
            file_path,
            metadata.sample_rate,
            audio_data,
            c=metadata.codec_name,
            overwrite=True,
            ac=metadata.num_channels,
            ab=metadata.bit_rate,
            write_id3v2=True,
        )
