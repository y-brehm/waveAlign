import argparse

from wavealign.wave_alignment import wave_alignment


def main():
    parser = argparse.ArgumentParser(
        description='Song loudness alignment processor for ending the loudness war.'
    )
    parser.add_argument(
        '-i',
        '--input',
        help="Specify an input directory to look for audio. Nested structures are allowed.",
        type=str,
    )
    parser.add_argument(
        '-o',
        '--output',
        help="Specify the output directory to save the processed data. "
             "If set to None the original data is overwritten."
             "Nested folder structures will be  disolved.",
        type=str
    )
    parser.add_argument(
        '-t',
        '--target',
        help="Specify the target loudness level in dB LUFS. Has to be between -30 and -9.",
        metavar='-30 <= target <= -10',
        choices=range(-30, -9),
        type=int,
        default=-14
    )
    parser.add_argument(
        '-c',
        '--clipping_check',
        help="Check for audio clipping during processing. Processing time will be much longer.",
        type=bool,
        default=False
    )
    parser.add_argument(
            '-r',
            '--read_only',
            help="Run in read only mode. Only outputs LUFS of input files without processing them.",
            type=bool,
            default=True
            )
    args = parser.parse_args()

    print(f"### PROCESSING STARTED! AIMING FOR NEW TARGET LUFS: {args.target} \n")

    wave_alignment(
            input_path=args.input,
            output_path=args.output,
            target_lufs=args.target,
            check_for_clipping=args.clipping_check,
            read_only=args.read_only
            )

    print("\n### PROCESSING SUCCESSFULLY FINISHED! THANK YOU FOR HELPING TO END THIS BULLSHIT! ###")


if __name__ == "__main__":
    main()
