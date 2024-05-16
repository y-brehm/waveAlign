import os
import numpy as np

from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.metadata_extractor import MetaDataExtractor
from wavealign.data_collection.audio_level_extractor import AudioLevelExtractor
from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.window_size import WindowSize


class AudioPropertySetGenerator:
    def __init__(self, window_size: WindowSize) -> None:
        self.__metadata_extractor = MetaDataExtractor()
        self.__audio_file_reader = AudioFileReader()
        self.__window_size = window_size

    def generate(
        self,
        file_path: str,
    ) -> AudioPropertySet:
        audio_data = self.__audio_file_reader.read(file_path)
        last_modified = os.path.getmtime(file_path)
        metadata = self.__metadata_extractor.extract(file_path)
        lufs_level, peak_level = self.__get_audio_levels(
            audio_data, metadata.sample_rate
        )
        return AudioPropertySet(
            file_path=file_path,
            last_modified=last_modified,
            original_lufs_level=lufs_level,
            original_peak_level=peak_level,
            metadata=metadata,
        )

    def __get_audio_levels(self, audio_data: np.ndarray, sample_rate: int):
        return (
            AudioLevelExtractor(
                GainCalculationStrategy.LUFS, sample_rate, self.__window_size
            ).extract(audio_data),
            AudioLevelExtractor(
                GainCalculationStrategy.PEAK, sample_rate, self.__window_size
            ).extract(audio_data),
        )
