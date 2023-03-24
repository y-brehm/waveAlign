import ffmpegio

from music_tag import load_file
from wavealign.loudness_processing.calculation import calculate_lufs
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.data_collection.pcm_float_converter import PcmFloatConverter


class AudioFileHandler:
    def __init__(self) -> None:
        self.__pcm_float_converter = PcmFloatConverter()

    def read(self, file_path: str) -> AudioFileSpecSet:
        metadata = load_file(file_path)
        artwork = metadata['artwork']

        sample_rate, audio = ffmpegio.audio.read(file_path)
        if self.__pcm_float_converter.is_pcm_encoded(audio):
            audio = self.__pcm_float_converter.pcm_to_float(audio)

        original_lufs = calculate_lufs(audio, sample_rate)

        audio_metadata = ffmpegio.probe.full_details(file_path)
        audio_stream_metadata = audio_metadata['streams'][0]
        codec_name = audio_stream_metadata['codec_name']
        bit_rate = self.__get_bitrate_specifier(audio_metadata)

        return AudioFileSpecSet(
            file_path=file_path,
            audio_data=audio,
            sample_rate=int(sample_rate),
            artwork=artwork,
            original_lufs=original_lufs,
            codec_name=codec_name,
            bit_rate=bit_rate
            )

    def write(self,
              file_path: str,
              audio_file_spec_set: AudioFileSpecSet
              ) -> None:

        audio = audio_file_spec_set.audio_data

        if self.__pcm_float_converter.is_pcm_encoded(audio):
            audio = self.__pcm_float_converter.float_to_pcm(audio)

        ffmpegio.audio.write(
            file_path,
            audio_file_spec_set.sample_rate,
            audio,
            c=audio_file_spec_set.codec_name,
            overwrite=True,
            ac=2,
            ab=audio_file_spec_set.bit_rate,
            write_id3v2=True,
            )

        metadata = load_file(file_path)
        metadata['artwork'] = audio_file_spec_set.artwork
        metadata.save()

    def __get_bitrate_specifier(self, audio_metadata: dict) -> str:
        for metadata in audio_metadata.values():
            if isinstance(metadata, dict) and 'bit_rate' in metadata:
                return f"{metadata['bit_rate'] / 1000}k"
