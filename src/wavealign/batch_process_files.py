import argparse

from wavealign.data_collection.logging_configuration import (
    setup_logging,
    output_logfile_warning,
)
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.data_collection.wave_alignment_reader import WaveAlignmentReader
from wavealign.wave_alignment_processor import WaveAlignmentProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Song loudness alignment processor for ending the loudness war."
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Specify an input directory to look for audio. Nested structures are allowed.",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Specify the output directory to save the processed data. "
        "If set to None the original data is overwritten."
        "Nested folder structures will be  dissolved.",
        type=str,
    )
    parser.add_argument(
        "-w",
        "--window_size",
        help="Specify the window size, LUFS-S (3s), LUFS-M (4s), LUFS-I (intergrated)."
        " Default is LUFS-S.",
        metavar="LUFS-S|LUFS-M|LUFS-I",
        type=lambda value: WindowSize(value),
        default=WindowSize.LUFS_S,
        choices=list(WindowSize),
    )
    parser.add_argument(
        "-t",
        "--target",
        help="Specify the target loudness level in dB. Has to be between -30 and -8.",
        metavar="-30 <= target <= -10",
        choices=range(-30, -7),
        type=int,
        default=-12,
    )
    parser.add_argument(
        "-r",
        "--read_only",
        help="Run in read only mode. "
        " Only outputs LUFS of input files without processing them."
        " Also outputs library dependent max LUFS.",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()

    setup_logging(args.output if args.output else args.input)

    if args.read_only:
        print("### PROCESSING STARTED! READ-ONLY MODE ACTIVE!")
        wave_alignment_reader = WaveAlignmentReader(
            input_path=args.input,
            window_size=args.window_size,
        )
        # TODO: optional: make this output usable for further processing
        _, _ = wave_alignment_reader.read()
    else:
        print(
            f"### PROCESSING STARTED! AIMING FOR NEW TARGET:\
            {args.target} dB {args.window_size.name}\n"
        )

        wave_alignment_processor = WaveAlignmentProcessor(
            input_path=args.input,
            output_path=args.output,
            window_size=args.window_size,
            target_level=args.target,
        )
        wave_alignment_processor.process()

    output_logfile_warning(args.output if args.output else args.input)
    print("\n### PROCESSING FINISHED! ###")


if __name__ == "__main__":
    main()
