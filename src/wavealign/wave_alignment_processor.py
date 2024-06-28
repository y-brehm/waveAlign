import concurrent.futures
from tqdm import tqdm

from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.data_collection.caching_processor import CachingProcessor
from wavealign.data_collection.cache_manager import CacheManager
from wavealign.utility.ensure_path_exists import ensure_path_exists
from wavealign.loudness_processing.uncompressed_file_processor import (
    UncompressedFileProcessor,
)


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
        self.__target_level = target_level
        self.__caching_processor = CachingProcessor(cache_path=input_path)
        cache_data = self.__caching_processor.read_cache()
        self.__audio_property_sets_reader = AudioPropertySetsReader(
            input_path=input_path,
            window_size=window_size,
            cache_manager=CacheManager(
                cache_data=cache_data, target_level=target_level
            ),
        )
        self.__audio_property_sets_processor = AudioPropertySetsProcessor(
            cache_data=cache_data, clipping_strategy=clipping_strategy
        )

    def process(self) -> None:
        ensure_path_exists(self.__output_path)
        cache_data = self.__caching_processor.read_cache()

        audio_property_sets = self.__audio_property_sets_reader.read()
        progress_bar = tqdm(total=len(audio_property_sets), desc="PROCESSING")
        cache = {}

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.__audio_property_sets_processor.process,
                    audio_property_set,
                    self.__target_level,
                    self.__output_path,
                )
                for audio_property_set in audio_property_sets
            ]

            for future in concurrent.futures.as_completed(futures):
                # TODO: try except block?
                progress_bar.update(1)
                file_path, last_modified = future.result()
                cache[file_path] = last_modified

        cache["target_level"] = self.__target_level
        progress_bar.close()

        if not (cache == cache_data):
            self.__caching_processor.write_cache(cache)
