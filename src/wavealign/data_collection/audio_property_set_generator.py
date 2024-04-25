import numpy as np

from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.metadata_extractor import MetaDataExtractor
from wavealign.data_collection.audio_level_extractor import AudioLevelExtractor
from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.window_size import WindowSize


class AudioPropertySetGenerator:
    def __init__(self) -> None:
        self.__metadata_extractor = MetaDataExtractor()
        self.__audio_file_reader = AudioFileReader()

    def read(
        self,
        file_path: str,
        window_size: WindowSize,
    ) -> AudioPropertySet:
        audio_data = self.__audio_file_reader.read(file_path)
        metadata = self.__metadata_extractor.extract(file_path)
        lufs_level, peak_level = self.__get_audio_levels(
            audio_data, metadata.sample_rate, window_size
        )

        return AudioPropertySet(
            file_path=file_path,
            original_lufs_level=lufs_level,
            original_peak_level=peak_level,
            metadata=metadata,
        )

    @staticmethod
    def __get_audio_levels(
        audio_data: np.ndarray, sample_rate: int, window_size: WindowSize
    ):
        return (
            AudioLevelExtractor(
                GainCalculationStrategy.LUFS, sample_rate, window_size
            ).extract(audio_data),
            AudioLevelExtractor(
                GainCalculationStrategy.PEAK, sample_rate, window_size
            ).extract(audio_data),
        )
