from music_tag import load_file
import soundfile

from wavealign.loudness_processing.calculation import calculate_lufs
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


def read(file_path: str) -> AudioFileSpecSet:
    metadata = load_file(file_path)
    artwork = metadata['artwork']

    audio_data, sample_rate = soundfile.read(file_path)

    original_lufs = calculate_lufs(audio_data, sample_rate)

    return AudioFileSpecSet(
        file_path=file_path,
        audio_data=audio_data,
        sample_rate=int(sample_rate),
        artwork=artwork,
        original_lufs=original_lufs,
        )


def write(file_path: str, audio_file_spec_set: AudioFileSpecSet) -> None:
    soundfile.write(file_path,
                    audio_file_spec_set.audio_data,
                    audio_file_spec_set.sample_rate,
                    subtype='PCM_16'
                    )

    metadata = load_file(file_path)
    metadata['artwork'] = audio_file_spec_set.artwork
    metadata.save()
