import os

from wavealign.caching.yaml_cache import YamlCache
# TODO: add logging


class CacheManager:
    def __init__(self, cache_data: YamlCache | None, target_level: int) -> None:
        self.__cache_data = cache_data
        self.__target_level = target_level

    def is_cached(self, file_path: str) -> bool:
        last_modified = os.path.getmtime(file_path)
        if self.__cache_data is None:
            print("Cache is invalid.")
            return False

        if self.__cache_data.target_level != self.__target_level:
            print("Target level has changed. Cache is invalid.")
            return False

        for single_file_cache in self.__cache_data.processed_files:
            if (
                single_file_cache.file_path == file_path
                and single_file_cache.last_modified == last_modified
            ):
                print(f"CacheManage has found {file_path} in cache. Skipping processing.")
                return True

        print(f"CacheManage has not found {file_path} in cache. Processing.")
        return False
