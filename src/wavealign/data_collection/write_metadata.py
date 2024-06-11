from mutagen import File

from wavealign.data_collection.audio_metadata import AudioMetadata


def write_metadata(file_path: str, audio_metadata: AudioMetadata) -> None:
    try:
        metadata = File(file_path)
        if metadata is None:
            raise ValueError
         
        for tag in audio_metadata.metadata.keys():
            if audio_metadata.metadata[tag]:
                metadata[tag] = audio_metadata.metadata[tag]

        metadata.save()

    except ValueError:
        raise Exception(f"Failed to write metadata for {file_path}")
