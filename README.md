# WaveAlign: Loudness Alignment Processor to end the Loudness War between DJs
[![Tests](https://github.com/y-brehm/waveAlign/actions/workflows/run_tests.yml/badge.svg)](https://github.com/y-brehm/waveAlign/actions/workflows/run_tests.yml)

WaveAlign is a Python command-line tool designed to help put an end to the loudness war between DJs by aligning the loudness levels of songs. 
It aligns all input audio files according to their LUFS level. With WaveAlign, you can process audio files in a specified input directory and optionally save the output to a different directory.

# ⚡️Requirements
* [ffmpeg >= 5.1](https://ffmpeg.org/)
* [python >= 3.11](https://www.python.org/)

# 📦Installation
```bash
pip3 install git+https://github.com/y-brehm/waveAlign
```

# 🚀Usage

## Display Argument Parser Help
```bash
python3 -m wavealign.batch_process_files -h
```
## Read-Only Mode: Determine the LUFS levels of your songs and an overall possible maximum LUFS level without clipping for your library

````bash
python3 -m wavealign.batch_process_files -i ./your/songs --read_only
````

## Audio Output Folder

An audio output folder is optional, but be careful, if you don't use one this will overwrite your original files with the loudness-aligned versions.

## Nested Input Folder Structures

Nested input folder structures are supported but will be dissolved in the case of a specified output directory.

## Target Loudness Level

The target is set to -12 dB LUFS by default but is user-adjustable between -10 dB LUFS and -30 dB LUFS.
If you choose a value that is too high and would result in clipping, wavAlign will skip all potentially clipped files.
Therefore WaveAlign never clips. Check the log file that is created in the case of theoretical clipping to see which files were skipped.

## Caching
WaveAlign employs an efficient caching mechanism to optimize its processing time. 
This mechanism revolves around the creation and utilization of a cache YAML file, which is generated in the input folder each time WaveAlign is run.
The cache file serves as a record of the files that have been processed in previous runs. 
It contains essential information such as the last modification time and the target LUFS level for each processed file.
When WaveAlign is run, it reads the cache file and checks each file in the input folder against the cache. 
If a file has been processed before, WaveAlign checks whether the file has been modified since the last run and whether the target LUFS level is the same as in the previous run. 
If both conditions are met, WaveAlign will skip the file, saving processing time.

## Example

Processing files from the ./your/songs folder with a loudness target of -16 dB LUFS, storing the processed files in the ./output folder:

````bash
python3 -m wavealign.batch_process_files -i ./your/songs -o ./output -t -16
````

## Recommended Usage
To make the most of WaveAlign, we recommend making it a habit to run WaveAlign on your USB stick every time you export something from Rekordbox to the stick.
To do so simply run:
````bash
python3 -m wavealign.batch_process_files -i ./<path_to_your_stick>
````
This simple practice will ensure that your music library is always loudness-aligned, ready for your next gig.
Running WaveAlign on your USB stick has an additional advantage: It leaves your original music library on your PC untouched. 
This means you always have access to your original files, while your USB stick carries the loudness-aligned tracks for your gigs.
The default settings of WaveAlign, -12 LUFS (target level) and LUFS-S (window size), are optimized for most use cases, so there's usually no need to specify a user target level or a different target window.
One of the key features of WaveAlign is its efficient caching mechanism. 
If you overwrite or change something on the USB stick after processing with WaveAlign, just run WaveAlign again. 
It will skip any files that have already been processed and haven't changed since the last run, saving you time.
Of course, if you prefer, you can also run WaveAlign directly on your entire music library on your PC. In this case you only have to run WaveAlign again once you add new tracks. 

# 😎Full featureset:
```bash
python wavealign.py [-i INPUT] [-o OUTPUT] [-w WINDOW_SIZE] [-t TARGET] [-r]
```

## Arguments:

    -i, --input (str): Specify an input directory to look for audio. Nested structures are allowed.
    -o, --output (str): Specify the output directory to save the processed data. If set to None, the original data is overwritten. Nested folder structures will be dissolved.
    -w, --window_size (enum, optional): Specify the window size. Follows the Reaper LUFS calculation windows: LUFS-S (3 seconds), LUFS-M (4 seconds), LUFS-I (integrated - whole file)
    -t, --target (int, optional): Specify the target loudness level in dB. Has to be between -30 and -9. Default is -14.
    -r, --read_only (bool, optional): Run in read-only mode. Only outputs LUFS of input files without processing them. Also outputs library dependent maximum LUFS. Default is False.

# ✅Run Tests (for developers only)
Make sure you have [poetry](https://python-poetry.org/) installed.

Create a local virtual environment using poetry and activate it:
```bash
cd <path_to_wavealign_repository>
poetry install
poetry shell
```
After that tests can be run from the main directory:
```bash
pytest
```
