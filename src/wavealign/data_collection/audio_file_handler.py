from music_tag import load_file
import ffmpegio

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
        if audio.dtype.kind == 'i':
            audio = self.__pcm_float_converter.pcm_to_float(audio)

        original_lufs = calculate_lufs(audio, sample_rate)

        return AudioFileSpecSet(
            file_path=file_path,
            audio_data=audio,
            sample_rate=int(sample_rate),
            artwork=artwork,
            original_lufs=original_lufs,
            )

    def write(self,
              file_path: str,
              audio_file_spec_set: AudioFileSpecSet
              ) -> None:

        audio = audio_file_spec_set.audio_data

        if audio.dtype.kind == 'i':
            audio = self.__pcm_float_converter.float_to_pcm(audio)

        ffmpegio.audio.write(
            file_path,
            audio_file_spec_set.sample_rate,
            audio
            )

        metadata = load_file(file_path)
        # TODO: add artwork edge case handling for m4a
        if not file_path.endswith('m4a'):
            metadata['artwork'] = audio_file_spec_set.artwork
        metadata.save()
