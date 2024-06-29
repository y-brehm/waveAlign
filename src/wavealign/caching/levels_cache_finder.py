import os
import logging

from wavealign.caching.levels import Levels
from wavealign.caching.yaml_cache import YamlCache


class LevelsCacheFinder:
    def __init__(self, cache_data: YamlCache | None) -> None:
        self.__cache_data = cache_data
        self.__logger = logging.getLogger(__name__)

    def get_levels(self, file_path: str) -> Levels | None:
        if self.__cache_data is None:
            return None

        last_modified = os.path.getmtime(file_path)

        for single_file_cache in self.__cache_data.processed_files:
            if (
                single_file_cache.file_path == file_path
                and single_file_cache.last_modified == last_modified
            ):
                self.__logger.debug(f"Found levels for {file_path} in cache.")
                return single_file_cache.levels

        return None
