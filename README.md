# BoothiumEdit

BoothiumEdit is a small, minimalistic GUI text editor writting in Python, using the PyQt6 GUI framework.

## Requirements

- Python 3.10 or above
- PyQt6 installed via pip

## Usage

First, download the code from this repository.

To open the editor, type the following into the shell:
`python [PATH OF BOOTHIUMEDIT FOLDER]/src/main.py [PATH OF FILE TO OPEN]`

Note that the path of the file to open must be the absolute path, rather than the relative path.

### Keyboard Shortcuts

BoothiumEdit allows the use of all standard text editing shortcuts, with a few additions:

- Ctrl-s: Save
- Ctrl-Shift-s: Save As
- Ctrl-f: Find & Replace

The functions of the aforementioned 3 shortcuts can also be accessed in a GUI manner, through the menu bar.

### Settings

BoothiumEdit allows you to edit settings both through a GUI popup, and by directly editing a JSON file called "BEditSettings.json".

To access the settings popup, go to the menu bar and select File > Settings. If you want to open "BEditSettings.json", the popup has a button at the bottom that opens the file in a new editor window.

## Language Support

BoothiumEdit has syntax highlighting support for the the following languages:

- Python
- C
- C++
- JavaScript
- Java
- Go

You can open any text file in the editor, but syntax highlighting will only be applied to the above 6.