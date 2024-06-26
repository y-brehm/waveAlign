from ffmpegio import probe
from mutagen import File

from wavealign.data_collection.audio_metadata import AudioMetadata


class MetaDataExtractor:
    def extract(
        self,
        file_path: str,
    ) -> AudioMetadata:
        metadata = File(file_path)
        full_details = probe.full_details(file_path)
        audio_stream_metadata = full_details["streams"][0]
        bit_rate = self.__get_bitrate_specifier(audio_stream_metadata["bit_rate"])

        return AudioMetadata(
            num_channels=audio_stream_metadata["channels"],
            metadata=metadata,
            codec_name=audio_stream_metadata["codec_name"],
            bit_rate=bit_rate,
            sample_rate=audio_stream_metadata["sample_rate"],
        )

    @staticmethod
    def __get_bitrate_specifier(bit_rate: int) -> str:
        return f"{int(bit_rate / 1000)}k"
