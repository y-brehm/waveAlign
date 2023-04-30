# waveAlign
Python repo for audio loudness matching to end the loudness war between DJs.

#⚡️Requirements
* [ffmpeg >= 5.1](https://ffmpeg.org/)
* [python >= 3.9](https://www.python.org/)

#📦Installation
```
pip3 install git+https://github.com/y-brehm/waveAlign
```

#🚀Usage
For showing the argument parser help:

````
python3 -m wavealign.batch_process_files -h
````

To start processing you need to specify an audio input folder. It makes sense to first of all set the `--read_only` flag to determine the minimum overall LUFS value of your songs:

````
python3 -m wavealign.batch_process_files -i ./your/songs --read_only
````

Then use this to actually process and loudness align your songs.
If you choose a value above the minimum overall LUFS value, clipping will very likely occure. 

An audio output folder is optional but be careful since this will overwrite your original files with the loudness-aligned version.

Nested input folder structures are supported but will be dissolved in the case of a specified output directory.

Target is set to -14 dB LUFS by default, but is user adjustable between -10 dB LUFS and -30 dB LUFS.

Example for processing files from the `./your/songs` folder with a loudness target of `-16` dB LUFS, storing the processed files in the `./output` folder, 
while checking for clipping:

````
python3 -m wavealign.batch_process_files -i ./your/songs -o ./output -t -16  --check_for_clipping
````

#✅Run Tests (for developers only)

Requires both `requirements.txt` and `dev_requirementes.txt` to be installed:

```
pip3 install -r requirementes.txt && pip3 install -r dev_requirementes.txt
```

After that tests can be run from the main directory:

```
python3 -m unittest discover
```
