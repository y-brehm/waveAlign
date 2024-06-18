import os
import yaml
from dataclasses import is_dataclass, asdict

from wavealign.utility.convert_dict_to_dataclass import convert_dict_to_dataclass
from wavealign.caching.yaml_cache import YamlCache


class YamlCacheProcessor:
    def __init__(self, cache_path: str) -> None:
        self.__cache_path = cache_path
        self.__cache_signature = ".wavealign_cache.yaml"
        if not cache_path:
            raise ValueError("Cache path must be provided")

    def read_cache(self) -> YamlCache | None:
        cache_file_path = os.path.join(self.__cache_path, self.__cache_signature)

        if not os.path.exists(cache_file_path):
            return None

        with open(cache_file_path, "r") as cache_file:
            yaml_dict = yaml.safe_load(cache_file)
            return convert_dict_to_dataclass(YamlCache, yaml_dict)

    def write_cache(self, cache_data: YamlCache) -> None:
        if not is_dataclass(cache_data):
            raise ValueError("Expected a YamlCache dataclass instance.")

        cache_path = os.path.join(self.__cache_path, self.__cache_signature)
        data = asdict(cache_data)

        with open(cache_path, "w") as cache_file:
            yaml.dump(data, cache_file, default_flow_style=False)
