# PyQt6 imports
from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QToolBar
from PyQt6.QtGui import QAction, QFontMetrics, QKeySequence

# Python standard lib imports
import sys
import platform
import json

# Local file imports
import saving
import findReplace


# Initialize PyQt app
app = QApplication([])


# Getting file from command line arguments
try:
	fileName = sys.argv[1]
except IndexError: # Handle user not providing a filename
	sys.exit("ERROR: No filename specified")

try:
	file = open(fileName, "r+")
except FileNotFoundError: # Handle user providing nonexistent file
	sys.exit("ERROR: File does not exist")

fileText = file.read()


# Get name of file without rest of path
if platform.system() == "Windows": # Account for windows using "\" as path seperator rather than "/"
	pathSeperator = '\\' # Double backslash to escape the first backslash
else:
	pathSeperator = '/'

lastPathSepIndex = fileName[::-1].index(pathSeperator) # Reverse file path to facilitate getting index of last path seperator 
fileNameNoPath = ((fileName[::-1])[:lastPathSepIndex])[::-1] # get characters of reverse path that precede last path seperator, then reverse this to get them finally in the right order


# Setup for window widget
window = QMainWindow()
window.setWindowTitle("BoothiumEdit - " + fileNameNoPath)
window.setGeometry(100, 100, 1000, 1000)
window.setMinimumSize(500, 500)


# Setup for code editor
editor = QTextEdit()
editor.setStyleSheet("""color: white; 
						background-color: #484D5D; 
						border-style: none; 
						font: courier new; 
						font-size: 10pt;""")
editor.setTabStopDistance(QFontMetrics(editor.font()).horizontalAdvance(' ') * 4) # Changing tab size to 4 spaces 
window.setCentralWidget(editor)
editor.insertPlainText(fileText)


# Setup for toolbar
toolbar = QToolBar("Toolbar")
toolbar.setStyleSheet("""color: white; 
						background-color: #434343;
						font: Source Sans Pro;""")

# Toolbar actions setup: Save, Save As & Find W/ keyboard shortcuts
save = QAction("Save")
save.triggered.connect(lambda: saving.save(fileName, editor.toPlainText()))
save.setShortcut(QKeySequence("Ctrl+s"))
toolbar.addAction(save)
												
saveAs = QAction("Save As")
saveAs.triggered.connect(lambda: saving.saveAs(editor.toPlainText()))
saveAs.setShortcut(QKeySequence("Ctrl+Shift+s"))
toolbar.addAction(saveAs)

find = QAction("Find")
find.triggered.connect(lambda: findReplace.find())
find.setShortcut(QKeySequence("Ctrl+f"))
toolbar.addAction(find)

window.addToolBar(toolbar)

																		
window.show()

sys.exit(app.exec())