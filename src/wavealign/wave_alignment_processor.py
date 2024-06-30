from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.loudness_processing.clipping_strategy_manager import (
    ClippingStrategyManager,
)
from wavealign.caching.yaml_cache import YamlCache
from wavealign.caching.yaml_cache_processor import YamlCacheProcessor
from wavealign.caching.cache_validator import CacheValidator
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
        self.__target_level = target_level
        self.__output_path = output_path
        self.__yaml_cache_processor = YamlCacheProcessor(cache_path=input_path)
        (
            cache_data,
            cache_validator,
            levels_cache_finder,
        ) = self.__setup_cache_management()

        self.__audio_property_sets_reader = AudioPropertySetsReader(
            input_path=input_path,
            window_size=window_size,
            cache_validator=cache_validator,
            levels_cache_finder=levels_cache_finder,
        )
        self.__audio_property_sets_processor = AudioPropertySetsProcessor(
            target_level=target_level,
            cache_data=cache_data,
            clipping_strategy_manager=ClippingStrategyManager(
                clipping_strategy=clipping_strategy, target_level=target_level
            ),
        )

    def process(self) -> None:
        ensure_path_exists(self.__output_path)
        cache_data = self.__yaml_cache_processor.read_cache()

        audio_property_sets = self.__audio_property_sets_reader.read()

        cache = self.__audio_property_sets_processor.process(
            audio_property_sets, self.__output_path
        )
        cache.target_level = self.__target_level

        if not (cache == cache_data):
            self.__yaml_cache_processor.write_cache(cache)

    def __setup_cache_management(
        self,
    ) -> tuple[YamlCache | None, CacheValidator | None, LevelsCacheFinder | None]:
        if self.__output_path is None:
            cache_data = self.__yaml_cache_processor.read_cache()
            cache_validator = CacheValidator(
                cache_data=cache_data, target_level=self.__target_level
            )
            levels_cache_finder = LevelsCacheFinder(cache_data=cache_data)
        else:
            cache_data = None
            cache_validator = None
            levels_cache_finder = None

        return cache_data, cache_validator, levels_cache_finder
