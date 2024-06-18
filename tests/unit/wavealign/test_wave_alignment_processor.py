import unittest
import mock
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.caching.yaml_cache_processor import YamlCacheProcessor
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)
from wavealign.wave_alignment_processor import (
    WaveAlignmentProcessor,
)

# TODO: use mock.patch.object also for other tests (seems cleaner)


class TestWaveAlignmentProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_read_cache = mock.patch.object(
            YamlCacheProcessor, "read_cache", return_value={}
        ).start()
        self.mock_write_cache = mock.patch.object(
            YamlCacheProcessor, "write_cache"
        ).start()
        self.mock_audio_read = mock.patch.object(
            AudioPropertySetsReader, "read", return_value=([])
        ).start()
        self.mock_audio_process = mock.patch.object(
            AudioPropertySetsProcessor, "process", return_value=({})
        ).start()
        self.mock_ensure_path_exists = mock.patch(
            "wavealign.wave_alignment_processor.ensure_path_exists"
        ).start()
        self.mock_read_cache.return_value = {"file1": 123}

        self.processor = WaveAlignmentProcessor(
            input_path="input_path",
            output_path="output_path",
            window_size=WindowSize.LUFS_S,
            target_level=10,
            clipping_strategy=ClippingStrategy.SKIP,
        )

    def tearDown(self):
        mock.patch.stopall()

    def test_process(self):
        self.processor.process()

        self.mock_ensure_path_exists.assert_called_once_with("output_path")
        self.assertTrue(self.mock_read_cache.call_count, 2)
        self.mock_audio_read.assert_called_once()
        self.mock_audio_process.assert_called_once_with([], 10, "output_path")
        self.mock_write_cache.assert_called_once()

    def test_process_same_cache(self):
        self.mock_audio_process.return_value = {"file1": 123}

        self.processor.process()

        self.mock_write_cache.assert_not_called()

    def test_process_cache_changed(self):
        self.mock_audio_process.return_value = {"file2": 456}

        self.processor.process()

        self.mock_write_cache.assert_called_once()
