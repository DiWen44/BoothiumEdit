from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor


""" 
Top-level function that creates popup and provides a conduit via which the other functions in this module can be accessed.

PARAMETERS:
    Document - the QTextDocument currently active in the code editor.
"""
def find(document):

    popup = QDialog()
    popup.setFixedSize(300, 100)
    popup.setWindowTitle("Find")
    popup.setStyleSheet("""color: white; 
						background-color: #484D5D;
                        font: Source Sans Pro;""")

    layout = QGridLayout()


    findBox = QLineEdit(popup)
    findBox.setFixedSize(120, 20)
    findBox.setStyleSheet("background-color: #151821; border-style: none;")
    findBox.setPlaceholderText("Find")

    findBox.returnPressed.connect(lambda: __getInstances(findBox.text(), document))
 
    nextInstance = QPushButton("Next", popup)
    nextInstance.setFixedSize(60, 20)
    prevInstance = QPushButton("Previous", popup)
    prevInstance.setFixedSize(60, 20)

    layout.addWidget(findBox, 0, 0)    
    layout.addWidget(nextInstance, 0, 1)
    layout.addWidget(prevInstance, 0, 2)


    repBox = QLineEdit(popup)
    repBox.setFixedSize(120, 20)
    repBox.setStyleSheet("background-color: #151821; border-style: none;")
    repBox.setPlaceholderText("Replace")

    replace = QPushButton("Replace", popup)
    replace.setFixedSize(65, 20)
    replaceAll = QPushButton("Replace All", popup)
    replaceAll.setFixedSize(65, 20)

    layout.addWidget(repBox, 1, 0)
    layout.addWidget(replace, 1, 1)
    layout.addWidget(replaceAll, 1, 2)


    popup.setLayout(layout)
    popup.exec()


"""
Gets instances of found text and highlights results

PARAMETERS:
    searchTerm - The text to search for.
    document - the QTextDocument for the currently active document in the editor (So we can highlight text).
"""
def __getInstances(searchTerm, document):

    # Exit function if no text was entered
    if searchTerm == "":
        return

    __unhighlight(document) # Remove previous highlights from the document


    inspectText = document.toPlainText()
    position = [] # Represents one instance of search term. Stores the position of initial & final character
    instances = [] # 2D array - Stores positions of the initial & final characters of all found text instances.
    isDiff = False # Flag indicating whether text being examined is discrepant from searchTerm

    for i in range(len(inspectText)):
            
            if inspectText[i] == searchTerm[0]:

                if len(searchTerm) > 1: # As we have established that the first characters are equal, if the searchTerm only has 1 character then we can conclude the scanning of this particular instance.

                    for offset in range(1, len(searchTerm)): # Range starts at 1 as we have already established that the first characters are equal.
                        if searchTerm[offset] != inspectText[i + offset]:
                            isDiff = True
                            break
                
                else:
                    offset = 0 # There is no offset if searchTerm only has 1 character.
            
                if not isDiff:
                    position = [i, i + offset]
                    instances.append(position)

                isDiff = False

    if instances == []: # In case no instances are found
        msgBox = QMessageBox()
        msgBox.setWindowTitle("BoothiumEdit")
        msgBox.setText(f"Couldn't find '{searchTerm}'")
        msgBox.exec()

    else:

        highlightFmt = QTextCharFormat() 
        highlightFmt.setBackground(QColor("blue"))
        
        cursor = QTextCursor(document)
        for instance in instances:
            cursor.setPosition(instance[0], QTextCursor.MoveMode.MoveAnchor) # Navigate cursor to instance
            cursor.setPosition(instance[1] + 1, QTextCursor.MoveMode.KeepAnchor) # Select whole instance by moving position to end of instance but maintaining anchor at beginning.
            # Note that because the cursor positions itself between characters, the cursors final position must be offset + 1.
            cursor.setCharFormat(highlightFmt)


"""
Removes highlighting from document. Will be called when find popup is closed, when new text is entered into the find textbox or when text is replaced using the replace function.

PARAMETERS:
    instances - the instances array.
    document - the QTextDocument for the currently active document in the editor.
"""
def __unhighlight(document):

    defaultFmt = QTextCharFormat() 
    defaultFmt.setBackground(QColor("#484D5D")) # Background will be reset to the background color of the editor 
    cursor = QTextCursor(document)

    cursor.setPosition(len(document.toPlainText()), QTextCursor.MoveMode.KeepAnchor) # Select entire document
    cursor.setCharFormat(defaultFmt)


            
        