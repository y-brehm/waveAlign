from glob import glob
from os.path import splitext, basename
from setuptools import setup, find_packages


setup(
    name='waveAlign',
    version=1.0,
    description="A python package for loudness alignment of audio files (currently .wav only).",
    url='https://github.com/y-brehm/waveAlign',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    python_requires='==3.9.*',
    install_requires=[
        'pyloudnorm==0.1.1',
        'numpy==1.22.0',
        'librosa==0.10.0',
        'pyloudnorm==0.1.1',
        ],
)
