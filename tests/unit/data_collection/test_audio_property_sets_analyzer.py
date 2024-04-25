import mock
import unittest

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_property_sets_analyzer import (
    AudioPropertySetsAnalyzer,
)


class TestAudioPropertySetsAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AudioPropertySetsAnalyzer()

    def test_detect_target_value(self):
        audio_property_sets = [
            AudioPropertySet(
                "dummy_path",
                original_peak_level=-0.5,
                original_lufs_level=-14.0,
                metadata=mock.MagicMock(),
            ),
            AudioPropertySet(
                "dummy_path",
                original_peak_level=-2.0,
                original_lufs_level=-15.0,
                metadata=mock.MagicMock(),
            ),
            AudioPropertySet(
                "dummy_path",
                original_peak_level=-6.0,
                original_lufs_level=-18.0,
                metadata=mock.MagicMock(),
            ),
        ]

        result = self.analyzer.detect_target_value(audio_property_sets)

        expected_result = -18
        self.assertEqual(result, expected_result)

    def test_detect_target_value_single_set(self):
        audio_property_sets = [
            AudioPropertySet(
                "dummy_path",
                original_peak_level=-1.0,
                original_lufs_level=-14.0,
                metadata=mock.MagicMock(),
            ),
        ]

        result = self.analyzer.detect_target_value(audio_property_sets)

        expected_result = -13

        self.assertEqual(result, expected_result)

    def test_detect_target_value_empty_set(self):
        audio_property_sets = []

        with self.assertRaises(ValueError):
            self.analyzer.detect_target_value(audio_property_sets)
