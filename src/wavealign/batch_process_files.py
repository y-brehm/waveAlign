import argparse

from wavealign.wave_alignment import wave_alignment


def main():
    parser = argparse.ArgumentParser(
        description='Song loudness alignment processor for ending the loudness war.'
    )
    parser.add_argument(
        '-i',
        '--input',
        help="specify directory to look for audio.",
        type=str,
    )
    parser.add_argument(
        '-o',
        '--output',
        help="specify the output directory to save the processed data. "
             "If set to None the original data is overwritten.",
        type=str
    )
    parser.add_argument(
        '-t',
        '--target',
        help="specify the target loudness level in dB LUFS.",
        metavar='-30 <= target <= -10',
        choices=range(-30, -9),
        type=int,
        default=-14
    )
    parser.add_argument(
        '-c',
        '--clipping_check',
        help="check for audio clipping during processing. Longer processing.",
        type=bool,
        default=False
    )
    args = parser.parse_args()

    print(f"### PROCESSING STARTED! AIMING FOR NEW TARGET LUFS: {args.target} \n")

    wave_alignment(
            input_path=args.input,
            output_path=args.output,
            target_lufs=args.target,
            check_for_clipping=args.clipping_check
            )

    print("\n### PROCESSING SUCCESSFULLY FINISHED! THANK YOU FOR HELPING TO END THIS BULLSHIT! ###")


if __name__ == "__main__":
    main()
