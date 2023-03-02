from dataclasses import dataclass
from numpy import ndarray


@dataclass
class AudioSpecSet:
    file_path: str
    audio_data: ndarray
    original_lufs: float
    sample_rate: int
    original_file_extension: str
