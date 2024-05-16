import os
import glob
import yaml
import time


class CachingProcessor:
    def __init__(self, cache_path: str):
        self.__cache_path = cache_path
        self.__cache_signature = "wavealign_cache.yaml"

    def read_cache(self) -> dict:
        cache_files = glob.glob(
            os.path.join(self.__cache_path, f"*_{self.__cache_signature}")
        )
        if cache_files:
            latest_cache_file = max(cache_files, key=os.path.getctime)
            with open(latest_cache_file, "r") as cache_file:
                return yaml.safe_load(cache_file)
        return {}

    def write_cache(self, cache_data: dict) -> None:
        new_timestamp = time.strftime("%Y%m%d-%H%M%S")
        cache_path = os.path.join(
            self.__cache_path, f"{new_timestamp}_{self.__cache_signature}"
        )
        with open(cache_path, "w") as cache_file:
            yaml.dump(cache_data, cache_file, default_flow_style=False)
