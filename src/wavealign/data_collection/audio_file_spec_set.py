from dataclasses import dataclass
from numpy import ndarray

from wavealign.data_collection.audio_metadata import AudioMetadata


@dataclass
class AudioFileSpecSet:
    file_path: str
    audio_data: ndarray
    original_audio_level: float
    metadata: AudioMetadata
