from PyQt6.QtWidgets import QPlainTextEdit, QPlainTextDocumentLayout
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor
from PyQt6.QtCore import Qt, QRect

import json
import os
import sys
import re

from lineNumberArea import LineNumberArea
from highlighter import Highlighter


"""
Represents the code editor textbox.

CONSTRUCTOR PARAMETERS:
    fileText - The text of the file to open.
    language - The string for the name of the programming language the user is editing.

ATTRIBUTES:
    language - The string for the name of the programming language the user is editing.
    lineNumberArea - The LineNumberArea representing the line number space on the left margin of the editor textbox.
    settings - Dictionary containing the settings loaded from BEditSettings.json.
    highlighter - The Highlighter object representing the editor's syntax highlighter. (If syntax highlighting is not to be applied to the file, then this attribute will equal None).
"""
class Editor(QPlainTextEdit):


    def __init__(self, fileText, language):

        super().__init__()

        self.setStyleSheet("""color: white; 
                                background-color: #22283a; 
                                border-style: none; 
                                font-family: Consolas, Menlo, monospace; 
                                font-size: 13pt;""")

        document = QTextDocument(fileText)
        plainTextLayout = QPlainTextDocumentLayout(document) # Document being edited in QPlainTextEdit must have a QPlainTextDocumentLayout.
        document.setDocumentLayout(plainTextLayout)
        self.setDocument(document)

        self.language = language

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.lineNumberArea.updateWidth) # Line numbers need to be revised when new lines are added or removed
        self.updateRequest.connect(self.lineNumberArea.updateRect) # When editor is scrolled, the line number section needs to be scrolled too.
        self.lineNumberArea.updateWidth()

        # Loading settings file into a dictionary
        sFilePath = os.path.join(sys.path[0], "BEditSettings.json")
        with open(sFilePath, 'r+') as file:
            self.settings = json.load(file)

        # Only highlight syntax for supported languages and if appropriate setting is enabled.
        if self.language == "unknown" or not self.settings["syntaxHighlighting"]:
            self.highlighter = None

        else:
            self.highlighter = Highlighter(self)
            self.highlighter.highlightAll()


    """
    Reimplemenation of Qwidget.resizeEvent. 
    When the editor is resized, this resizes the LineNumberArea proportionally.
    """
    def resizeEvent(self, event):

        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberArea.getWidth(), cr.height()))


    """
    Reimplementation of QWidget.keyPressEvent() signal, to perform syntax highlighting and
    to check if automatic indentation and/or automatic bracket & quotation mark closure is required after a key press.
    """
    def keyPressEvent(self, event):

        originalCursorPos = self.textCursor().position() # Cursor's position before "super().keyPressEvent(event)" is called

        super().keyPressEvent(event)  # Do as normal first

        # Automatic indentation
        if (event.key() ==  Qt.Key.Key_Return) and self.settings["autoIndent"]:
            # Create cursor that represents the user's cursor before "return" was pressed
            originalCursor = QTextCursor(self.document())
            originalCursor.setPosition(originalCursorPos) 
            self.__autoIndent(originalCursor)

        # Bracket autoclosure
        if self.settings["autoCloseBrckt"]:    
            
            if event.key() ==  Qt.Key.Key_BracketLeft: # Square bracket/Bracket
                self.textCursor().insertText(']')
                self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter) # Move cursor to previous position so that it is between brackets
            elif event.key() ==  Qt.Key.Key_ParenLeft: # Round bracket/Parentheses
                self.textCursor().insertText(')')
                self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)
            elif event.key() ==  Qt.Key.Key_BraceLeft: # Curly bracket/Brace
                self.textCursor().insertText('}')
                self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)

        # Quotemark autoclosure
        if self.settings["autoCloseQt"]:

            if event.key() ==  Qt.Key.Key_Apostrophe:
                self.textCursor().insertText('\'')
                self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)
            elif event.key() ==  Qt.Key.Key_QuoteDbl:
                self.textCursor().insertText('"')
                self.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)

        # Syntax highlighting
        if self.highlighter != None:
            self.highlighter.highlightLine()


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
        # so here we obtain the previous line's text and deduce it's number of indents.
        prevLine = "" 
        char = editorTxt[cursorBeforeReturn.position() - 1] # The character occuring immediately before the cursor in the document
        
        charCount = 1 # charCount begins as 1, because char is initially the character 1 position before the cursor's position
        while char != "\n": # Get all characters on the line by iterating backwards from cursor until a newline character is reached i.e When the end of the line before is reached
 
            prevLine = prevLine + char # Appends character to line
            charCount += 1
            char = editorTxt[cursorBeforeReturn.position() - charCount] # Move char to next character back 


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
        charCount = 1  
        while char.isspace(): # Iterate backwards through any whitespace until a non-whitespace character is encountered           

            if char == "\n": # Exit loop if newline character is encountered before any non-whitespace characters i.e When the end of the line before is reached.
                break
            
            charCount += 1
            char = editorTxt[cursorBeforeReturn.position() - charCount]
            
            
        if (char in brackets) or (char == ":"): # Indent if character is colon or a bracket
            indentsNeeded += 1

        for indent in range(indentsNeeded):
            self.textCursor().insertText('\t')