from unittest.mock import patch
import unittest
import os

from wavealign.loudness_processing.retrieve_mp3processor_executable_path import (
    retrieve_mp3processor_executable_path,
)


class TestRetrieveMp3ProcessorExecutablePath(unittest.TestCase):
    def setUp(self):
        self.mock_system = patch(
            "wavealign.loudness_processing.retrieve_mp3processor_executable_path.platform.system"
        ).start()
        self.mock_realpath = patch(
            "wavealign.loudness_processing.retrieve_mp3processor_executable_path.os.path.realpath"
        ).start()
        self.mock_dirname = patch(
            "wavealign.loudness_processing.retrieve_mp3processor_executable_path.os.path.dirname"
        ).start()
        self.mock_realpath.return_value = (
            os.path.join("fake"),
            "path",
            "to",
            "current",
            "file.py",
        )
        self.mock_dirname.side_effect = [
            os.path.join("fake", "path", "to", "current"),
            os.path.join("fake", "path", "to"),
        ]

    def tearDown(self):
        patch.stopall()

    def test_retrieve_mp3processor_executable_path_mac(self):
        self.mock_system.return_value = "Darwin"

        expected_path = os.path.join(
            "fake", "path", "to", "mp3processor", "bin", "Mac", "mp3processor"
        )
        actual_path = retrieve_mp3processor_executable_path()

        self.assertEqual(actual_path, expected_path)

    def test_retrieve_mp3processor_executable_path_windows(self):
        self.mock_system.return_value = "Windows"

        expected_path = os.path.join(
            "fake",
            "path",
            "to",
            "mp3processor",
            "bin",
            "Win",
            "Release",
            "mp3processor.exe",
        )
        actual_path = retrieve_mp3processor_executable_path()

        self.assertEqual(actual_path, expected_path)

    def test_retrieve_mp3processor_executable_path_unsupported(self):
        self.mock_system.return_value = "Linux"

        with self.assertRaises(SystemError) as context:
            retrieve_mp3processor_executable_path()
            self.assertEqual(str(context.exception), "Unsupported platform: Linux")
