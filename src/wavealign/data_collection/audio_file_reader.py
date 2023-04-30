from ffmpegio import audio
from numpy import ndarray

from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.data_collection.pcm_float_converter import PcmFloatConverter
from wavealign.data_collection.metadata_extractor import MetaDataExtractor
from wavealign.data_collection.audio_level_extractor import AudioLevelExtractor
from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy


class AudioFileReader:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()
        self.__metadata_extractor = MetaDataExtractor()

    def read(self,
             file_path: str,
             window_size: int,
             gain_calculation_strategy: GainCalculationStrategy
             ) -> AudioFileSpecSet:
        audio_data = self.__read_audio_file(file_path)
        metadata = self.__metadata_extractor.extract(file_path)

        audio_level_extractor = AudioLevelExtractor(
            gain_calculation_strategy,
            metadata.sample_rate,
            window_size
        )
        original_audio_level = audio_level_extractor.extract(audio_data)

        return AudioFileSpecSet(
            file_path=file_path,
            audio_data=audio_data,
            original_audio_level=original_audio_level,
            metadata=metadata
        )

    def __read_audio_file(self, file_path: str) -> ndarray:
        _, audio_data = audio.read(file_path)

        if self.__pcm_float_converter.is_pcm_encoded(audio_data):
            audio_data = self.__pcm_float_converter.pcm_to_float(audio_data)

        return audio_data