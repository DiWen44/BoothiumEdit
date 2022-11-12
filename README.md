# BoothiumEdit

BoothiumEdit is a small, minimalistic GUI text editor writting in Python, using the PyQt6 GUI framework.

## Requirements

Python 3.10 or above
PyQt6 installed via pip

## Usage

First, download the code from this repository.

To open the editor, type the following into the shell:
`python [PATH OF BOOTHIUMEDIT FOLDER]/main.py [PATH OF FILE TO OPEN]`

### Keyboard Shortcuts

BoothiumEdit allows the use of all standard text editing shortcuts, with a few additions:

    - Ctrl-s: Save
    - Ctrl-Shift-s: Save As
    - Ctrl-f: Find & Replace

The functions of the aforementioned 3 shortcuts can also be accessed in a GUI manner, through the menu bar.

### Settings

BoothiumEdit allows you to edit settings both through a GUI popup, and by directly editing a JSON file called "BEditSettings.json".

## Language Support

BoothiumEdit has syntax highlighting support for the the following languages:

    - Python
    - C
    - C++
    - JavaScript
    - Java
    - Go

Language support can be added manually by editing the "BEditSettings.json" file.