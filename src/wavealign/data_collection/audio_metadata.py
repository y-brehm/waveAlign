from dataclasses import dataclass

from music_tag.file import AudioFile

@dataclass
class AudioMetadata:
    num_channels: float
    metadata: AudioFile
    codec_name: str
    bit_rate: str
    sample_rate: int
