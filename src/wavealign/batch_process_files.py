import argparse

from wavealign.loudness_processing.window_size import WindowSize
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
        help="Specify the target loudness level in dB. Has to be between -30 and -9.",
        metavar="-30 <= target <= -10",
        choices=range(-30, -5),
        type=int,
        default=-12,
    )
    parser.add_argument(
        "-r",
        "--read_only",
        help="Run in read only mode. Only outputs LUFS of input files without processing them.",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()

    if args.read_only:
        print("### PROCESSING STARTED! READ-ONLY MODE ACTIVE!")
    else:
        print(
            f"### PROCESSING STARTED! AIMING FOR NEW TARGET:\
            {args.target} dB {args.window_size.name}\n"
        )

    wave_alignment_processor = WaveAlignmentProcessor()
    wave_alignment_processor.process(
        input_path=args.input,
        output_path=args.output,
        window_size=args.window_size,
        user_target_level=args.target,
        read_only=args.read_only,
    )

    print("\n### PROCESSING FINISHED! ###")


if __name__ == "__main__":
    main()
