from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QMenuBar, QMenu
from PyQt6.QtGui import QAction, QKeySequence, QTextDocument

import sys
import platform

from editor import Editor
import saving
import findReplace
import settings


app = QApplication([])


class MainWindow(QMainWindow):
	
    def __init__(self):

        super().__init__()

        self.setGeometry(100, 100, 1000, 1000)
        self.setMinimumSize(500, 500)

        # Getting file from command line arguments
        try:
            fileName = sys.argv[1]
        except IndexError: # Handle user not providing a filename
            # TESTING ONLY: fileName = "C:\\Users\\devin\\OneDrive\\Documents\\BoothiumEdit\\test.txt"
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
        fileNameNoPath = ((fileName[::-1])[:lastPathSepIndex])[::-1] # Get characters of reverse path that precede last path seperator, then reverse this to get them finally in the right order

        self.setWindowTitle("BoothiumEdit - " + fileNameNoPath)

        editor = Editor(fileText)
        self.setCentralWidget(editor)

        menuBar = self.menuBar()
        menuBar.setStyleSheet("""color: white; 
                                background-color: #404040;
                                font: Garet;
                                font-size: 13pt;
                                """)

        saveAct = QAction("Save", self)
        saveAct.triggered.connect(lambda: saving.save(fileName, self.centralWidget().toPlainText()))
        saveAct.setShortcut(QKeySequence("Ctrl+s"))
                                                        
        saveAsAct = QAction("Save As", self)
        saveAsAct.triggered.connect(lambda: saving.saveAs(self.centralWidget().toPlainText()))
        saveAsAct.setShortcut(QKeySequence("Ctrl+Shift+s"))

        settingsAct = QAction("Settings", self)
        settingsAct.triggered.connect(settings.SettingsPopup)

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(saveAct)
        fileMenu.addAction(saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(settingsAct)

        findAct = QAction("Find", self)
        findAct.triggered.connect(lambda: findReplace.FindReplacePopup(self.centralWidget()))
        findAct.setShortcut(QKeySequence("Ctrl+f"))

        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(findAct)


window = MainWindow()
window.show()

sys.exit(app.exec())