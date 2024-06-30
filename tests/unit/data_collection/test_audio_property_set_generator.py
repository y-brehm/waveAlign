import unittest
from unittest import mock
import numpy as np

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_property_set_generator import (
    AudioPropertySetGenerator,
)
from wavealign.caching.levels_cache_finder import LevelsCacheFinder
from wavealign.loudness_processing.window_size import WindowSize


class TestAudioPropertySetGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_audio_file_reader = mock.patch(
            "wavealign.data_collection.audio_property_set_generator.AudioFileReader"
        ).start()
        self.mock_os_path_getmtime = mock.patch(
            "wavealign.data_collection.audio_property_set_generator.os.path.getmtime"
        ).start()
        self.mock_metadata_extractor = mock.patch(
            "wavealign.data_collection.audio_property_set_generator.MetaDataExtractor"
        ).start()
        self.mock_audio_level_extractor = mock.patch(
            "wavealign.data_collection.audio_property_set_generator.AudioLevelExtractor"
        ).start()

        self.mock_audio_file_reader.return_value.read.return_value = np.array(
            [0.0, 1.0, -1.0], dtype=np.float32
        )
        self.mock_metadata_extractor.return_value.extract.return_value = (
            mock.MagicMock()
        )
        self.mock_audio_level_extractor.return_value.extract.side_effect = [-14, -1]
        self.mock_os_path_getmtime.return_value = 1234567890

    def tearDown(self):
        mock.patch.stopall()

    def test_generate_without_cache(self):
        generator = AudioPropertySetGenerator(WindowSize.LUFS_S)
        audio_property_set = generator.generate("dummy_path")

        self.mock_audio_file_reader.return_value.read.assert_called_once_with(
            "dummy_path"
        )
        self.mock_os_path_getmtime.assert_called_once_with("dummy_path")
        self.mock_metadata_extractor.return_value.extract.assert_called_once_with(
            "dummy_path"
        )
        self.assertEqual(
            self.mock_audio_level_extractor.return_value.extract.call_count, 2
        )
        self.assertIsInstance(audio_property_set, AudioPropertySet)
        self.assertEqual(audio_property_set.file_path, "dummy_path")
        self.assertEqual(audio_property_set.original_lufs_level, -14)
        self.assertEqual(audio_property_set.original_peak_level, -1)
        self.assertEqual(
            audio_property_set.metadata,
            self.mock_metadata_extractor.return_value.extract.return_value,
        )
        self.assertEqual(audio_property_set.last_modified, 1234567890)

    def test_generate_with_cache(self):
        mock_cache_finder = mock.MagicMock(spec=LevelsCacheFinder)
        mock_cached_levels = mock.MagicMock()
        mock_cached_levels.lufs = -10
        mock_cached_levels.peak = -2
        mock_cache_finder.get_levels.return_value = mock_cached_levels

        generator = AudioPropertySetGenerator(
            WindowSize.LUFS_S, levels_cache_finder=mock_cache_finder
        )
        audio_property_set = generator.generate("dummy_path")

        self.mock_audio_file_reader.return_value.read.assert_called_once_with(
            "dummy_path"
        )
        self.mock_metadata_extractor.return_value.extract.assert_called_once_with(
            "dummy_path"
        )
        mock_cache_finder.get_levels.assert_called_once_with("dummy_path")
        self.mock_audio_level_extractor.return_value.extract.assert_not_called()
        self.assertIsInstance(audio_property_set, AudioPropertySet)
        self.assertEqual(audio_property_set.file_path, "dummy_path")
        self.assertEqual(audio_property_set.original_lufs_level, -10)
        self.assertEqual(audio_property_set.original_peak_level, -2)
        self.assertEqual(
            audio_property_set.metadata,
            self.mock_metadata_extractor.return_value.extract.return_value,
        )
        self.assertEqual(audio_property_set.last_modified, 1234567890)

    def test_generate_with_cache_miss(self):
        mock_cache_finder = mock.MagicMock(spec=LevelsCacheFinder)
        mock_cache_finder.get_levels.return_value = None

        generator = AudioPropertySetGenerator(
            WindowSize.LUFS_S, levels_cache_finder=mock_cache_finder
        )
        audio_property_set = generator.generate("dummy_path")

        self.mock_audio_file_reader.return_value.read.assert_called_once_with(
            "dummy_path"
        )
        self.mock_metadata_extractor.return_value.extract.assert_called_once_with(
            "dummy_path"
        )
        mock_cache_finder.get_levels.assert_called_once_with("dummy_path")
        self.assertEqual(
            self.mock_audio_level_extractor.return_value.extract.call_count, 2
        )
        self.assertIsInstance(audio_property_set, AudioPropertySet)
        self.assertEqual(audio_property_set.file_path, "dummy_path")
        self.assertEqual(audio_property_set.original_lufs_level, -14)
        self.assertEqual(audio_property_set.original_peak_level, -1)
        self.assertEqual(
            audio_property_set.metadata,
            self.mock_metadata_extractor.return_value.extract.return_value,
        )
        self.assertEqual(audio_property_set.last_modified, 1234567890)
