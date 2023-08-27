import os

from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)
from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.clipping_processor import ClippingProcessor


class WaveAlignmentProcessor:
    def __init__(self) -> None:
        self.__audio_file_finder = AudioFileFinder()
        self.__audio_file_reader = AudioFileReader()
        self.__audio_file_writer = AudioFileWriter()
        self.__clipping_processor = ClippingProcessor()

    def process(
        self,
        input_path: str,
        output_path: str,
        window_size: int,
        gain_calculation_strategy: GainCalculationStrategy,
        target_level: int,
        read_only: bool,
        check_for_clipping: bool,
    ) -> None:
        audio_levels = []
        unprocessed_files = []
        for file_path in self.__audio_file_finder.find(
            os.path.normpath(input_path)
        ):
            try:
                audio_file_spec_set = self.__audio_file_reader.read(
                    file_path, window_size, gain_calculation_strategy
                )
                audio_levels.append(audio_file_spec_set.original_audio_level)
                print(
                    f"Processing file: {file_path}, original {gain_calculation_strategy.value}: "
                    f"{audio_file_spec_set.original_audio_level}"
                )

                if read_only:
                    continue

                audio_file_spec_set.audio_data = align_waveform_to_target(
                    audio_file_spec_set.audio_data,
                    audio_file_spec_set.original_audio_level,
                    target_level,
                )
                if check_for_clipping:
                    self.__clipping_processor.check_for_clipping(
                        audio_file_spec_set.audio_data
                    )

                if not output_path:
                    output = audio_file_spec_set.file_path
                else:
                    output = os.path.join(
                        output_path, os.path.split(audio_file_spec_set.file_path)[1]
                    )
                self.__audio_file_writer.write(output, audio_file_spec_set)

            except Exception as e:
                unprocessed_files.append((file_path, str(e)))
                print(f"Error processing file {file_path}: {e}")
                continue

        self.__print_processing_information(
            audio_levels, gain_calculation_strategy.value
        )
        if unprocessed_files:
            print("The following files could not be processed:")
            for file, error in unprocessed_files:
                print(f"{file}: {error}")

    @staticmethod
    def __print_processing_information(audio_levels: list[float], gain_calculation_strategy: str):
        print(f"Total number of processed files: {len(audio_levels)}")
        print(
            f"Minimum overall {gain_calculation_strategy}-value: "
            f"{min(audio_levels)} dB {gain_calculation_strategy}"
        )
        print(
            f"Maximum overall {gain_calculation_strategy}-value: "
            f"{max(audio_levels)} dB {gain_calculation_strategy}"
        )
