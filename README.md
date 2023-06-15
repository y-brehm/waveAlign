# WaveAlign: Loudness Alignment Processor to end the Loudness War between DJs
[![Tests](https://github.com/y-brehm/waveAlign/actions/workflows/run_tests.yml/badge.svg)](https://github.com/y-brehm/waveAlign/actions/workflows/run_tests.yml)

WaveAlign is a Python command-line tool designed to help put an end to the loudness war between DJs by aligning the loudness levels of songs. 
It supports multiple gain calculation strategies, such as PEAK, RMS, and LUFS. With WaveAlign, you can process audio files in a specified input directory and optionally save the output to a different directory.

# ⚡️Requirements
* [ffmpeg >= 5.1](https://ffmpeg.org/)
* [python >= 3.9](https://www.python.org/)

# 📦Installation
```bash
pip3 install git+https://github.com/y-brehm/waveAlign
```

# 🚀Usage

## Display Argument Parser Help
```bash
python3 -m wavealign.batch_process_files -h
```
## Read-Only Mode: Determine the Minimum Overall Level of Your Songs

````bash
python3 -m wavealign.batch_process_files -i ./your/songs --read_only
````

## Gain Calculation Strategy

You can select between LUFS loudness calculation (default), RMS level calculation, and PEAK level calculation using the -g flag.
Default is set to LUFS. The default setting is LUFS, while RMS and PEAK are not suggested for loudness alignment of entire songs. Instead, they are more suitable for other batch normalization tasks.

## Audio Output Folder

An audio output folder is optional, but be careful, as this will overwrite your original files with the loudness-aligned version.

## Nested Input Folder Structures

Nested input folder structures are supported but will be dissolved in the case of a specified output directory.

## Target Loudness Level

The target is set to -14 dB LUFS by default but is user-adjustable between -10 dB (LUFS, RMS, PEAK) and -30 dB (LUFS, RMS, PEAK).
If you choose a value above the minimum overall LUFS value, clipping will very likely occure.

## Example

Processing files from the ./your/songs folder with a loudness target of -16 dB LUFS, storing the processed files in the ./output folder, and checking for clipping:

````bash
python3 -m wavealign.batch_process_files -i ./your/songs -o ./output -t -16  --check_for_clipping
````

# 😎Full featureset:
```bash
python wavealign.py [-i INPUT] [-o OUTPUT] [-w WINDOW_SIZE] [-g GAIN_CALCULATION_STRATEGY] [-t TARGET] [-r] [-c]
```
## Arguments:

    -i, --input (str): Specify an input directory to look for audio. Nested structures are allowed.
    -o, --output (str): Specify the output directory to save the processed data. If set to None, the original data is overwritten. Nested folder structures will be dissolved.
    -w, --window_size (float, optional): Specify the window size in seconds. Has to be between 0.1 and 10.0. If set to none, LUFS is calculated for the whole file.
    -g, --gain_calculation_strategy (enum, optional): Specify the gain calculation strategy. Use 'PEAK' for peak based calculation, 'RMS' for RMS based calculation, 'LUFS' for LUFS based calculation. Default is LUFS.
    -t, --target (int, optional): Specify the target loudness level in dB. Has to be between -30 and -9. Default is -14.
    -r, --read_only (bool, optional): Run in read-only mode. Only outputs LUFS of input files without processing them. Default is False.
    -c, --check_for_clipping (bool, optional): Check for audio clipping during processing. Processing time will be much longer. Only active if read-only is disabled.


# ✅Run Tests (for developers only)

Requires both `requirements.txt` and `dev_requirements.txt` to be installed:

```bash
pip3 install -r requirements.txt && pip3 install -r dev_requirements.txt
```

After that tests can be run from the main directory:

```bash
python3 -m unittest discover
```
