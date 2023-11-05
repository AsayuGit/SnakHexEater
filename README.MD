
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

## How to use:

### Opening a local file

Upon launch you'll be greated by the main menu of SnakHexEater.

In the file menu you will find the differents methods of opening a file. To open a file
locally click on the Open File Item.

![](screens/Main%20Menu.png)

This will open the file picker dialog were you will be able to open a file from the disk

![](screens/Open%20File.png)

Once loaded you'll be able to view and edit the hex date as well as the plain text data.

If you loaded an image you will be able to review the exif data as well.

![](screens/Local%20File%20loaded.png)

### Opening a remote file

To open a remote file go to the file menu then click on Open Remote File

![](screens/Open%20Remote%20file.png)

This will open the remote file dialog where you need to input the url of the file to open

![](screens/Open%20Remote%20file%20dialog.png)

Once loaded you'll be able to edit it just the same as a local file.

Note that since its a remote file you're able to view the http header and request info
as well

![](screens/Remote%20file%20header.png)

![](screens/Remote%20File%20Info.png)

To save go to the save menu and click Save this will bring up the save dialog were you
will be able to save the file on your disk.

![](screens/Save%20dialog.png)

## Authors

- [@AsayuGit](https://github.com/AsayuGit)

## FAQ

#### What are the supported OS for SnakHexEater ?

SnakHexEater is build with python so it should be able to run on any OS where python3 is installed.