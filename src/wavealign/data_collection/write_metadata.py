from music_tag import load_file

from wavealign.data_collection.audio_metadata import AudioMetadata

#TODO: Metadata transfer alternative #32

def write_metadata(file_path: str, audio_metadata: AudioMetadata) -> None:
    try:
        metadata = load_file(file_path)
        
        if not metadata:
            raise ValueError
         
        for tag_name in audio_metadata.metadata._TAG_MAP.keys():
            metadata[tag_name] = audio_metadata.metadata[tag_name]

        metadata.save()

    except ValueError:
        raise Exception(f"Failed to read metadata for {file_path}")
