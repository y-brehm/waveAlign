from music_tag import load_file
from ffmpegio import probe

from wavealign.data_collection.audio_metadata import AudioMetadata


class MetaDataExtractor:
    def extract(self, file_path: str) -> AudioMetadata:
        tag_metadata = load_file(file_path)
        full_details = probe.full_details(file_path)
        audio_stream_metadata = full_details['streams'][0]

        return AudioMetadata(
            num_channels=audio_stream_metadata['channels'],
            artwork=tag_metadata['artwork'],
            codec_name=audio_stream_metadata['codec_name'],
            bit_rate=self.__get_bitrate_specifier(full_details),
            sample_rate=audio_stream_metadata['sample_rate']
            )

    def __get_bitrate_specifier(self, full_details: dict) -> str:
        for details in full_details.values():
            if isinstance(details, dict) and 'bit_rate' in details:
                return f"{details['bit_rate'] / 1000}k"
