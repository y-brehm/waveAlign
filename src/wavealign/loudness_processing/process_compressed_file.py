import os
import shutil
import subprocess

from wavealign.data_collection.audio_property_set import AudioPropertySet


def process_compressed_file(
    audio_property_set: AudioPropertySet, target_level: int, output_file_path: str
) -> None:
    gain_adjustment = str(
        0.75 * (target_level - audio_property_set.original_lufs_level)
    )
    print("AACGAIN: Gain adjustment: " + gain_adjustment)

    if output_file_path != audio_property_set.file_path:
        shutil.copy(audio_property_set.file_path, output_file_path)

    parent_dir = os.path.realpath(__file__)
    for _ in range(4):
        parent_dir = os.path.dirname(parent_dir)

    aacgain_path = os.path.join(parent_dir, "third_party", "aacgain", "Mac", "aacgain")

    result = subprocess.run(
        [
            aacgain_path,
            "-g",
            gain_adjustment,
            "-q",
            output_file_path,
        ]
    )

    if result.returncode != 0:
        raise Exception(
            "AACGAIN: Failed to process compressed file:" + audio_property_set.file_path
        )
