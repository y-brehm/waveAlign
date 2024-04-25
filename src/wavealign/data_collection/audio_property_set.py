from dataclasses import dataclass

from wavealign.data_collection.audio_metadata import AudioMetadata


@dataclass
class AudioPropertySet:
    file_path: str
    original_lufs_level: float
    original_peak_level: float
    metadata: AudioMetadata
