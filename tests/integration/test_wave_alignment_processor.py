import os
import shutil
import unittest

from scipy.io import wavfile
from pyloudnorm import Meter

from src.wavealign.wave_alignment_processor import WaveAlignmentProcessor
from src.wavealign.loudness_processing.window_size import WindowSize


class TestWaveAlignmentProcessor(unittest.TestCase):
    def setUp(self):
        self.__processor = WaveAlignmentProcessor()
        self.__input_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "test_files")
        )
        self.__output_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "temp_files")
        )
        os.makedirs(self.__output_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.__output_path)

    def test_processing_successful(self):
        problem_files = self.__processor.process(
            self.__input_path,
            self.__output_path,
            window_size=WindowSize.LUFS_I,
            user_target_level=-14,
        )
        for audio_file in get_file_paths_with_ending(self.__output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)

        self.assertEqual(len(problem_files), 0)

    # TODO: Add more tests


def get_file_paths_with_ending(directory: str, ending: str):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ending):
                file_paths.append(os.path.join(root, file))
    return file_paths
