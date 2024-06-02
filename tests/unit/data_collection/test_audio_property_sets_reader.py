import unittest
import mock

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.loudness_processing.window_size import WindowSize


class TestAudioPropertySetsReader(unittest.TestCase):
    def setUp(self):
        self.mock_audio_property_set_generator = mock.patch(
            "wavealign.data_collection.audio_property_sets_reader.AudioPropertySetGenerator"
        ).start()
        self.mock_audio_file_finder = mock.patch(
            "wavealign.data_collection.audio_property_sets_reader.AudioFileFinder"
        ).start()
        self.mock_getlogger = mock.patch(
            "wavealign.data_collection.audio_property_sets_reader.logging.getLogger"
        ).start()
        self.mock_logger = mock.MagicMock()
        self.mock_getlogger.return_value = self.mock_logger

    def tearDown(self):
        mock.patch.stopall()

    def test_read(self):
        self.mock_audio_file_finder.return_value.find.return_value = [
            "dummy_path_1",
            "dummy_path_2",
        ]
        self.mock_audio_property_set_generator.return_value.generate.side_effect = [
            AudioPropertySet("dummy_path_1", 1234, -14, -1, metadata=mock.MagicMock()),
            Exception("Error"),
        ]

        reader = AudioPropertySetsReader("input_path", WindowSize.LUFS_S)
        audio_property_sets = reader.read()

        self.mock_audio_file_finder.return_value.find.assert_called_once_with(
            "input_path"
        )
        self.mock_getlogger.assert_called_once_with("AUDIO READER")
        self.assertEqual(
            self.mock_audio_property_set_generator.return_value.generate.call_count, 2
        )
        self.assertEqual(len(audio_property_sets), 1)
        self.assertEqual(audio_property_sets[0].file_path, "dummy_path_1")

    def test_read_no_errors(self):
        self.mock_audio_file_finder.return_value.find.return_value = [
            "dummy_path_1",
            "dummy_path_2",
        ]
        self.mock_audio_property_set_generator.return_value.generate.side_effect = [
            AudioPropertySet("dummy_path_1", 123, -14, -1, metadata=mock.MagicMock()),
            AudioPropertySet("dummy_path_2", 456, -14, -1, metadata=mock.MagicMock()),
        ]

        reader = AudioPropertySetsReader("input_path", WindowSize.LUFS_S)
        audio_property_sets = reader.read()

        self.mock_audio_file_finder.return_value.find.assert_called_once_with(
            "input_path"
        )
        self.mock_getlogger.assert_called_once_with("AUDIO READER")
        self.assertEqual(
            self.mock_audio_property_set_generator.return_value.generate.call_count, 2
        )
        self.assertEqual(len(audio_property_sets), 2)
        self.assertEqual(audio_property_sets[0].file_path, "dummy_path_1")
        self.assertEqual(audio_property_sets[1].file_path, "dummy_path_2")

    def test_read_with_caching(self):
        self.mock_audio_file_finder.return_value.find.return_value = [
            "dummy_path_1",
            "dummy_path_2",
        ]
        self.mock_audio_property_set_generator.return_value.generate.side_effect = [
            AudioPropertySet("dummy_path_2", 456, -14, -1, metadata=mock.MagicMock()),
        ]

        mock_cache_manager = mock.MagicMock()
        mock_cache_manager.is_cached.side_effect = [
            True,
            False,
        ]

        reader = AudioPropertySetsReader(
            "input_path", WindowSize.LUFS_S, cache_manager=mock_cache_manager
        )
        audio_property_sets = reader.read()

        self.mock_audio_file_finder.return_value.find.assert_called_once_with(
            "input_path"
        )
        self.mock_getlogger.assert_called_once_with("AUDIO READER")
        self.assertEqual(
            self.mock_audio_property_set_generator.return_value.generate.call_count, 1
        )
        self.assertEqual(len(audio_property_sets), 1)
        self.assertEqual(audio_property_sets[0].file_path, "dummy_path_2")
        mock_cache_manager.is_cached.assert_has_calls(
            [mock.call("dummy_path_1"), mock.call("dummy_path_2")]
        )
        self.mock_logger.info.assert_called_once()
