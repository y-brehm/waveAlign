import unittest
import mock

from unittest.mock import mock_open
from wavealign.data_collection.caching_processor import CachingProcessor


class TestCachingProcessor(unittest.TestCase):
    @mock.patch("os.path.exists")
    def test_read_cache_non_existent(self, mock_exists):
        mock_exists.return_value = False

        result = CachingProcessor("/fake/path").read_cache()

        self.assertEqual(result, {})

    @mock.patch("builtins.open", new_callable=mock_open, read_data="key: value\n")
    @mock.patch("wavealign.data_collection.caching_processor.os.path.exists")
    @mock.patch("wavealign.data_collection.caching_processor.yaml.safe_load")
    def test_read_cache_exists(self, mock_yaml_load, mock_exists, mock_open):
        mock_exists.return_value = True

        result = CachingProcessor("/fake/path").read_cache()

        mock_yaml_load.assert_called_once_with(mock_open())
        self.assertEqual(result, mock_yaml_load.return_value)

    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("wavealign.data_collection.caching_processor.yaml.dump")
    def test_write_cache(self, mock_yaml_dump, mock_open):
        cache_data = {"key": "value"}
        CachingProcessor("/fake/path").write_cache(cache_data)

        mock_open.assert_called_once_with("/fake/path/.wavealign_cache.yaml", "w")
        mock_yaml_dump.assert_called_with(
            cache_data, mock_open(), default_flow_style=False
        )

    def test_init_no_cache_path(self):
        with self.assertRaises(ValueError):
            CachingProcessor("")
