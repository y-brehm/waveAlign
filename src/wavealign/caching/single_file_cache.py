from dataclasses import dataclass

from wavealign.caching.levels import Levels


@dataclass
class SingleFileCache:
    file_path: str
    last_modified: float
    levels: Levels
