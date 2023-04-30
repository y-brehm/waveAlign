from ffmpegio import audio

from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.data_collection.pcm_float_converter import PcmFloatConverter
from wavealign.data_collection.write_metadata import write_metadata


class AudioFileWriter:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()

    def write(self,
              file_path: str,
              audio_file_spec_set: AudioFileSpecSet
              ) -> None:
        self.__write_audio(audio_file_spec_set, file_path)
        write_metadata(audio_file_spec_set, file_path)

    def __write_audio(self,
                      audio_file_spec_set: AudioFileSpecSet,
                      file_path: str
                      ) -> None:
        audio_data = audio_file_spec_set.audio_data

        if self.__pcm_float_converter.is_pcm_encoded(audio_data):
            audio_data = self.__pcm_float_converter.float_to_pcm(audio_data)

        audio.write(
            file_path,
            audio_file_spec_set.metadata.sample_rate,
            audio_data,
            c=audio_file_spec_set.metadata.codec_name,
            overwrite=True,
            ac=audio_file_spec_set.metadata.num_channels,
            ab=audio_file_spec_set.metadata.bit_rate,
            write_id3v2=True,
            )
