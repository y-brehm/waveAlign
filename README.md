<h1 align="center">
waveAlign
</h1>

<p align="center">
<i align="center"><b>End the Loudness War between DJs</b></i>
</p>

<h4 align="center">
  <a href="https://github.com/y-brehm/waveAlign/actions/workflows/run_tests.yml">
    <img src="https://github.com/y-brehm/waveAlign/actions/workflows/run_tests.yml/badge.svg"
    alt="testing status" style="height: 20px;">
  </a>
  <a href="">
    <img src="" alt="LICENSE PLACEHOLDER" style="height: 20px">
  </a>
</h4>

<p style='text-align: justify;'>
WaveAlign is a Python command-line tool designed to end the loudness war between
DJs by aligning the loudness levels of songs to a specific LUFS level.
Loudness Units relative to Full Scale (LUFS) alignment provides several
advantages as compared to peak normalization:
<ul>
  <li><b>Consistent perceived loudness: </b>
      LUFS measurement aligns with human loudness perception
  </li>
  <li><b>Dynamic range preservation: </b>
      No compression maintains natural dynamics of tracks
  </li>
  <li><b>Better transient handling: </b>
      Average loudness over time allows better management of transient-rich tracks
  </li>
</ul>

It was developed with DJs in mind, which is why all waveAligned tracks retain
their metadata as well as timing accuracy for lossy formats (e.g. mp3).
The integrity and accuracy of meticulously created cue points within tools such as
Rekodbox(R) remains unchanged at their respective positions prior to processing.
</p>
<p align="center">
  <a href="#quickstart">Quickstart</a> •
  <a href="#details">Details</a> •
  <a href="#full-featureset">Full Featureset</a> •
  <a href="#run-tests">Run Tests</a>
</p>

## Quickstart

### ⚡️ Requirements

* [ffmpeg >= 5.1](https://ffmpeg.org/)
* [python >= 3.11](https://www.python.org/)

### 📦 Installation

```bash
pip3 install git+https://github.com/y-brehm/waveAlign
```

### 🚀 Usage

##### Display Argument Parser Help

```bash
python3 -m wavealign.batch_process_files -h
```

##### Start with Read-Only Mode

Determine the LUFS levels of your songs and an overall possible maximum LUFS level
without clipping for your library.

````bash
python3 -m wavealign.batch_process_files -i ./your/songs --read_only
````

##### Select an Audio Output Folder

An audio output folder is optional, however not specifying it will overwrite
your original files with the loudness-aligned versions. Nested input folder
structures are supported but will be dissolved in the case of a specified
output directory.

##### Target Loudness Level

The default target is set to -12 dB LUFS, but is user-adjustable between -10 dB
LUFS and -30 dB LUFS. If a target value would result in clipping, waveAlign
will skip all potentially clipped filed. Additionally a log file is created
with information on skipped files.

##### Example

Processing files from the ./your/songs folder with a loudness target of -16 dB
LUFS, storing the processed files in the ./output folder:

````bash
python3 -m wavealign.batch_process_files -i ./your/songs -o ./output -t -16
````

## Details

### 🎶 Supported file types

placeholderplaceholder

### 🔌 waveAlignment of your USB Stick

We recommend running waveAlign on your USB stick every time you export new
tracks from your library management tool (e.g. Rekordbox(r)).
Simply run:

````bash
python3 -m wavealign.batch_process_files -i ./<path_to_your_stick>
````

This will ensure that your mobile music library is always loudness-aligned.

Running waveAlign on your USB stick has an additional advantage: It leaves
your original music library on your PC untouched. This means you always have
access to your original files, while your USB stick carries the
loudness-aligned tracks for your gigs.  

### 💻 waveAlignment of your library

While it is recommended to use waveAlign directly on the files on your USB stick,
it is also possible to run waveAlign on your full music library. Please make sure
to backup your source files before running. Also you will need to re-analyze your
files within your music library tool (e.g. Rekordbox(r)) after waveAlignment.

All metadata as well as timing information, such as cue points, will be retained
after processing your library. This is also true for lossy formats (e.g. mp3)
which usually require de-coding and en-coding for processing.

In case you add new tracks after processing just run waveAlign again.

### 🎛️ Detailed preferences

The default settings of WaveAlign, -12 LUFS (target level) and LUFS-S
(window size), are optimized for most use cases, so there's usually
no need to specify a user target level or a different target window.

## Full featureset

```bash
python wavealign.py [-i INPUT] [-o OUTPUT] [-w WINDOW_SIZE] [-t TARGET] [-r]
```

### 📋 Arguments

    -i, --input (str): Specify an input directory to look for audio. Nested structures are allowed.
    -o, --output (str): Specify the output directory to save the processed data. If set to None, the original data is overwritten. Nested folder structures will be dissolved.
    -w, --window_size (enum, optional): Specify the window size. Follows the Reaper LUFS calculation windows: LUFS-S (3 seconds), LUFS-M (4 seconds), LUFS-I (integrated - whole file)
    -t, --target (int, optional): Specify the target loudness level in dB. Has to be between -30 and -9. Default is -14.
    -r, --read_only (bool, optional): Run in read-only mode. Only outputs LUFS of input files without processing them. Also outputs library dependent maximum LUFS. Default is False.
    -v, --verbose (bool, optional): Save additional debugging information in log file.

### 💾 Caching

WaveAlign employs an efficient caching mechanism to optimize its processing time.
Caching makes use of a YAML file, which is generated in the input folder after
each run. The cache file is a record of all processed files in previous runs including
the filepath, last modification time and target LUFS.  

When running waveAlign the cache file is read and input files are checked
against the cache. The input file is skipped if the file path, last
modification date as well as current LUFS target setting match with cache data.

If you apply changes to your USB stick after waveAlignment, just re-run the waveAlign.

## Run Tests

Make sure you have [poetry](https://python-poetry.org/) installed.

Create a local virtual environment using poetry and activate it:

```bash
cd <path_to_wavealign_repository>
poetry install --with dev
poetry shell
```

After that tests can be run from the main directory:

```bash
pytest
```
