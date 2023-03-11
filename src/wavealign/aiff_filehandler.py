import music_tag
import numpy as np

from soundfile import write, read


class AiffFileHandler:
    def __init__(self):
        self.artwork = None
        self.sample_rate = None

    def read(self, filepath: str) -> None:
        metadata = music_tag.load_file(filepath)
        self.artwork = metadata['artwork']

        audio_data, self.sample_rate = read(filepath)

    def write(self, filepath: str, audio_data: np.array) -> None:
        write("test_output.aiff",
              audio_data,
              self.sample_rate,
              subtype='PCM_16',
              format='AIFF')

        metadata = music_tag.load_file("test_output.aiff")
        metadata['artwork'] = self.artwork
        metadata.save()
