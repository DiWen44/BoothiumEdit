from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.QtGui import QAction, QKeySequence

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
            self.filePath = sys.argv[1]
        except IndexError: # Handle user not providing a filename
            sys.exit("ERROR: No filename specified")

        try:
            with open(self.filePath, "r") as file:
                fileText = file.read()
        except FileNotFoundError: # Handle user providing nonexistent file
            sys.exit("ERROR: File does not exist")

        # Get name of file without rest of path
        if platform.system() == "Windows": # Account for windows using "\" as path seperator rather than "/"
            pathSeperator = '\\' # Double backslash to escape the first backslash
        else:
            pathSeperator = '/'
            
        lastPathSepIndex = self.filePath[::-1].index(pathSeperator) # Reverse file path to facilitate getting index of last path seperator 
        fileNameNoPath = ((self.filePath[::-1])[:lastPathSepIndex])[::-1] # Get characters of reverse path that precede last path seperator, then reverse this to get them finally in the right order

        self.setWindowTitle("BoothiumEdit - " + fileNameNoPath)

        editor = Editor(fileText)
        self.setCentralWidget(editor)

        menuBar = self.menuBar()
        menuBar.setStyleSheet("""color: white; 
                                background-color: #3d506e;
                                font: Garet;
                                font-size: 13pt;
                                """)

        saveAct = QAction("Save", self)
        saveAct.triggered.connect(lambda: saving.save(self.filePath, self.centralWidget().toPlainText()))
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


    # Reimplementation of QWidget.closeEvent(). Prompts user to save if text in editor is discrepant from text in file 
    def closeEvent(self, event):

        editorText = self.centralWidget().toPlainText()

        with open(self.filePath, "r") as file:
            fileText = file.read()

        if editorText != fileText:

            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("BoothiumEdit")
            msgBox.setText("You have unsaved changes. Do you want to save these changes before exiting?")

            save = QPushButton("Save")

            def saveAndExit(newText):
                saving.save(self.filePath, newText)
                self.close()

            save.clicked.connect(lambda: saveAndExit(editorText))
            msgBox.addButton(save, QMessageBox.ButtonRole.AcceptRole)

            discard = QPushButton("Discard")
            discard.clicked.connect(lambda: self.close())
            msgBox.addButton(discard, QMessageBox.ButtonRole.RejectRole)

            msgBox.exec()

    

window = MainWindow()
window.show()

sys.exit(app.exec())