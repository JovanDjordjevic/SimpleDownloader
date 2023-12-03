# SimpleDownloader

A simple app to speed up installation of softwre of a fresh Windows 10/11 install.
This software provides a simple GUI to select some commonly used programs for dowload.

Internally, `winget` is used to download and install specified programs.
If a selected program already exists on the system, winget will attempt to upgrade it.

## How to use

Download the latest release archive, unpack it and run the executable

## How to run locally from source(for windows)

Python must be installed on your system.
After cloning the repo, navigate to the repo root folder and run:

```shell
# Create and activate python virtual environment
python -m venv venv
.\venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run the program
python main.py
```
