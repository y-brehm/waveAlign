from glob import glob
from os.path import splitext, basename
from setuptools import setup, find_packages

# TODO: switch to toml
# TODO: move to python 3.11 (optional type hints)
setup(
    name="waveAlign",
    version="1.0.0",
    description="A python package for loudness alignment of audio files.",
    url="https://github.com/y-brehm/waveAlign",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    python_requires=">=3.9.*",
    install_requires=[
        "pyloudnorm==0.1.1",
        "numpy==1.24.3",
        "pyyaml==6.0.1",
        "librosa==0.10.0",
        "music-tag==0.4.3",
        "ffmpegio==0.8.3",
        "pyloudnorm==0.1.1",
    ],
    # TODO: check if extras required works
    extras_require={"dev": [
        "mock == 4.0.3",
        "parameterized == 0.8.1",
        "pytest == 7.4.0"
    ]},
)
