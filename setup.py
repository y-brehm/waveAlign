from glob import glob
from os.path import splitext, basename
from setuptools import setup, find_packages

# TODO: switch to toml #25
# TODO: move to python 3.11 (optional type hints) #26
# TODO: add dev requirements here and check if there is a way to get rid of dev/requirements.txt #27

setup(
    name="waveAlign",
    version="1.0.0",
    description="A python package for loudness alignment of audio files.",
    url="https://github.com/y-brehm/waveAlign",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    python_requires=">=3.11.*",
    install_requires=[
        "pyloudnorm==0.1.1",
        "numpy==1.24.3",
        "pyyaml==6.0.1",
        "librosa==0.10.0",
        "music-tag==0.4.3",
        "ffmpegio==0.8.3",
        "pyloudnorm==0.1.1",
    ],
)
