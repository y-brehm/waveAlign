from music_tag import load_file

from wavealign.data_collection.audio_metadata import AudioMetadata


def write_metadata(file_path: str, audio_metadata: AudioMetadata) -> None:
    try:
        metadata = load_file(file_path)

        if not metadata:
            raise ValueError

        metadata["artwork"] = audio_metadata.artwork
        metadata.save()

    except ValueError:
        raise Exception(f"Failed to read metadata for {file_path}")
