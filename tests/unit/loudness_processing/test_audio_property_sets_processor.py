import mock
import unittest

from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)


class TestAudioPropertySetsProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_audio_file_reader = mock.patch(
            "wavealign.loudness_processing.audio_property_sets_processor.AudioFileReader"
        ).start()
        self.mock_audio_file_writer = mock.patch(
            "wavealign.loudness_processing.audio_property_sets_processor.AudioFileWriter"
        ).start()
        self.mock_clipping_detected = mock.patch(
            "wavealign.loudness_processing.audio_property_sets_processor.clipping_detected"
        ).start()
        self.mock_align_waveform_to_target = mock.patch(
            "wavealign.loudness_processing.audio_property_sets_processor.align_waveform_to_target"
        ).start()
        self.mock_getlogger = mock.patch(
            "wavealign.data_collection.audio_property_sets_reader.logging.getLogger"
        ).start()
        self.mock_logger = mock.MagicMock()
        self.mock_getlogger.return_value = self.mock_logger

    def tearDown(self):
        mock.patch.stopall()

    def test_process_all_clipping(self):
        processor = AudioPropertySetsProcessor(
            clipping_strategy=ClippingStrategy.SKIP, cache_data={}
        )
        self.mock_clipping_detected.return_value = True

        fake_output_path = "path/to/fake_output"
        fake_metadata1 = mock.MagicMock()
        fake_metadata2 = mock.MagicMock()

        test_files = [
            AudioPropertySet(
                file_path="file1.wav",
                last_modified=1234,
                original_peak_level=-1,
                original_lufs_level=-14,
                metadata=fake_metadata1,
            ),
            AudioPropertySet(
                file_path="file2.wav",
                last_modified=5678,
                original_peak_level=-2,
                original_lufs_level=-15,
                metadata=fake_metadata2,
            ),
        ]
        target_level = -10
        cache_data = processor.process(test_files, target_level, fake_output_path)

        self.mock_clipping_detected.assert_has_calls(
            [
                mock.call(-1, -14, target_level),
                mock.call(-2, -15, target_level),
            ]
        )
        self.mock_getlogger.assert_called_once_with("AUDIO PROCESSOR")
        self.mock_logger.warning.assert_has_calls(
            [
                mock.call(
                    "file1.wav was clipped, clipping strategy: ClippingStrategy.SKIP"
                ),
                mock.call(
                    "file2.wav was clipped, clipping strategy: ClippingStrategy.SKIP"
                ),
            ]
        )
        self.assertDictEqual(cache_data, {"target_level": -10})

    def test_process_one_file_clipping(self):
        processor = AudioPropertySetsProcessor(
            clipping_strategy=ClippingStrategy.SKIP, cache_data={}
        )
        self.mock_clipping_detected.side_effect = [False, True]
        self.mock_align_waveform_to_target.return_value = "aligned_audio_data"

        fake_output_path = "path/to/fake_output"
        fake_metadata1 = mock.MagicMock()
        fake_metadata2 = mock.MagicMock()

        test_files = [
            AudioPropertySet(
                file_path="file1.wav",
                last_modified=1234,
                original_peak_level=-1,
                original_lufs_level=-14,
                metadata=fake_metadata1,
            ),
            AudioPropertySet(
                file_path="file2.wav",
                last_modified=5678,
                original_peak_level=-2,
                original_lufs_level=-18,
                metadata=fake_metadata2,
            ),
        ]
        target_level = -10
        cache_data = processor.process(test_files, target_level, fake_output_path)

        self.mock_getlogger.assert_called_once_with("AUDIO PROCESSOR")

        self.mock_clipping_detected.assert_has_calls(
            [
                mock.call(-1, -14, target_level),
                mock.call(-2, -18, target_level),
            ]
        )
        self.mock_audio_file_reader.return_value.read.assert_called_once_with(
            "file1.wav"
        )
        self.mock_align_waveform_to_target.assert_called_once_with(
            self.mock_audio_file_reader.return_value.read.return_value,
            -14,
            target_level,
        )
        self.mock_audio_file_writer.return_value.write.assert_called_once_with(
            "path/to/fake_output/file1.wav", "aligned_audio_data", fake_metadata1
        )
        self.mock_logger.warning.assert_called_once_with(
            "file2.wav was clipped, clipping strategy: ClippingStrategy.SKIP"
        )

        self.assertDictEqual(cache_data, {"file1.wav": 1234, "target_level": -10})
