import mock
import unittest
import os
from unittest.mock import mock_open

from wavealign.caching.yaml_cache import YamlCache
from wavealign.caching.yaml_cache_processor import YamlCacheProcessor


class TestYamlCacheProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_open = mock.patch("builtins.open", new_callable=mock_open).start()
        self.mock_os_path_exists = mock.patch("os.path.exists").start()
        self.fake_path = os.path.join("fake", "path")

    def tearDown(self):
        mock.patch.stopall()

    def test_read_cache_non_existent(self):
        self.mock_os_path_exists.return_value = False

        result = YamlCacheProcessor(self.fake_path).read_cache()

        self.assertEqual(result, None)

    @mock.patch("wavealign.caching.yaml_cache_processor.yaml.safe_load")
    @mock.patch("wavealign.caching.yaml_cache_processor.DictToDataclassConverter")
    def test_read_cache_exists(self, mock_dict_to_dataclass_converter, mock_yaml_load):
        self.mock_os_path_exists.return_value = True
        fake_yaml_dict = {"key": "value"}
        dummy_dataclass = mock.MagicMock()

        mock_yaml_load.return_value = fake_yaml_dict
        mock_dict_to_dataclass_converter.return_value.process.return_value = (
            dummy_dataclass
        )

        result = YamlCacheProcessor(self.fake_path).read_cache()

        mock_yaml_load.assert_called_once_with(self.mock_open())
        mock_dict_to_dataclass_converter.return_value.process.assert_called_once_with(
            YamlCache, fake_yaml_dict
        )
        self.assertEqual(result, dummy_dataclass)

    @mock.patch("wavealign.caching.yaml_cache_processor.yaml.dump")
    def test_write_cache(self, mock_yaml_dump):
        cache_data = YamlCache(processed_files=[], target_level=0.5)

        cache_dict = {"processed_files": [], "target_level": 0.5}

        YamlCacheProcessor(self.fake_path).write_cache(cache_data)

        self.mock_open.assert_called_once_with(
            os.path.join("fake", "path", ".wavealign_cache.yaml"), "w"
        )
        mock_yaml_dump.assert_called_with(
            cache_dict, self.mock_open(), default_flow_style=False
        )
