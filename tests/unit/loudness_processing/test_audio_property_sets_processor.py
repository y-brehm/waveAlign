import mock
import unittest

from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)


class TestAudioPropertySetsProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = AudioPropertySetsProcessor(
            clipping_strategy=ClippingStrategy.SKIP
        )

    @mock.patch(
        "wavealign.loudness_processing.audio_property_sets_processor.clipping_detected"
    )
    def test_clipped_files_addition(self, mock_clipping_detected):
        mock_clipping_detected.return_value = True

        fake_output_path = "path/to/fake_output"
        fake_metadata1 = mock.MagicMock()
        fake_metadata2 = mock.MagicMock()

        test_files = [
            AudioPropertySet(
                file_path="file1.wav",
                original_peak_level=-1,
                original_lufs_level=-14,
                metadata=fake_metadata1,
            ),
            AudioPropertySet(
                file_path="file2.wav",
                original_peak_level=-2,
                original_lufs_level=-15,
                metadata=fake_metadata2,
            ),
        ]
        target_level = -10
        clipped_files = self.processor.process(
            test_files, target_level, fake_output_path
        )

        mock_clipping_detected.assert_has_calls(
            [
                mock.call(-1, -14, target_level),
                mock.call(-2, -15, target_level),
            ]
        )

        expected_files = [
            "file1.wav was clipped, clipping strategy: SKIP",
            "file2.wav was clipped, clipping strategy: SKIP",
        ]
        self.assertListEqual(clipped_files, expected_files)


# TODO: Add more tests
