import os

import music_tag
import numpy as np

from soundfile import write, read
from wavealign.loudness_processing.calculation import calculate_lufs
from wavealign.data_collection.audio_spec_set import AudioSpecSet


class AudioFileHandler:
    def __init__(self):
        self.artwork = None
        self.sample_rate = None

    def read(self, file_path: str) -> AudioSpecSet:
        metadata = music_tag.load_file(file_path)
        self.artwork = metadata['artwork']

        audio_data, self.sample_rate = read(file_path)

        original_lufs = calculate_lufs(audio_data, self.sample_rate)
        original_file_format = os.path.splitext(file_path)[1]

        return AudioSpecSet(
            file_path=file_path,
            audio_data=audio_data,
            sample_rate=int(self.sample_rate),
            original_lufs=original_lufs,
            original_file_extension=original_file_format
        )

    def write(self, filepath: str, audio_data: np.array) -> None:
        write(filepath,
              audio_data,
              self.sample_rate,
              subtype='PCM_16')

        metadata = music_tag.load_file(filepath)
        metadata['artwork'] = self.artwork
        metadata.save()
