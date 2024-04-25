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

    def tearDown(self):
        mock.patch.stopall()

    def test_read(self):
        self.mock_audio_file_finder.return_value.find.return_value = [
            "dummy_path_1",
            "dummy_path_2",
        ]
        self.mock_audio_property_set_generator.return_value.read.side_effect = [
            AudioPropertySet("dummy_path_1", -14, -1, metadata=mock.MagicMock()),
            Exception("Error"),
        ]

        reader = AudioPropertySetsReader()
        audio_property_sets, unprocessed_files = reader.read(
            "input_path", WindowSize.LUFS_S
        )

        self.mock_audio_file_finder.return_value.find.assert_called_once_with(
            "input_path"
        )
        self.assertEqual(
            self.mock_audio_property_set_generator.return_value.read.call_count, 2
        )
        self.assertEqual(len(audio_property_sets), 1)
        self.assertEqual(audio_property_sets[0].file_path, "dummy_path_1")
        self.assertEqual(len(unprocessed_files), 1)
        self.assertEqual(unprocessed_files[0], "dummy_path_2: Error")

    def test_read_no_errors(self):
        self.mock_audio_file_finder.return_value.find.return_value = [
            "dummy_path_1",
            "dummy_path_2",
        ]
        self.mock_audio_property_set_generator.return_value.read.side_effect = [
            AudioPropertySet("dummy_path_1", -14, -1, metadata=mock.MagicMock()),
            AudioPropertySet("dummy_path_2", -14, -1, metadata=mock.MagicMock()),
        ]

        reader = AudioPropertySetsReader()
        audio_property_sets, unprocessed_files = reader.read(
            "input_path", WindowSize.LUFS_S
        )

        self.mock_audio_file_finder.return_value.find.assert_called_once_with(
            "input_path"
        )
        self.assertEqual(
            self.mock_audio_property_set_generator.return_value.read.call_count, 2
        )
        self.assertEqual(len(audio_property_sets), 2)
        self.assertEqual(audio_property_sets[0].file_path, "dummy_path_1")
        self.assertEqual(audio_property_sets[1].file_path, "dummy_path_2")
        self.assertEqual(len(unprocessed_files), 0)
