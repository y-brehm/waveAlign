import unittest
from unittest import mock

from wavealign.caching.cache_validator import CacheValidator


class TestCacheValidator(unittest.TestCase):
    def setUp(self):
        self.mock_getmtime = mock.patch(
            "wavealign.caching.cache_validator.os.path.getmtime"
        ).start()
        self.mock_getlogger = mock.patch(
            "wavealign.caching.cache_validator.logging.getLogger"
        ).start()
        self.mock_logger = mock.MagicMock()
        self.mock_getlogger.return_value = self.mock_logger

    def tearDown(self):
        mock.patch.stopall()

    def test_is_cached_with_no_cache_data(self):
        cache_validator = CacheValidator(cache_data=None, target_level=1)
        self.mock_getmtime.return_value = 1234567890

        result = cache_validator.is_cached("dummy_path")

        self.assertFalse(result)
        self.mock_logger.debug.assert_called_with("Cache is invalid.")

    def test_is_cached_with_different_target_level(self):
        mock_cache_data = mock.MagicMock()
        mock_cache_data.target_level = 2
        cache_validator = CacheValidator(cache_data=mock_cache_data, target_level=1)
        self.mock_getmtime.return_value = 1234567890

        result = cache_validator.is_cached("dummy_path")

        self.assertFalse(result)
        self.mock_logger.debug.assert_called_with(
            "Target level has changed. Cache is invalid."
        )

    def test_is_cached_file_found_in_cache(self):
        mock_cache_data = mock.MagicMock()
        mock_cache_data.target_level = 1
        mock_cache_data.processed_files = [
            mock.MagicMock(file_path="dummy_path", last_modified=1234567890)
        ]
        cache_validator = CacheValidator(cache_data=mock_cache_data, target_level=1)
        self.mock_getmtime.return_value = 1234567890

        result = cache_validator.is_cached("dummy_path")

        self.assertTrue(result)
        self.mock_logger.debug.assert_called_with(
            "CacheValidator has found dummy_path in cache. Skipping processing."
        )

    def test_is_cached_file_not_found_in_cache(self):
        mock_cache_data = mock.MagicMock()
        mock_cache_data.target_level = 1
        mock_cache_data.processed_files = [
            mock.MagicMock(file_path="other_path", last_modified=1234567890)
        ]
        cache_validator = CacheValidator(cache_data=mock_cache_data, target_level=1)
        self.mock_getmtime.return_value = 1234567890

        result = cache_validator.is_cached("dummy_path")

        self.assertFalse(result)
        self.mock_logger.debug.assert_called_with(
            "CacheValidator has not found dummy_path in cache. Processing."
        )
