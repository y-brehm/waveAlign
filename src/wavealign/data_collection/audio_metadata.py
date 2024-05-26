from dataclasses import dataclass

from mutagen import FileType

@dataclass
class AudioMetadata:
    num_channels: float
    metadata: FileType
    codec_name: str
    bit_rate: str
    sample_rate: int
    start_time: float
