import os
import glob
import shutil
import mock
import unittest

from io import StringIO
from scipy.io import wavfile
from pyloudnorm import Meter

from src.wavealign.wave_alignment_processor import WaveAlignmentProcessor
from src.wavealign.loudness_processing.window_size import WindowSize

# TODO: Fix scipy wav file chunk read error (remove unreadable header from test files)


class TestWaveAlignmentProcessor(unittest.TestCase):
    def setUp(self):
        self.__input_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "test_files")
        )
        self.__output_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "temp_files")
        )
        os.makedirs(self.__output_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.__output_path)
        for file in glob.glob(os.path.join(self.__input_path, "*.yaml")):
            os.remove(file)

    def test_processing_successful(self):
        processor = WaveAlignmentProcessor(
            self.__input_path,
            self.__output_path,
            window_size=WindowSize.LUFS_I,
            target_level=-14,
        )
        processor.process()
        for audio_file in get_file_paths_with_ending(self.__output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)

    def test_processing_successful_skip_existing_files(self):
        processor = WaveAlignmentProcessor(
            self.__input_path,
            self.__output_path,
            window_size=WindowSize.LUFS_I,
            target_level=-14,
        )
        processor.process()
        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            processor.process()
            self.assertIn("Skipping already processed file", mock_stdout.getvalue())

        for audio_file in get_file_paths_with_ending(self.__output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)


def get_file_paths_with_ending(directory: str, ending: str):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ending):
                file_paths.append(os.path.join(root, file))
    return file_paths
