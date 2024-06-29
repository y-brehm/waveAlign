import os
import logging

from wavealign.caching.yaml_cache import YamlCache


class CacheManager:
    def __init__(self, cache_data: YamlCache | None, target_level: int) -> None:
        self.__cache_data = cache_data
        self.__target_level = target_level
        self.__logger = logging.getLogger(__name__)

    def is_cached(self, file_path: str) -> bool:
        last_modified = os.path.getmtime(file_path)
        if self.__cache_data is None:
            self.__logger.debug("Cache is invalid.")
            return False

        if self.__cache_data.target_level != self.__target_level:
            self.__logger.debug("Target level has changed. Cache is invalid.")
            return False

        for single_file_cache in self.__cache_data.processed_files:
            if (
                single_file_cache.file_path == file_path
                and single_file_cache.last_modified == last_modified
            ):
                self.__logger.debug(
                    f"CacheManager has found {file_path} in cache. Skipping processing."
                )
                return True

        self.__logger.debug(f"CacheManager has not found {file_path} in cache. Processing.")
        return False
