import mock
import unittest

from wavealign.data_collection.audio_file_finder import AudioFileFinder


class TestAudioFileFinder(unittest.TestCase):
    def setUp(self):
        self.audio_file_finder = AudioFileFinder()
        self.fake_start_dir = "/my/fake/dir"
        self.fake_file_dir = [
            ("/my/fake/dir", ["subdir"], ["fake_file_1.wav", "fake_file_2.txt"]),
            ("/my/fake/dir/subdir", [], ["fake_file_3.aiff"]),
        ]
        self.expected_output = [
            "/my/fake/dir/fake_file_1.wav",
            "/my/fake/dir/subdir/fake_file_3.aiff",
        ]

        self.mock_walk = mock.patch(
            "wavealign.data_collection.audio_file_finder.os.walk"
        ).start()
        self.mock_walk.return_value = self.fake_file_dir

    @mock.patch("wavealign.data_collection.audio_file_finder.os.path.abspath")
    @mock.patch(
        "wavealign.data_collection.audio_file_finder.AudioFileFinder."
        "_AudioFileFinder__is_supported_audio_file"
    )
    def test_find_calls(
        self, mock_AudioFileFinder__is_supported_audio_file, mock_abspath
    ):
        mock_abspath.return_value = self.fake_start_dir
        mock_AudioFileFinder__is_supported_audio_file.side_effect = [True, False, True]

        fake_output = self.audio_file_finder.find(self.fake_start_dir)

        mock_abspath.assert_called_once_with(self.fake_start_dir)
        self.mock_walk.assert_called_once_with(self.fake_start_dir)
        mock_AudioFileFinder__is_supported_audio_file.assert_has_calls(
            [
                mock.call("fake_file_1.wav"),
                mock.call("fake_file_2.txt"),
                mock.call("fake_file_3.aiff"),
            ]
        )

        self.assertEqual(fake_output, self.expected_output)

    def test_find_functionality(self):
        fake_output = self.audio_file_finder.find(self.fake_start_dir)

        self.mock_walk.assert_called_once_with(self.fake_start_dir)
        self.assertEqual(fake_output, self.expected_output)
