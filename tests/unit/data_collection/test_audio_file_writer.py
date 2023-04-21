import mock
import unittest

from src.wavealign.data_collection.audio_file_writer import AudioFileWriter
from src.wavealign.data_collection.audio_metadata import AudioMetadata
from src.wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


class TestAudioFileWriter(unittest.TestCase):
    def setUp(self):
        self.mock_audio_data = mock.MagicMock()
        self.mock_artwork = mock.MagicMock()
        self.mock_metadata = AudioMetadata(
            num_channels=2,
            artwork=self.mock_artwork,
            codec_name='eva01',
            bit_rate=16,
            sample_rate=44100)
        self.mock_spec_set = AudioFileSpecSet(
                file_path='some_path',
                audio_data=self.mock_audio_data,
                original_lufs=-16,
                metadata=self.mock_metadata
                )
        self.mock_tag_metadata = mock.MagicMock()

        self.mock_pcm_float_converter = mock.patch(
            'src.wavealign.data_collection.audio_file_writer.PcmFloatConverter').start()
        self.mock_write = mock.patch(
            'src.wavealign.data_collection.audio_file_writer.audio.write').start()
        self.mock_tag_load_file = mock.patch(
            'src.wavealign.data_collection.audio_file_writer.load_file').start()

        self.mock_tag_load_file.return_value = self.mock_tag_metadata

    def tearDown(self):
        mock.patch.stopall()

    def test_write(self):
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.return_value = False

        AudioFileWriter().write('some_path', self.mock_spec_set)

        self.mock_pcm_float_converter.return_value.pcm_to_float.assert_not_called()
        self.mock_write.assert_called_once_with('some_path',
                                                44100,
                                                self.mock_audio_data,
                                                c='eva01',
                                                overwrite=True,
                                                ac=2,
                                                ab=16,
                                                write_id3v2=True)
        self.mock_tag_metadata.save.assert_called_once()

    def test_write_with_conversion(self):
        mock_audio_data_converted = mock.MagicMock()
        self.mock_pcm_float_converter.return_value.float_to_pcm.return_value = mock_audio_data_converted
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.return_value = True

        AudioFileWriter().write('some_path', self.mock_spec_set)

        self.mock_write.assert_called_once_with('some_path',
                                                44100,
                                                mock_audio_data_converted,
                                                c='eva01',
                                                overwrite=True,
                                                ac=2,
                                                ab=16,
                                                write_id3v2=True)
        self.mock_tag_metadata.save.assert_called_once()


class TestAudioFileWriterAssert(unittest.TestCase):
    @mock.patch('src.wavealign.data_collection.audio_file_writer.load_file').start()
    def test_write_with_faulty_metadata(self, mock_tag_load_file):
        mock_tag_load_file.return_value = None

        try:
            AudioFileWriter().write('some_path', mock.MagicMock())
        except ValueError:
            pass
        except Exception:
            self.fail('unexpected exception raised')
        else:
            self.fail('ExpectedException not raised')
