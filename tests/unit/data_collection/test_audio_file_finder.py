import unittest
import mock
import os

from wavealign.data_collection.audio_file_finder import AudioFileFinder


class TestAudioFileFinder(unittest.TestCase):
    def setUp(self):
        self.audio_file_finder = AudioFileFinder()
        self.abs_path = os.path.join("root", "subdir")
        self.subdir_path = os.path.join(self.abs_path, "subdir")
        self.mock_abspath = mock.patch(
            "wavealign.data_collection.audio_file_finder.os.path.abspath"
        ).start()
        self.mock_walk = mock.patch(
            "wavealign.data_collection.audio_file_finder.os.walk"
        ).start()
        self.mock_abspath.return_value = self.abs_path

    def tearDown(self):
        self.mock_abspath.stop()
        self.mock_walk.stop()

    def test_find_no_files(self):
        self.mock_walk.return_value = [
            (self.abs_path, ("subdir",), ()),
        ]

        result = self.audio_file_finder.find("/some/path")
        self.assertEqual(result, [])

    def test_find_only_supported_audio_files(self):
        self.mock_walk.return_value = [
            (self.abs_path, ("subdir",), ("file1.wav", "file2.mp3")),
            (self.subdir_path, (), ("file3.aif", "file4.aiff", "file5.flac")),
        ]

        result = self.audio_file_finder.find("/some/path")
        expected = [
            os.path.join(self.abs_path, "file1.wav"),
            os.path.join(self.abs_path, "file2.mp3"),
            os.path.join(self.subdir_path, "file3.aif"),
            os.path.join(self.subdir_path, "file4.aiff"),
            os.path.join(self.subdir_path, "file5.flac"),
        ]
        self.assertEqual(result, expected)

    def test_find_no_supported_audio_files(self):
        self.mock_walk.return_value = [
            (self.abs_path, ("subdir",), ("file1.txt", "file2.doc")),
            (self.subdir_path, (), ("file3.pdf", "file4.docx")),
        ]

        result = self.audio_file_finder.find("/some/path")
        self.assertEqual(result, [])

    def test_find_mixed_files(self):
        self.mock_walk.return_value = [
            (
                self.abs_path,
                ("subdir",),
                ("file1.wav", "file2.mp3", "file3.txt", "file4.aiff"),
            ),
            (self.subdir_path, (), ("file5.aif", "file6.flac", "file7.doc")),
        ]

        result = self.audio_file_finder.find("/some/path")
        expected = [
            os.path.join(self.abs_path, "file1.wav"),
            os.path.join(self.abs_path, "file2.mp3"),
            os.path.join(self.abs_path, "file4.aiff"),
            os.path.join(self.subdir_path, "file5.aif"),
            os.path.join(self.subdir_path, "file6.flac"),
        ]
        self.assertEqual(result, expected)
