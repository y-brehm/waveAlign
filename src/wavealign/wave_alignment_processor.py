from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.caching.caching_processor import CachingProcessor
from wavealign.caching.cache_manager import CacheManager
from wavealign.caching.levels_cache_finder import LevelsCacheFinder
from wavealign.utility.ensure_path_exists import ensure_path_exists


class WaveAlignmentProcessor:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        window_size: WindowSize,
        target_level: int,
        clipping_strategy: ClippingStrategy = ClippingStrategy.SKIP,
    ) -> None:
        self.__output_path = output_path
        self.__caching_processor = CachingProcessor(cache_path=input_path)
        cache_data = self.__caching_processor.read_cache()

        self.__audio_property_sets_reader = AudioPropertySetsReader(
            input_path=input_path,
            window_size=window_size,
            cache_manager=CacheManager(
                cache_data=cache_data, target_level=target_level
            ),
            levels_cache_finder=LevelsCacheFinder(cache_data=cache_data),
        )
        self.__audio_property_sets_processor = AudioPropertySetsProcessor(
            target_level=target_level,
            cache_data=cache_data,
            clipping_strategy=clipping_strategy,
        )

    def process(self) -> None:
        ensure_path_exists(self.__output_path)
        cache_data = self.__caching_processor.read_cache()

        audio_property_sets = self.__audio_property_sets_reader.read()

        cache = self.__audio_property_sets_processor.process(
            audio_property_sets, self.__output_path
        )

        if not (cache == cache_data):
            self.__caching_processor.write_cache(cache)
