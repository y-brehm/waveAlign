import os
import logging

from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.data_collection.audio_property_sets_analyzer import (
    AudioPropertySetsAnalyzer,
)
from wavealign.loudness_processing.audio_property_sets_processor import (
    AudioPropertySetsProcessor,
)
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy


class WaveAlignmentProcessor:
    def __init__(
        self,
        clipping_strategy: ClippingStrategy = ClippingStrategy.SKIP,
    ) -> None:
        self.__audio_property_sets_reader = AudioPropertySetsReader()
        self.__audio_property_sets_analyzer = AudioPropertySetsAnalyzer()
        self.__audio_property_sets_processor = AudioPropertySetsProcessor(
            clipping_strategy=clipping_strategy
        )

    def process(
        self,
        input_path: str,
        output_path: str,
        window_size: WindowSize = WindowSize.LUFS_S,
        user_target_level: int = -14,
        read_only: bool = False,
    ) -> list[str]:
        audio_property_sets, skipped_files = self.__audio_property_sets_reader.read(
            input_path, window_size
        )
        if user_target_level:
            target_level = user_target_level
        else:
            library_dependent_max_lufs = (
                self.__audio_property_sets_analyzer.detect_target_value(
                    audio_property_sets
                )
            )
            target_level = library_dependent_max_lufs
        if read_only:
            for audio_property_set in audio_property_sets:
                print(
                    f"{audio_property_set.file_path} - "
                    f"{audio_property_set.original_lufs_level} LUFS"
                )
            clipped_files = []
            print(
                f"Library dependent target level: "
                f"{self.__audio_property_sets_analyzer.detect_target_value(audio_property_sets)}"
                f" LUFS"
            )
        else:
            clipped_files = self.__audio_property_sets_processor.process(
                audio_property_sets, target_level, output_path
            )

        problem_files = skipped_files + clipped_files
        # TODO: add caching and logging timestamps
        # TODO: add progress bar
        if problem_files:
            log_file_path = os.path.join(
                output_path if output_path else input_path, "wavealign.log"
            )
            logging.basicConfig(filename=log_file_path, level=logging.INFO)
            print(
                f"Some files were not processed successfully. "
                f"Check the log file located at {log_file_path} for details."
            )
            logging.info("The following files were not processed:")
            for problem_file in problem_files:
                logging.info(problem_file)
        else:
            print("All files processed successfully.")

        return problem_files
