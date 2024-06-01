import os


class CacheManager:
    def __init__(self, cache_data: dict, target_level: int):
        self.__cache_data = cache_data
        self.__target_level = target_level

    def is_cached(self, file_path: str) -> bool:
        last_modified = os.path.getmtime(file_path)
        if self.__cache_data.get(
            file_path
        ) == last_modified and self.__target_level == self.__cache_data.get(
            "target_level"
        ):
            return True
        return False
