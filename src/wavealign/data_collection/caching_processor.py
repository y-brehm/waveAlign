import os
import yaml


class CachingProcessor:
    def __init__(self, cache_path: str):
        self.__cache_path = cache_path
        self.__cache_signature = "wavealign_cache.yaml"
        if not cache_path:
            raise ValueError("Cache path must be provided")

    def read_cache(self) -> dict:
        cache_file_path = os.path.join(self.__cache_path, self.__cache_signature)

        if not os.path.exists(cache_file_path):
            return {}

        with open(cache_file_path, "r") as cache_file:
            return yaml.safe_load(cache_file)

    def write_cache(self, cache_data: dict) -> None:
        cache_path = os.path.join(self.__cache_path, self.__cache_signature)

        with open(cache_path, "w") as cache_file:
            yaml.dump(cache_data, cache_file, default_flow_style=False)
