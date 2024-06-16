import os
import numpy as np

from wavealign.caching.levels_cache_finder import LevelsCacheFinder
from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.metadata_extractor import MetaDataExtractor
from wavealign.data_collection.audio_level_extractor import AudioLevelExtractor
from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.window_size import WindowSize


class AudioPropertySetGenerator:
    def __init__(
        self, window_size: WindowSize, levels_cache_finder: LevelsCacheFinder | None = None
    ) -> None:
        self.__levels_cache_finder = levels_cache_finder
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

        if self.__levels_cache_finder is not None:
            cached_levels = self.__levels_cache_finder.get_levels(file_path)

            if cached_levels is not None:

                return AudioPropertySet(
                    file_path=file_path,
                    last_modified=last_modified,
                    original_lufs_level=cached_levels.lufs,
                    original_peak_level=cached_levels.peak,
                    metadata=metadata,
                )
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

    def __get_audio_levels(
        self, audio_data: np.ndarray, sample_rate: int
    ) -> tuple[float, float]:
        return (
            AudioLevelExtractor(
                GainCalculationStrategy.LUFS, sample_rate, self.__window_size
            ).extract(audio_data),
            AudioLevelExtractor(
                GainCalculationStrategy.PEAK, sample_rate, self.__window_size
            ).extract(audio_data),
        )
