from mutagen import File, FileType

from wavealign.data_collection.audio_metadata import AudioMetadata


def write_metadata(file_path: str, audio_metadata: AudioMetadata) -> None:
    try:
        metadata = File(file_path)
        
        if not isinstance(metadata, FileType):
            raise ValueError
         
        for tag_name in audio_metadata.metadata.keys():
            if audio_metadata.metadata[tag_name]:
                metadata[tag_name] = audio_metadata.metadata[tag_name]

        metadata.save()

    except ValueError:
        raise Exception(f"Failed to write metadata for {file_path}")
