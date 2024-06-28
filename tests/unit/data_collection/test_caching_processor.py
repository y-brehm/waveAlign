import mock
import unittest
from unittest.mock import mock_open

from wavealign.caching.yaml_cache import YamlCache
from wavealign.caching.yaml_cache_processor import YamlCacheProcessor


class TestCachingProcessor(unittest.TestCase):
    @mock.patch("wavealign.caching.yaml_cache_processor.os.path.exists")
    def test_read_cache_non_existent(self, mock_exists):
        mock_exists.return_value = False

        result = YamlCacheProcessor("/fake/path").read_cache()

        self.assertEqual(result, None)

    @mock.patch("builtins.open", new_callable=mock_open, read_data="key: value\n")
    @mock.patch("os.path.exists")
    @mock.patch("wavealign.caching.yaml_cache_processor.yaml.safe_load")
    @mock.patch("wavealign.caching.yaml_cache_processor.convert_dict_to_dataclass")
    def test_read_cache_exists(
        self, mock_convert_dict_to_dataclass, mock_yaml_load, mock_exists, mock_open
    ):
        mock_exists.return_value = True
        fake_yaml_dict = {"key": "value"}
        dummy_dataclass = mock.MagicMock()

        mock_yaml_load.return_value = fake_yaml_dict
        mock_convert_dict_to_dataclass.return_value = dummy_dataclass

        result = YamlCacheProcessor("/fake/path").read_cache()

        mock_yaml_load.assert_called_once_with(mock_open())
        mock_convert_dict_to_dataclass.assert_called_once_with(
            YamlCache, fake_yaml_dict
        )
        self.assertEqual(result, dummy_dataclass)

    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("wavealign.caching.yaml_cache_processor.yaml.dump")
    def test_write_cache(self, mock_yaml_dump, mock_open):
        cache_data = YamlCache(processed_files=[], target_level=0.5)

        cache_dict = {"processed_files": [], "target_level": 0.5}

        YamlCacheProcessor("/fake/path").write_cache(cache_data)

        mock_open.assert_called_once_with("/fake/path/.wavealign_cache.yaml", "w")
        mock_yaml_dump.assert_called_with(
            cache_dict, mock_open(), default_flow_style=False
        )

    def test_no_dataclass_instance(self):
        with self.assertRaises(ValueError):
            YamlCacheProcessor("/fake/path").write_cache({})

    def test_init_no_cache_path(self):
        with self.assertRaises(ValueError):
            YamlCacheProcessor("")
