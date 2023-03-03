# waveAlign
Python repo for audio loudness matching to end the loudness war between DJs.

# Installation
Requires python3.9 installed on your system.

```
pip install git+https://github.com/y-brehm/waveAlign
```

# Usage

The current version only works with .wav files. All processed files will be stored with the original sample rate and a 16-bit integer bit depth.

For showing the argument parser help:
````
python -m wavealign.batch_process_files -h
````

To start processing you need to specify an audio input folder. An audio output folder is optional but be careful since this will overwrite your original files with the loudness-aligned version.

Nested input folder structures are supported but will be dissolved in the case of a specified output directory.

Target LUFS is set to -14 by default but is user adjustable between -10 dB and -30 dB LUFS.

Example for processing files from the `./input` folder with a loudness target of `-14` dB LUFS, storing the processed files in the `./output` folder:

````
python -m wavealign.batch_process_files -i ./input -o ./output -t -14
````
