from dataclasses import dataclass


@dataclass
class AudioMetadata:
    num_channels: float
    artwork: bytearray
    codec_name: str
    bit_rate: int
    sample_rate: int
