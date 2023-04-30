import os

from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.loudness_processing.waveform_aligner import WaveformAligner
from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.peak_calculator import PeakCalculator


class WaveAlignmentProcessor:
    def __init__(self) -> None:
        self.__audio_file_finder = AudioFileFinder()
        self.__audio_file_reader = AudioFileReader()
        self.__audio_file_writer = AudioFileWriter()
        self.__wavform_aligner = WaveformAligner()
        self.__peak_calculator = PeakCalculator()

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
        try:
            audio_levels = []
            for file_path in self.__audio_file_finder.find(os.path.normpath(input_path)):
                audio_file_spec_set = self.__audio_file_reader.read(file_path, window_size, gain_calculation_strategy)
                audio_levels.append(audio_file_spec_set.original_audio_level)
                print(f"Processing file: {file_path}, original {gain_calculation_strategy.value}: "
                      f"{audio_file_spec_set.original_audio_level}")
                if read_only is False:
                    self.__wavform_aligner.align_waveform_to_target(audio_file_spec_set, target_level)
                    if check_for_clipping:
                        peak_after_processing = self.__peak_calculator.calculate_level(audio_file_spec_set.audio_data)
                        print(f"new PEAK value after processing: {peak_after_processing} dBFS")

                        assert (peak_after_processing <= 0)

                    if output_path is None:
                        output = audio_file_spec_set.file_path
                    else:
                        output = os.path.join(
                                output_path,
                                os.path.split(audio_file_spec_set.file_path)[1]
                                )
                    self.__audio_file_writer.write(output, audio_file_spec_set)
            print(f"Total number of processed files: {len(audio_levels)}")
            print(f"Minimum overall {gain_calculation_strategy.value}-value: "
                  f"{min(audio_levels)} dB {gain_calculation_strategy.value}")
            print(f"Maximum overall {gain_calculation_strategy.value}-value: "
                  f"{max(audio_levels)} dB {gain_calculation_strategy.value}")
        except AssertionError:
            raise Exception("Clipping occurred, please check your Levels!")
