from numpy import ndarray
from ffmpegio import audio

from wavealign.data_collection.pcm_float_converter import PcmFloatConverter

# TODO: Include full metadata read and write


class AudioFileReader:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()

    def read(self, file_path: str) -> ndarray:
        _, audio_data = audio.read(file_path)

        if self.__pcm_float_converter.is_pcm_encoded(audio_data):
            audio_data = self.__pcm_float_converter.pcm_to_float(audio_data)

        return audio_data
