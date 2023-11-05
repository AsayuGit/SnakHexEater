
# SnakHexEater

A simple hex editor witten in python

[![GPLv2 License](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://opensource.org/licenses/)
## Features

- Load file from disk
- Load file from an HTTP/HTTPS url
- Save file modifications to disk
- Display exif data
- Exif json export
- Display file metadata

## Dependencies

To run SnakHexEater needs python3 and the following pip modules :
- overrides
- Pillow
- PySide6
- PySide6-Addons
- PySide6-Essentials
- shiboken6

## How to run :

```bash
  cd SnakHexEater
  python3 -m venv ./venv
  source venv/bin/activate
  pip install -r requirements.txt
  python3 main.py
```

## Authors

- [@AsayuGit](https://github.com/AsayuGit)

## FAQ

#### What are the supported OS for SnakHexEater ?

SnakHexEater is build with python so it should be able to run on any OS where python3 is installed.