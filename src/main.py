from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QMenuBar, QMenu
from PyQt6.QtGui import QAction, QFontMetrics, QKeySequence, QTextDocument

import sys
import platform

import saving
import findReplace


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


        editor = QTextEdit()
        editor.setStyleSheet("""color: white; 
                                background-color: #484D5D; 
                                border-style: none; 
                                font: courier new; 
                                font-size: 10pt;""")
        editor.setTabStopDistance(QFontMetrics(editor.font()).horizontalAdvance(' ') * 4) # Changing tab size to 4 spaces 
        document = QTextDocument(fileText)
        editor.setDocument(document)
        self.setCentralWidget(editor)

        
        menuBar = self.menuBar()
        menuBar.setStyleSheet("""color: white; 
                                background-color: #434343;
                                font: Source Sans Pro;
                                """)

        saveAct = QAction("Save", self)
        saveAct.triggered.connect(lambda: saving.save(fileName, self.centralWidget().toPlainText()))
        saveAct.setShortcut(QKeySequence("Ctrl+s"))
                                                        
        saveAsAct = QAction("Save As", self)
        saveAsAct.triggered.connect(lambda: saving.saveAs(self.centralWidget().toPlainText()))
        saveAsAct.setShortcut(QKeySequence("Ctrl+Shift+s"))
        
        findAct = QAction("Find", self)
        findAct.triggered.connect(lambda: findReplace.FindReplacePopup(self.centralWidget()))
        findAct.setShortcut(QKeySequence("Ctrl+f"))

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(saveAct)
        fileMenu.addAction(saveAsAct)
        
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(findAct)


window = MainWindow()
window.show()

sys.exit(app.exec())