from music_tag import load_file

from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


def write_metadata(audio_file_spec_set: AudioFileSpecSet,
                   file_path: str
                   ) -> None:
    try:
        metadata = load_file(file_path)

        if not metadata:
            raise ValueError

        metadata['artwork'] = audio_file_spec_set.metadata.artwork
        metadata.save()

    except ValueError:
        raise ValueError(f"Failed to read metadata for {file_path}")
