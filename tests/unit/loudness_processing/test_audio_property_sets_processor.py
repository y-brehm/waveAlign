import mock
import unittest
import os

from wavealign.caching.yaml_cache import YamlCache
from wavealign.loudness_processing.clipping_strategy_manager import ClippingStrategyManager
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)

# TODO: write new tests


class TestAudioPropertySetsProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_audio_file_reader = mock.patch(
            "wavealign.loudness_processing.audio_property_sets_processor.AudioFileReader"
        ).start()
        self.mock_audio_file_processor = mock.patch(
            "wavealign.loudness_processing.audio_property_sets_processor.AudioFileProcessor"
        ).start()
        self.mock_getlogger = mock.patch(
            "wavealign.data_collection.audio_property_sets_reader.logging.getLogger"
        ).start()
        self.mock_logger = mock.MagicMock()
        self.mock_getlogger.return_value = self.mock_logger
        self.fake_output_path = os.path.join("path", "to", "fake_output")

    def tearDown(self):
        mock.patch.stopall()

    def test_process_all_clipping(self):
        clipping_strategy_manager = ClippingStrategyManager(
            target_level=-10,
            clipping_strategy=ClippingStrategy.SKIP
            )
        yaml_cache = YamlCache(processed_files=[], target_level=-10)

        processor = AudioPropertySetsProcessor(
            clipping_strategy_manager=clipping_strategy_manager,
            target_level=-10,
            cache_data=yaml_cache
                )

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
        cache_data = processor.process(test_files, target_level, self.fake_output_path)

        self.mock_getlogger.assert_called_once_with("CLIPPING STRATEGY MANAGER")
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
        cache_data = processor.process(test_files, target_level, self.fake_output_path)

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
        self.mock_audio_file_processor.return_value.process.assert_called_once_with(
            test_files[0],
            target_level,
            os.path.join(self.fake_output_path, "file1.wav"),
            self.mock_audio_file_reader.return_value.read.return_value,
        )
        self.mock_logger.warning.assert_called_once_with(
            "file2.wav was clipped, clipping strategy: ClippingStrategy.SKIP"
        )

        self.assertDictEqual(cache_data, {"file1.wav": 1234, "target_level": -10})
