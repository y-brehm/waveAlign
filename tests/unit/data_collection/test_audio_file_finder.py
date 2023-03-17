import mock
import unittest

from wavealign.data_collection.audio_file_finder import AudioFileFinder

class TestAudioFileFinder(unittest.TestCase):

    def setUp(self):
        self.audio_file_finder = AudioFileFinder()
        self.fake_start_dir = "/my/fake/dir"

    @mock.patch('os.path.abspath')
    @mock.patch('os.walk')
    def test_find(self, mock_walk, mock_abspath):
        mock_abspath.return_value = self.fake_start_dir
        mock_walk.return_value = [
                ("/my/fake/dir", ["subdir"], ["fake_file_1.wav", "fake_file_2.aiff", "fake_file_3.mp3"]),
                ("/my/fake/dir/subdir", ["subdir2"], ["fake_file_4.mp3", "fake_file_5.wav"]),
                ("/my/fake/dir/subdir/subdir2", [], [])
        ]
    
        expected_result = [
                "/my/fake/dir/fake_file_1.wav",
                "/my/fake/dir/fake_file_2.aiff",
                "/my/fake/dir/subdir/fake_file_5.wav"
        ]

        self.assertEqual(self.audio_file_finder.find(self.fake_start_dir), expected_result)
        mock_abspath.assert_called_once_with(self.fake_start_dir)
        mock_walk.assert_called_once_with(self.fake_start_dir)


    def test_is_supported_audio_file(self):
        self.assertTrue(self.audio_file_finder._AudioFileFinder__is_supported_audio_file("fake_file_1.wav"))
        self.assertTrue(self.audio_file_finder._AudioFileFinder__is_supported_audio_file("fake_file_2.aiff"))

        self.assertFalse(self.audio_file_finder._AudioFileFinder__is_supported_audio_file("fake_file_3.mp3"))
        self.assertFalse(self.audio_file_finder._AudioFileFinder__is_supported_audio_file("fake_file_4.txt"))

