import os

from soundfile import write

from wavealign.data_collection.find_audio_files import find_audio_files
from wavealign.data_collection.generate_audio_spec_set import generate_audio_spec_set
from wavealign.loudness_processing.align_waveform_to_target import align_waveform_to_target
from wavealign.loudness_processing.calculation import detect_peak


def wave_alignment(input_path, output_path, target_lufs, check_for_clipping):
    try:
        for file_path in find_audio_files(os.path.normpath(input_path), file_ending='.wav'):
            audio_spec_set = generate_audio_spec_set(file_path)
            print(f"Processing file: {file_path}, original LUFS: {audio_spec_set.original_lufs}")
            align_waveform_to_target(audio_spec_set, target_lufs)
            if check_for_clipping:
                peak_after_processing = detect_peak(audio_spec_set.audio_data)
                print(f"new PEAK value after processing: {peak_after_processing}")

                assert (peak_after_processing <= 0)

            if output_path is None:
                output = input_path
            else:
                output = os.path.join(output_path, os.path.split(audio_spec_set.file_path)[1])
            write(output, audio_spec_set.audio_data, audio_spec_set.sample_rate, subtype='PCM_16')
    except AssertionError:
        raise Exception("Clipping occurred, please check your Levels!")
