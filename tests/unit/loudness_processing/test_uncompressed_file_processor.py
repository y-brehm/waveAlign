import mock
import unittest

from wavealign.loudness_processing.uncompressed_file_processor import (
    UncompressedFileProcessor,
)


class TestUncompressedFileProcessor(unittest.TestCase):
    @mock.patch(
        "wavealign.loudness_processing.uncompressed_file_processor.align_waveform_to_target"
    )
    @mock.patch(
        "wavealign.loudness_processing.uncompressed_file_processor.AudioFileWriter"
    )
    def test_process(self, mock_audio_file_writer, mock_align_waveform):
        audio_property_set = mock.MagicMock()
        target_level = -10
        output_file_path = "output.wav"
        audio_data = mock.MagicMock()

        UncompressedFileProcessor().process(
            audio_property_set, target_level, output_file_path, audio_data
        )
        mock_audio_file_writer.return_value.write.assert_called_once_with(
            output_file_path,
            mock_align_waveform.return_value,
            audio_property_set.metadata,
        )
        mock_align_waveform.assert_called_once_with(
            audio_data, audio_property_set.original_lufs_level, target_level
        )
