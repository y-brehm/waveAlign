import unittest
from unittest import mock

from wavealign.caching.levels import Levels
from wavealign.caching.yaml_cache import YamlCache, SingleFileCache
from wavealign.caching.levels_cache_finder import LevelsCacheFinder


class TestLevelsCacheFinder(unittest.TestCase):
    def setUp(self):
        self.mock_getmtime = mock.patch(
            "wavealign.caching.levels_cache_finder.os.path.getmtime"
        ).start()
        self.mock_getlogger = mock.patch(
            "wavealign.caching.levels_cache_finder.logging.getLogger"
        ).start()
        self.mock_logger = mock.MagicMock()
        self.mock_getlogger.return_value = self.mock_logger

    def tearDown(self):
        mock.patch.stopall()

    def test_get_levels_with_no_cache_data(self):
        levels_cache_finder = LevelsCacheFinder(cache_data=None)

        result = levels_cache_finder.get_levels("dummy_path")

        self.assertIsNone(result)

    def test_get_levels_file_found_in_cache(self):
        mock_levels = Levels(lufs=-14.0, peak=-1.0)
        single_file_cache = SingleFileCache(
            file_path="dummy_path", last_modified=1234567890, levels=mock_levels
        )
        yaml_cache = YamlCache(processed_files=[single_file_cache], target_level=-23.0)
        levels_cache_finder = LevelsCacheFinder(cache_data=yaml_cache)
        self.mock_getmtime.return_value = 1234567890

        result = levels_cache_finder.get_levels("dummy_path")

        self.assertEqual(result, mock_levels)
        self.mock_logger.debug.assert_called_with(
            "Found levels for dummy_path in cache."
        )

    def test_get_levels_file_not_found_in_cache(self):
        mock_levels = Levels(lufs=-14.0, peak=-1.0)
        single_file_cache = SingleFileCache(
            file_path="other_path", last_modified=1234567890, levels=mock_levels
        )
        yaml_cache = YamlCache(processed_files=[single_file_cache], target_level=-23.0)
        levels_cache_finder = LevelsCacheFinder(cache_data=yaml_cache)
        self.mock_getmtime.return_value = 1234567890

        result = levels_cache_finder.get_levels("dummy_path")

        self.assertIsNone(result)

    def test_get_levels_file_modified_after_cache(self):
        mock_levels = Levels(lufs=-14.0, peak=-1.0)
        single_file_cache = SingleFileCache(
            file_path="dummy_path", last_modified=1234567890, levels=mock_levels
        )
        yaml_cache = YamlCache(processed_files=[single_file_cache], target_level=-23.0)
        levels_cache_finder = LevelsCacheFinder(cache_data=yaml_cache)
        self.mock_getmtime.return_value = 1234567891

        result = levels_cache_finder.get_levels("dummy_path")

        self.assertIsNone(result)
