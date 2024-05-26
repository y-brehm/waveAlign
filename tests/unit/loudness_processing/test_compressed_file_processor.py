import mock
import unittest

from wavealign.loudness_processing.compressed_file_processor import (
    CompressedFileProcessor,
)


class TestCompressedFileProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_get_mp3processor_executable_path = mock.patch(
            "wavealign.loudness_processing.compressed_file_processor.get_mp3processor_executable_path"
        ).start()
        self.mock_subprocess_run = mock.patch(
            "wavealign.loudness_processing.compressed_file_processor.subprocess.run"
        ).start()
        self.mock_copy = mock.patch(
            "wavealign.loudness_processing.compressed_file_processor.shutil.copy"
        ).start()
        self.audio_property_set = mock.MagicMock()
        self.target_level = -10
        self.audio_property_set.original_lufs_level = -10
        self.output_file_path = "output.mp3"
        self.mock_subprocess_run.return_value.returncode = 0

    def tearDown(self):
        mock.patch.stopall()

    def test_process(self):
        CompressedFileProcessor().process(
            self.audio_property_set, self.target_level, self.output_file_path
        )

        self.mock_copy.assert_called_once_with(
            self.audio_property_set.file_path, self.output_file_path
        )
        self.mock_subprocess_run.assert_called_once_with(
            [
                self.mock_get_mp3processor_executable_path.return_value,
                "i",
                self.output_file_path,
                "-g",
                "0.0",
            ]
        )
        self.mock_get_mp3processor_executable_path.assert_called_once()

    def test_process_no_copy(self):
        self.audio_property_set.file_path = self.output_file_path

        CompressedFileProcessor().process(
            self.audio_property_set, self.target_level, self.output_file_path
        )

        self.mock_copy.assert_not_called()

    def test_process_throws(self):
        self.mock_subprocess_run.return_value.returncode = 1

        with self.assertRaises(Exception):
            CompressedFileProcessor().process(
                self.audio_property_set, self.target_level, self.output_file_path
            )
