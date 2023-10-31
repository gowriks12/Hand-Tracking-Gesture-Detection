from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

APP = ['gestureDetectionApp.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5'],
    'install_requires': requirements,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
