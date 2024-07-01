import os
import unittest
import subprocess
import shutil

from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.gain_calculation_strategy import (
    GainCalculationStrategy,
)
from wavealign.data_collection.audio_level_extractor import (
    AudioLevelExtractor,
)
from wavealign.loudness_processing.retrieve_mp3processor_executable_path import (
    retrieve_mp3processor_executable_path,
)
from wavealign.loudness_processing.window_size import WindowSize


class TestMp3Processor(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(
            self.current_dir,
            "test_files",
            "4832f_c_weighted_white_noise_-10LUFS_added_diracs_stereo.mp3",
        )
        self.temp_file_path = os.path.join(self.current_dir, "test_file1.mp3")
        shutil.copy(self.file_path, self.temp_file_path)

    def tearDown(self):
        os.remove(self.temp_file_path)

    def _read_and_extract_lufs(self, temp_file_path):
        audio_data = AudioFileReader().read(temp_file_path)
        lufs = AudioLevelExtractor(
            GainCalculationStrategy.LUFS, 48000, WindowSize.LUFS_S
        ).extract(audio_data)

        return lufs

    def test_processing_increase(self):
        result = subprocess.run(
            [
                retrieve_mp3processor_executable_path(),
                "-i",
                self.temp_file_path,
                "-g",
                str(5.0),
            ]
        )
        lufs = self._read_and_extract_lufs(self.temp_file_path)
        self.assertEqual(result.returncode, 0)
        self.assertAlmostEqual(lufs, -5.0, delta=0.75)

    def test_processing_decrease(self):
        result = subprocess.run(
            [
                retrieve_mp3processor_executable_path(),
                "-i",
                self.temp_file_path,
                "-g",
                str(-5.0),
            ]
        )
        lufs = self._read_and_extract_lufs(self.temp_file_path)
        self.assertEqual(result.returncode, 0)
        self.assertAlmostEqual(lufs, -15.0, delta=0.75)

    def test_processing_no_change(self):
        result = subprocess.run(
            [
                retrieve_mp3processor_executable_path(),
                "-i",
                self.temp_file_path,
                "-g",
                str(0.0),
            ]
        )
        lufs = self._read_and_extract_lufs(self.temp_file_path)
        self.assertEqual(result.returncode, 0)
        # TODO this tolerance should be smaller
        self.assertAlmostEqual(lufs, -10.0, delta=0.5)
