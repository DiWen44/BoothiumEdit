from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtCore import Qt

import json
import os
import sys



"""
Represents the code editor textbox.

CONSTRUCTOR PARAMETERS:
    fileText - The text of the file to open.
"""
class Editor(QTextEdit):


    def __init__(self, fileText):

        super().__init__()

        self.setStyleSheet("""color: white; 
                                background-color: #0E0E10; 
                                border-style: none; 
                                font-family: Consolas, Menlo,  monospace; 
                                font-size: 13pt;""")
        document = QTextDocument(fileText)
        self.setDocument(document)


    """
    Reimplementation of QWidget.keyPressEvent() signal, 
    to check if automatic indentation and/or automatic bracket & quotation mark closure is required after a key press.
    """
    def keyPressEvent(self, event):
        
        # Loading settings file into dictionary
        sFilePath = os.path.join(sys.path[0], "BEditSettings.json")
        with open(sFilePath, 'r+') as file:
            settings = json.load(file)

        originalCursorPos = self.textCursor().position() # Cursor's position before "super().keyPressEvent(event)" is called

        super().keyPressEvent(event)  # Do as normal first

        # Automatic indentation
        if (event.key() ==  Qt.Key.Key_Return) and settings["autoIndent"]:
            # Create cursor that represents the user's cursor before "return" was pressed
            originalCursor = QTextCursor(self.document())
            originalCursor.setPosition(originalCursorPos) 
            self.__autoIndent(originalCursor)

        # Bracket autoclosure
        if settings["autoCloseBrckt"]:    
            
            if event.key() ==  Qt.Key.Key_BracketLeft: # Square bracket/Bracket
                self.textCursor().insertText(']')
            elif event.key() ==  Qt.Key.Key_ParenLeft: # Round bracket/Parentheses
                self.textCursor().insertText(')')
            elif event.key() ==  Qt.Key.Key_BraceLeft: # Curly bracket/Brace
                self.textCursor().insertText('}')

            self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter) # Move cursor to previous position so that it is between brackets

        # Quotemark autoclosure
        if settings["autoCloseQt"]:

            if event.key() ==  Qt.Key.Key_Apostrophe:
                self.textCursor().insertText('\'')
            elif event.key() ==  Qt.Key.Key_QuoteDbl:
                self.textCursor().insertText('"')

            self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)


    """
    Checks if additional indentation is required at the beginning of a new line, and indents however many times is necessary:
        - Adds necessary indentation to beginning of new line to match previous line's level of indentation.
        - Indents one more time if previous line ends with a colon or an opening bracket ('{'.  '(' or '[' ).

    PARAMETERS:
        cursorBeforeReturn - QTextCursor representing the editor's cursor BEFORE the "return" key was pressed.
    """
    def __autoIndent(self, cursorBeforeReturn):

        brackets = ['[', '(', '{']  

        indentsNeeded = 0 # Number of indents that are needed

        editorTxt = self.toPlainText()

        # There may be previous indents at the beginning of the line the cursor was on before "return" was pressed. 
        # The new line must be indented to the same level as the previous (and one more if the previous line ended with a colon or bracket),
        # so here we get the number of indents of the previous line.
        prevLine = "" 
        char = editorTxt[cursorBeforeReturn.position() - 1] # The character occuring immediately before the cursor in the document
        charCount = 2 # charCount begins as 2, because char is initially the character 1 position before the cursor's position

        while not (char == "\n"): # Get all characters on the line by iterating backwards from cursor until a newline character is reached

            prevLine = prevLine + char # Appends character to line
            char = editorTxt[cursorBeforeReturn.position() - charCount]
            charCount += 1

        prevLine = prevLine[::-1] # Since iteration started at the end of the line, the line string is backwards. This inverts it so the characters are in the correct order.

        for i in prevLine:  
            if i == "\t":
                indentsNeeded += 1
            else: # Any tabs on the line occuring after the first non-tab character are irrelevant, so we can end the loop.
                break
        
        # The line may end with a colon or bracket, but there is a chance that there is whitespace after the colon/bracket and before the cursor. 
        # If so, it's still necessary to indent, so here we traverse any whitespace before the cursor, and determine if it's necessary to indent based on the character at the other end of the whitespace.
        # This will still work as intended if there is no whitespace before the cursor, as the loop just won't be executed.
        char = editorTxt[cursorBeforeReturn.position() - 1]
        charCount = 2  
        while char.isspace(): # Iterate backwards through any whitespace until a non-whitespace character is encountered           

            if char == "\n": # Exit loop if newline character is encountered before any non-whitespace characters. We don't need to add an indent in this siuation
                break

            char = editorTxt[cursorBeforeReturn.position() - charCount]
            charCount += 1
            
        if (char in brackets) or (char == ":"): # Indent if character is colon or a bracket
            indentsNeeded += 1

        for indent in range(indentsNeeded):
            self.textCursor().insertText('\t')


