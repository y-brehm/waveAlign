import os
import glob
import mock
import unittest
import tempfile

from scipy.io import wavfile
from pyloudnorm import Meter
from mutagen import aiff

from src.wavealign.wave_alignment_processor import WaveAlignmentProcessor
from src.wavealign.loudness_processing.window_size import WindowSize

# TODO: Fix scipy wav file chunk read error (remove unreadable header from test files)


class TestWaveAlignmentProcessor(unittest.TestCase):
    def setUp(self):
        self.input_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "test_files")
        )
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = self.temp_dir.name
        self.mock_logger = mock.MagicMock()
        self.mock_getlogger = mock.patch(
            "wavealign.data_collection.audio_property_sets_reader.logging.getLogger"
        ).start()
        self.mock_getlogger.return_value = self.mock_logger
        self.processor = WaveAlignmentProcessor(
            self.input_path,
            self.output_path,
            window_size=WindowSize.LUFS_I,
            target_level=-14,
        )

    def tearDown(self):
        self.temp_dir.cleanup()
        for file in glob.glob(os.path.join(self.input_path, ".*.yaml")):
            os.remove(file)
        mock.patch.stopall()

    def test_processing_successful(self):
        self.processor.process()
        for audio_file in get_file_paths_with_ending(self.output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)

    def test_processing_successful_skip_existing_files(self):
        self.processor.process()
        self.processor.process()

        for audio_file in get_file_paths_with_ending(self.output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)

    def test_full_transfer_of_metadata(self):
        self.processor.process()
        for audio_file in get_file_paths_with_ending(self.output_path, ".aiff"):
            input_file = os.path.join(self.input_path, os.path.basename(audio_file))
            output_metadata = aiff.AIFF(audio_file)
            input_metadata = aiff.AIFF(input_file)

            for tag in input_metadata.keys():
                self.assertEqual(input_metadata[tag], output_metadata[tag])

    def test_successful_double_processing(self):
        self.processor.process()

        new_processor = WaveAlignmentProcessor(
            self.output_path,
            self.output_path,
            window_size=WindowSize.LUFS_I,
            target_level=-16,
        )

        try:
            new_processor.process()
        except Exception as e:
            self.fail(f"Raised the following excepton {e}")


def get_file_paths_with_ending(directory: str, ending: str):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ending):
                file_paths.append(os.path.join(root, file))

    return file_paths
