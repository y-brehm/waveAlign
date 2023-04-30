from ffmpegio import audio
from numpy import ndarray

from wavealign.loudness_processing.calculation import calculate_lufs
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.data_collection.pcm_float_converter import PcmFloatConverter
from wavealign.data_collection.metadata_extractor import MetaDataExtractor


class AudioFileReader:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()
        self.__metadata_extractor = MetaDataExtractor()

    def read(self, file_path: str) -> AudioFileSpecSet:
        audio_data = self.__read_audio_file(file_path)
        metadata = self.__metadata_extractor.extract(file_path)
        original_lufs = calculate_lufs(audio_data, metadata.sample_rate)

        return AudioFileSpecSet(
            file_path=file_path,
            audio_data=audio_data,
            original_lufs=original_lufs,
            metadata=metadata
            )

    def __read_audio_file(self, file_path: str) -> ndarray:
        _, audio_data = audio.read(file_path)

        if self.__pcm_float_converter.is_pcm_encoded(audio_data):
            audio_data = self.__pcm_float_converter.pcm_to_float(audio_data)

        return audio_data
