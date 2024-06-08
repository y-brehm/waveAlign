from dataclasses import dataclass


@dataclass
class SingleFileCache:
    file_path: str
    last_modified: str
