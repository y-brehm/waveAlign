import os
import glob
import shutil
import mock
import unittest

from io import StringIO
from scipy.io import wavfile
from pyloudnorm import Meter

from src.wavealign.wave_alignment_processor import WaveAlignmentProcessor
from src.wavealign.data_collection.audio_file_reader import AudioFileReader
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
        self.__processor = WaveAlignmentProcessor(
            self.__input_path,
            self.__output_path,
            window_size=WindowSize.LUFS_I,
            target_level=-14,
        )

    def tearDown(self):
        shutil.rmtree(self.__output_path)
        for file in glob.glob(os.path.join(self.__input_path, "*.yaml")):
            os.remove(file)

    def test_processing_successful(self):
        self.__processor.process()
        for audio_file in get_file_paths_with_ending(self.__output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)

    def test_processing_successful_skip_existing_files(self):
        self.__processor.process()
        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.__processor.process()
            self.assertIn("Skipping already processed file", mock_stdout.getvalue())

        for audio_file in get_file_paths_with_ending(self.__output_path, ".wav"):
            sample_rate, audio_data = wavfile.read(audio_file)
            meter = Meter(sample_rate)
            loudness = meter.integrated_loudness(audio_data)
            self.assertAlmostEqual(loudness, -14, delta=0.5)

    def test_length_of_wav_audio_file_stays_the_same(self):
        self.__processor.process()
        for audio_file in get_file_paths_with_ending(self.__output_path, ".wav"):
            _, audio_data = wavfile.read(audio_file)
            _, original_audio_data = wavfile.read(
                os.path.join(self.__input_path, os.path.basename(audio_file))
            )
            self.assertEqual(len(audio_data), len(original_audio_data))

    def test_length_of_mp3_audio_file_stays_the_same(self):
        audio_file_reader = AudioFileReader()
        self.__processor.process()
        for audio_file in get_file_paths_with_ending(self.__output_path, ".mp3"):
            audio_data = audio_file_reader.read(audio_file)
            original_audio_data = audio_file_reader.read(
                os.path.join(self.__input_path, os.path.basename(audio_file))
            )
            self.assertEqual(len(audio_data), len(original_audio_data))


def get_file_paths_with_ending(directory: str, ending: str):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ending):
                file_paths.append(os.path.join(root, file))

    return file_paths
