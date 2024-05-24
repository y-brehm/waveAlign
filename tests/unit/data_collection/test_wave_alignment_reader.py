import unittest
import mock
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.data_collection.audio_property_sets_analyzer import (
    AudioPropertySetsAnalyzer,
)
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.wave_alignment_reader import WaveAlignmentReader


class TestWaveAlignmentReader(unittest.TestCase):
    def setUp(self):
        self.mock_audio_read = mock.patch.object(
            AudioPropertySetsReader, "read", return_value=[]
        ).start()
        self.mock_audio_analyze = mock.patch.object(
            AudioPropertySetsAnalyzer, "detect_target_value", return_value=-10
        ).start()
        self.mock_print = mock.patch("builtins.print").start()

        self.reader = WaveAlignmentReader(
            input_path="input_path",
            window_size=WindowSize.LUFS_S,
        )

    def tearDown(self):
        mock.patch.stopall()

    def test_read(self):
        audio_property_sets, library_dependent_target_level = self.reader.read()

        self.assertEqual(audio_property_sets, [])
        self.assertEqual(library_dependent_target_level, -10)

        self.mock_audio_read.assert_called_once()
        self.mock_audio_analyze.assert_called_once_with([])

    def test_read_with_audio_property_sets(self):
        audio_property_set = AudioPropertySet(
            file_path="file_path",
            last_modified=123,
            original_peak_level=-1,
            original_lufs_level=-10,
            metadata=mock.MagicMock(),
        )
        self.mock_audio_read.return_value = [audio_property_set]

        audio_property_sets, library_dependent_target_level = self.reader.read()

        self.assertEqual(audio_property_sets, [audio_property_set])
        self.assertEqual(library_dependent_target_level, -10)

        self.mock_audio_read.assert_called_once()
        self.mock_audio_analyze.assert_called_once_with([audio_property_set])
        self.mock_print.assert_any_call("FILE: file_path ORIGINAL LUFS: -10.00 dB LUFS_S ORIGINAL PEAK: -1.00")
        self.mock_print.assert_any_call("Library dependent target level: -10 dB LUFS_S")
