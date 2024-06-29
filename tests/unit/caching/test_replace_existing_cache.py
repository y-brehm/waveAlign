import mock
import unittest
from wavealign.caching.single_file_cache import SingleFileCache

from wavealign.caching.replace_existing_cache import replace_existing_cache


class TestReplaceExistingCache(unittest.TestCase):
    def test_replace_existing_cache_with_none_list(self):
        new_cache = SingleFileCache(
            file_path="path1", last_modified=123, levels=mock.MagicMock()
        )

        result = replace_existing_cache(None, new_cache)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], new_cache)

    def test_replace_existing_cache_with_empty_list(self):
        original_cache_list = []
        new_cache = SingleFileCache(
            file_path="path1", last_modified=123, levels=mock.MagicMock()
        )

        result = replace_existing_cache(original_cache_list, new_cache)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], new_cache)

    def test_replace_existing_cache_with_new_entry(self):
        original_cache_list = [
            SingleFileCache(
                file_path="path1", last_modified=123, levels=mock.MagicMock()
            )
        ]
        new_cache = SingleFileCache(
            file_path="path2", last_modified=456, levels=mock.MagicMock()
        )

        result = replace_existing_cache(original_cache_list, new_cache)

        self.assertEqual(len(result), 2)
        self.assertIn(new_cache, result)

    def test_replace_existing_cache_with_replacement(self):
        original_cache_list = [
            SingleFileCache(
                file_path="path1", last_modified=123, levels=mock.MagicMock()
            )
        ]
        new_cache = SingleFileCache(
            file_path="path1", last_modified=456, levels=mock.MagicMock()
        )

        result = replace_existing_cache(original_cache_list, new_cache)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], new_cache)
        self.assertEqual(result[0].last_modified, 456)

    def test_replace_existing_cache_with_multiple_entries(self):
        original_cache_list = [
            SingleFileCache(
                file_path="path1", last_modified=123, levels=mock.MagicMock()
            ),
            SingleFileCache(
                file_path="path2", last_modified=789, levels=mock.MagicMock()
            ),
        ]
        new_cache = SingleFileCache(
            file_path="path1", last_modified=456, levels=mock.MagicMock()
        )

        result = replace_existing_cache(original_cache_list, new_cache)

        self.assertEqual(len(result), 2)
        self.assertIn(new_cache, result)
        self.assertNotIn(
            SingleFileCache(
                file_path="path1", last_modified=123, levels=mock.MagicMock()
            ),
            result,
        )
