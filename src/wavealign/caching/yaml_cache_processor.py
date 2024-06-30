import os
import yaml
from dataclasses import asdict

from wavealign.utility.dict_to_dataclass_converter import DictToDataclassConverter
from wavealign.caching.yaml_cache import YamlCache


class YamlCacheProcessor:
    def __init__(self, cache_path: str) -> None:
        self.__cache_path = cache_path
        self.__cache_signature = ".wavealign_cache.yaml"
        self.__dict_to_dataclass_converter = DictToDataclassConverter()

    def read_cache(self) -> YamlCache | None:
        cache_file_path = os.path.join(self.__cache_path, self.__cache_signature)

        if not os.path.exists(cache_file_path):
            return None

        with open(cache_file_path, "r") as cache_file:
            yaml_dict = yaml.safe_load(cache_file)
            return self.__dict_to_dataclass_converter.process(YamlCache, yaml_dict)

    def write_cache(self, cache_data: YamlCache) -> None:
        cache_path = os.path.join(self.__cache_path, self.__cache_signature)
        data = asdict(cache_data)

        with open(cache_path, "w") as cache_file:
            yaml.dump(data, cache_file, default_flow_style=False)
