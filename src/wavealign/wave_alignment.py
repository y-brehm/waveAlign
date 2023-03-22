import os

from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.data_collection.audio_file_handler import AudioFileHandler
from wavealign.loudness_processing.align_waveform_to_target import align_waveform_to_target
from wavealign.loudness_processing.calculation import detect_peak


def wave_alignment(
        input_path: str,
        output_path: str,
        target_lufs: int,
        read_only: bool,
        check_for_clipping: bool,
        ) -> None:
    try:
        lufs_values = []
        for file_path in AudioFileFinder().find(os.path.normpath(input_path)):
            audio_file_spec_set = AudioFileHandler().read(file_path)
            lufs_values.append(audio_file_spec_set.original_lufs)
            print(f"Processing file: {file_path}, original LUFS: {audio_file_spec_set.original_lufs}")
            if read_only is False:
                align_waveform_to_target(audio_file_spec_set, target_lufs)
                if check_for_clipping:
                    peak_after_processing = detect_peak(audio_file_spec_set.audio_data)
                    print(f"new PEAK value after processing: {peak_after_processing}")

                    assert (peak_after_processing <= 0)

                if output_path is None:
                    output = audio_file_spec_set.file_path
                else:
                    output = os.path.join(output_path, os.path.split(audio_file_spec_set.file_path)[1])
                AudioFileHandler().write(output, audio_file_spec_set)
        print(f"Total number of processed files: {len(lufs_values)}")
        print(f"Minimum overall LUFS-value: {min(lufs_values)} dB LUFS")
        print(f"Maximum overall LUFS-value: {max(lufs_values)} dB LUFS")
    except AssertionError:
        raise Exception("Clipping occurred, please check your Levels!")
