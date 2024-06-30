from dataclasses import dataclass

from wavealign.caching.single_file_cache import SingleFileCache


@dataclass
class YamlCache:
    processed_files: list[SingleFileCache]
    target_level: float
