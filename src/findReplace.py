from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QMessageBox, QTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor



""" 
Represents the popup containing the find & replace functionality

CONSTRUCTOR PARAMETERS:
    editor - The QTextEditor representing the code editor textbox.
"""
class FindReplacePopup(QDialog):


    def __init__(self, editor):

        super().__init__()

        self.setFixedSize(300, 100)
        self.setWindowTitle("Find & Replace")
        self.setStyleSheet("""color: white; 
                            background-color: #0E0E10;
                            font: Garet;""")

        self.editor = editor 
        self.document = editor.document()

        self.instances = [] # Array of QTextCursors - stores the cursors that select individual occurences of found text.

        layout = QGridLayout()

        textBoxStyle = "background-color: #151821; border-style: none;"
        btnStyle = "background-color: #151821; border-style: none;"

        findBox = QLineEdit(self)
        findBox.setFixedSize(120, 20)
        findBox.setStyleSheet(textBoxStyle)
        findBox.setPlaceholderText("Find")
        findBox.returnPressed.connect(lambda: self.__find(findBox.text()))
    
        next = QPushButton("Next", self)
        next.setFixedSize(60, 20)
        next.setStyleSheet(btnStyle)
        next.clicked.connect(self.__nextInstance)

        previous = QPushButton("Previous", self)
        previous.setFixedSize(60, 20)
        previous.setStyleSheet(btnStyle)
        previous.clicked.connect(self.__prevInstance)

        layout.addWidget(findBox, 0, 0)    
        layout.addWidget(next, 0, 1)
        layout.addWidget(previous, 0, 2)

        repBox = QLineEdit(self)
        repBox.setFixedSize(120, 20)
        repBox.setStyleSheet(textBoxStyle)
        repBox.setPlaceholderText("Replace")

        replace = QPushButton("Replace", self)
        replace.setFixedSize(65, 20)
        replace.setStyleSheet(btnStyle)
        replace.clicked.connect(lambda: self.__replace(repBox.text()))

        replaceAll = QPushButton("Replace All", self)
        replaceAll.setFixedSize(65, 20)
        replaceAll.setStyleSheet(btnStyle)
        replaceAll.clicked.connect(lambda: self.__replaceAll(repBox.text()))

        layout.addWidget(repBox, 1, 0)
        layout.addWidget(replace, 1, 1)
        layout.addWidget(replaceAll, 1, 2)

        self.setLayout(layout)
        self.exec()

    
    # When user presses exit button, remove highlights before closing (Reimplementation of QWidget.closeEvent()).
    def closeEvent(self, event):
        self.__unhighlight()
        self.close()


    """
    Gets instances of searchTerm, adds the positions of these instances to self.instances[], and highlights the instances in the editor. 
    The user's cursor will be moved to select the first instance

    PARAMETERS:
        searchTerm - The text to search for.
    """
    def __find(self, searchTerm):

        # Exit function if no text was entered
        if searchTerm == "":
            return

        document = self.document
        text = document.toPlainText()

        self.__unhighlight() # Remove previous highlights from the document that were created by a previous call to this function.
        self.instances = [] # Clear instances array of any instances left over from a previous function call.

        isDiff = False # Flag indicating whether text being examined is discrepant from searchTerm

        for i in range(len(text)):
                
                if text[i] == searchTerm[0]: # Look for first character of searchTerm

                    if len(searchTerm) == 1: # As we have established that the first characters are equal, if the searchTerm only has 1 character then we can conclude the scanning of this particular instance.
                        offset = 0 # There is no offset if searchTerm only has 1 character.
                    
                    else:
                        for offset in range(1, len(searchTerm)): # Range starts at 1, not 0, as we have already established that the first characters are equal.
                            if searchTerm[offset] != text[i + offset]:
                                isDiff = True
                                break
                        
                    if not isDiff:

                        start = i 
                        end = i + offset + 1  # Note that because QTextCursor positions itself between characters, the cursors final position must be offset + 1.

                        cursor = QTextCursor(self.document)
                        cursor.setPosition(start, QTextCursor.MoveMode.MoveAnchor) # Navigate cursor to instance.
                        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor) # Select whole instance by moving position to end of instance but maintaining anchor at beginning.
                        self.instances.append(cursor)

                    isDiff = False # Reset difference flag.

        if self.instances == []: # In case no instances are found
            msgBox = QMessageBox()
            msgBox.setWindowTitle("BoothiumEdit")
            msgBox.setText(f"Couldn't find '{searchTerm}'")
            msgBox.exec()

        else:

            highlightFmt = QTextCharFormat() 
            highlightFmt.setBackground(QColor("#40d4db"))

            for instanceCursor in self.instances:
                instanceCursor.setCharFormat(highlightFmt) # Apply highlighting

            self.editor.setTextCursor(self.instances[0]) # Have user's cursor select first instance
        

    # Removes highlighting from document that was created by __find(). 
    def __unhighlight(self):

        defaultFmt = QTextCharFormat() 
        defaultFmt.setBackground(QColor("#0E0E10")) # Background will be reset to the background color of the editor 
        cursor = QTextCursor(self.document)

        cursor.setPosition(len(self.document.toPlainText()), QTextCursor.MoveMode.KeepAnchor) # Select entire document
        cursor.setCharFormat(defaultFmt)


    # Moves user's cursor to next instance  
    def __nextInstance(self):

        if len(self.instances) <= 1: # There is no next instance if there is only 1 instance, so exit the function in that case. If there are no instances, the user pressed the button without any instances having been found.
            return

        currentCursor = self.editor.textCursor()
        newCursor = QTextCursor(self.document)

        for i in range(len(self.instances)): # Find instance which user's current cursor is at.

            if self.instances[i] == currentCursor:

                try:
                    newCursor = self.instances[i + 1]
                except IndexError: # Raised if there is no instance after the currently selected one. In this case, put the cursor back to the first instance.
                    newCursor = self.instances[0]
                    
        self.editor.setTextCursor(newCursor) 


    # Moves user's cursor to previous instance
    def __prevInstance(self):        

        if len(self.instances) <= 1: # There is no previous instance if there is only 1 instance, so exit the function in that case. If there are no instances, the user pressed the button without any instances having been found.
            return

        currentCursor = self.editor.textCursor()
        newCursor = QTextCursor(self.document)

        for i in range(len(self.instances)): # Find instance which user's current cursor is at.

            if self.instances[i] == currentCursor:

                try:
                    newCursor = self.instances[i - 1]
                except IndexError: # Raised if there is no instance before the currently selected one. In this case, put the cursor to the last instance.
                    newCursor = self.instances[len(self.instances) - 1]
                    
        self.editor.setTextCursor(newCursor) 


    """
    Replace instance of found text on which the user's cursor is positioned with new text, 
    moving the user's cursor to next instance in the process.

        PARAMETERS:
            newText - The text to replace the selected instance with.
    """
    def __replace(self, newText):

        if newText == "" or self.instances == []:
            return
        
        cursorForInstance = self.editor.textCursor()

        # Removing highlighting from instance.
        defaultFmt = QTextCharFormat() 
        defaultFmt.setBackground(QColor("#0E0E10")) # Background will be reset to the background color of the editor 
        cursorForInstance.setCharFormat(defaultFmt)

        self.__nextInstance()

        # Remove instance to be replaced from self.instances
        for i in self.instances:
            if i.anchor() == cursorForInstance.anchor():
                self.instances.remove(i)
                break

        cursorForInstance.insertText(newText) # insertText() also deletes current selection before inserting new text


    """
    Replace all instances of found text in file with new text.

        PARAMETERS:
            newText - The text to replace the selected instance with.
    """
    def __replaceAll(self, newText):
        
        if newText == "" or self.instances == []:
            return

        for i in range(len(self.instances)):
            self.__replace(newText)

        self.__unhighlight() # Remove all highlighting from document now that all instances have been replaced.