from dataclasses import dataclass
from numpy import ndarray


@dataclass
class AudioFileSpecSet:
    file_path: str
    audio_data: ndarray
    original_lufs: float
    sample_rate: int
    artwork: bytearray
    codec_name: str
