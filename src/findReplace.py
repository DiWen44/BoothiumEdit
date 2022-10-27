from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QMessageBox, QTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor



""" 
Represents the popup containing the find & replace functionality

CONSTRUCTOR PARAMETERS:
    editor - The code editor.
"""
class FindReplacePopup(QDialog):



    def __init__(self, editor):

        super().__init__()

        self.setFixedSize(300, 100)
        self.setWindowTitle("Find & Replace")
        self.setStyleSheet("""color: white; 
                            background-color: #484D5D;
                            font: Source Sans Pro;""")

        self.editor = editor 
        self.instances = [] # 2D array - Stores positions of the start & end of all found text instances in form: [start, end] 
        """
        Note: Because each subarray of self.instances[] is designed to hold the anchor (start) and position (end) of a hypothetical QTextCursor that selects the instance, 
        the second element of the subarray (i.e the "end") will be 1 + the position of the final character of the instance within the document.
        This is because a QTextCursor positions itself BETWEEN characters, so the end of the cursor's selection is between the last character of the instance and the following character
        """

        layout = QGridLayout()

        findBox = QLineEdit(self)
        findBox.setFixedSize(120, 20)
        findBox.setStyleSheet("background-color: #151821; border-style: none;")
        findBox.setPlaceholderText("Find")
        findBox.returnPressed.connect(lambda: self.__find(findBox.text()))
    
        next = QPushButton("Next", self)
        next.setFixedSize(60, 20)
        next.clicked.connect(self.__nextInstance)

        previous = QPushButton("Previous", self)
        previous.setFixedSize(60, 20)
        previous.clicked.connect(self.__prevInstance)

        layout.addWidget(findBox, 0, 0)    
        layout.addWidget(next, 0, 1)
        layout.addWidget(previous, 0, 2)

        repBox = QLineEdit(self)
        repBox.setFixedSize(120, 20)
        repBox.setStyleSheet("background-color: #151821; border-style: none;")
        repBox.setPlaceholderText("Replace")

        replace = QPushButton("Replace", self)
        replace.setFixedSize(65, 20)
        replace.clicked.connect(lambda: self.__replace(repBox.text()))

        replaceAll = QPushButton("Replace All", self)
        replaceAll.setFixedSize(65, 20)
        replaceAll.clicked.connect(lambda: self.__replaceAll(repBox.text()))

        layout.addWidget(repBox, 1, 0)
        layout.addWidget(replace, 1, 1)
        layout.addWidget(replaceAll, 1, 2)

        self.setLayout(layout)
        self.exec()



    """
    Reimplementation of QWidget.closeEvent() 
    
    When user presses the exit button, this removes highlights from the editor before closing window
    """
    def closeEvent(self, event):
        self.__unhighlight()
        self.close()



    """
    Gets instances of searchTerm, adds the positions of these instances to self.instances[], and highlights the instances in the editor.

    PARAMETERS:
        searchTerm - The text to search for.
    """
    def __find(self, searchTerm):

        # Exit function if no text was entered
        if searchTerm == "":
            return

        document = self.editor.document()

        self.__unhighlight() # Remove previous highlightings from the document that were created by a previous function call.
        self.instances = [] # Clear instances array of any instances left over from a previous function call.

        text = document.toPlainText()
        position = [] # Represents one instance of search term. Stores the position of initial & final character
        isDiff = False # Flag indicating whether text being examined is discrepant from searchTerm

        for i in range(len(text)):
                
                if text[i] == searchTerm[0]:

                    if len(searchTerm) > 1: # As we have established that the first characters are equal, if the searchTerm only has 1 character then we can conclude the scanning of this particular instance.

                        for offset in range(1, len(searchTerm)): # Range starts at 1 as we have already established that the first characters are equal.
                            if searchTerm[offset] != text[i + offset]:
                                isDiff = True
                                break
                    
                    else:
                        offset = 0 # There is no offset if searchTerm only has 1 character.
                
                    if not isDiff:
                        position = [i, i + offset + 1]  # Note that because QTextCursor positions itself between characters, the cursors final position must be offset + 1.
                        self.instances.append(position)

                    isDiff = False

        if self.instances == []: # In case no instances are found
            msgBox = QMessageBox()
            msgBox.setWindowTitle("BoothiumEdit")
            msgBox.setText(f"Couldn't find '{searchTerm}'")
            msgBox.exec()

        else:

            highlightFmt = QTextCharFormat() 
            highlightFmt.setBackground(QColor("#40d4db"))
            cursor = QTextCursor(document)

            for instance in self.instances:
                cursor.setPosition(instance[0], QTextCursor.MoveMode.MoveAnchor) # Navigate cursor to instance
                cursor.setPosition(instance[1], QTextCursor.MoveMode.KeepAnchor) # Select whole instance by moving position to end of instance but maintaining anchor at beginning.
                cursor.setCharFormat(highlightFmt)
                if instance == self.instances[0]: # Have user's cursor select first instance
                    self.editor.setTextCursor(cursor) 
            


    # Removes highlighting from document. Will be called when find popup is closed, when new text is entered into the find textbox (to remove leftover highlighting from previous call of __find()) or when text is replaced using the replace function.
    def __unhighlight(self):

        document = self.editor.document()
        defaultFmt = QTextCharFormat() 
        defaultFmt.setBackground(QColor("#0E0E10")) # Background will be reset to the background color of the editor 
        cursor = QTextCursor(document)

        cursor.setPosition(len(document.toPlainText()), QTextCursor.MoveMode.KeepAnchor) # Select entire document
        cursor.setCharFormat(defaultFmt)



    # Moves user's cursor to next instance  
    def __nextInstance(self):

        if len(self.instances) <= 1: # There is no next instance if there is only 1 instance, so exit the function in that case. If there are no instances, the user pressed the button without any instances having been found.
            return

        currentCursor = self.editor.textCursor()
        newCursor = QTextCursor(self.editor.document())

        for i in range(len(self.instances)): # Find instance which user's current cursor is at
            if (self.instances)[i][0] == currentCursor.anchor():
                try:
                    newCursor.setPosition((self.instances)[i + 1][0], QTextCursor.MoveMode.MoveAnchor) # Navigate new cursor to next instance from the instance user's cursor is at
                    newCursor.setPosition((self.instances)[i + 1][1], QTextCursor.MoveMode.KeepAnchor) # Select whole instance by moving position to end of instance but maintaining anchor at beginning.
                    break
                    # Note that because the cursor positions itself between characters, the cursors final position must be the final character's position + 1.
                except IndexError: # An IndexError will be raised from the above statement if there is no instance after the current one. In this case we should put the cursor back to the first instance.
                    newCursor.setPosition((self.instances)[0][0], QTextCursor.MoveMode.MoveAnchor) 
                    newCursor.setPosition((self.instances)[0][1], QTextCursor.MoveMode.KeepAnchor) 
                    
        self.editor.setTextCursor(newCursor) 



    # Moves user's cursor to previous instance
    def __prevInstance(self):        

        if len(self.instances) <= 1: # There is no previous instance if there is only 1 instance, so exit the function in that case. If there are no instances, the user pressed the button without any instances having been found.
            return

        currentCursor = self.editor.textCursor()
        newCursor = QTextCursor(self.editor.document())

        for i in range(len(self.instances)): # Find instance which user's current cursor is at
            if self.instances[i][0] == currentCursor.anchor():
                try:
                    newCursor.setPosition(self.instances[i - 1][0], QTextCursor.MoveMode.MoveAnchor) # Navigate new cursor to next instance from the instance user's cursor is at
                    newCursor.setPosition(self.instances[i - 1][1], QTextCursor.MoveMode.KeepAnchor) # Select whole instance by moving position to end of instance but maintaining anchor at beginning.
                    # Note that because the cursor positions itself between characters, the cursors final position must be the final character's position + 1.
                    break
                except IndexError: # An IndexError will be raised from the above statement if there is no instance before the current one. In this case we should put the cursor to the last instance.
                    newCursor.setPosition(self.instances[len(self.instances)][0], QTextCursor.MoveMode.MoveAnchor) 
                    newCursor.setPosition(self.instances[len(self.instances)][1], QTextCursor.MoveMode.KeepAnchor) 
                    
        self.editor.setTextCursor(newCursor) 


    
    """
    Replace instance of found text on which the user's cursor is positioned with new text, then move user's cursor to next instance.

        PARAMETERS:
            - newText - The text to replace the selected instance with.
    """
    def __replace(self, newText):
        
        # Exit function if no text was entered
        if newText == "":
            return

        # This means that the user has pressed the replace button without first finding any instances, so exit the function in this case.
        if self.instances == []: 
            return

        originalAnchor = self.editor.textCursor().anchor()
        originalPos = self.editor.textCursor().position()
        
        # Removing highlighting from instance, as after replacement it will no longer be an instance of the original search term.
        defaultFmt = QTextCharFormat() 
        defaultFmt.setBackground(QColor("#0E0E10")) # Background will be reset to the background color of the editor 
        self.editor.textCursor().setCharFormat(defaultFmt)

        self.editor.textCursor().insertText(newText) # insertText() also deletes current selection before inserting new text

        """
        insertText() moves the user's cursor's anchor and position to the end of the insertion, 
        so we need to reset these to their previous values in order to be able to find the user's cursor's in self.instances[], 
        which in turn is necessary for __nextInstance to work.
        """
        resetCursor = QTextCursor(self.editor.document())
        resetCursor.setPosition(originalAnchor, QTextCursor.MoveMode.MoveAnchor)
        resetCursor.setPosition(originalPos, QTextCursor.MoveMode.KeepAnchor)
        self.editor.setTextCursor(resetCursor)

        """
        ACCOUNTING FOR CHARACTER SHIFT:

        By replacing the original text with new text that is of a different length to the old text, 
        all characters that occur AFTER the replaced text are shifted, thus their positions in the document change
        The positions are shifted by the difference in length between the new and old text.
        Therefore it is necessary to update the positions stored in the self.instances array to account for these changes.

        As lengthDifference is the length of the new text minus that of the old text, it will be negative if the old text is longer than the new text. 
        This is not an issue, as when lengthDifference is added to the positions, if LengthDifference is negative it's absolute value will be subtracted from the positions, 
        shifting the characters leftwards, which is the desired effect if the new text is shorter than the old text.
        """
        originalLength = originalPos - originalAnchor
        if originalLength != len(newText):
            lengthDifference = len(newText) - originalLength
            for i in self.instances:
                if i[0] > self.editor.textCursor().anchor(): # Only shift instances if they occur after instance being replaced
                    i[0] = i[0] + lengthDifference
                    i[1] = i[1] + lengthDifference
    
        self.__nextInstance() # Have user's cursor select the next instance, now that the character shift has been accounted for in self.instances. 
        self.instances.remove([originalAnchor, originalPos]) # Remove currently selected instance from self.instances, as after replacement it no longer represents an instance of the original found text. 
        


    """
    Replace all instances of found text in file with new text.

        PARAMETERS:
            - newText - The text to replace the selected instance with.
    """
    def __replaceAll(self, newText):
        
        # Exit function if no text was entered
        if newText == "":
            return

        if self.instances == []: # This means that the user has pressed the replace button without first finding any instances, so exit the function in this case.
            return

        for i in range(len(self.instances)):
            self.__replace(newText)

        self.__unhighlight() # Remove highlighting from document now that all instances of the original text have been replaced