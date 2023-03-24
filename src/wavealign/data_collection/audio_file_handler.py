from ffmpegio import audio
from music_tag import load_file

from wavealign.loudness_processing.calculation import calculate_lufs
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.data_collection.pcm_float_converter import PcmFloatConverter
from wavealign.data_collection.metadata_extractor import MetaDataExtractor


class AudioFileHandler:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()
        self.__metadata_extractor = MetaDataExtractor()

    def read(self, file_path: str) -> AudioFileSpecSet:
        _, audio_data = audio.read(file_path)

        if self.__pcm_float_converter.is_pcm_encoded(audio_data):
            audio_data = self.__pcm_float_converter.pcm_to_float(audio_data)

        metadata = self.__metadata_extractor.extract(file_path)
        original_lufs = calculate_lufs(audio_data, metadata.sample_rate)

        return AudioFileSpecSet(
            file_path=file_path,
            audio_data=audio_data,
            original_lufs=original_lufs,
            metadata=metadata
            )

    def write(self,
              file_path: str,
              audio_file_spec_set: AudioFileSpecSet
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

        metadata = load_file(file_path)
        metadata['artwork'] = audio_file_spec_set.metadata.artwork
        metadata.save()
