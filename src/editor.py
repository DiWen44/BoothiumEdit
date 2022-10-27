from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextDocument, QFontMetrics, QTextCursor
from PyQt6.QtCore import Qt


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
                                font-family: Consolas, "Courier New",  monospace; 
                                font-size: 13pt;""")
        document = QTextDocument(fileText)
        self.setDocument(document)


    """Reimplementation of QWidget.keyPressEvent(), to check if automatic indentation and/or automatic bracket & quotation mark closure is required after the key press"""
    def keyPressEvent(self, event):
        
        cursor = self.textCursor()

        match event.key():

            # Automatic indentation
            case Qt.Key.Key_Return:
                originalCursor = cursor
                originalCursorPos = originalCursor.position() # Cursor's position before "return" is pressed
                super().keyPressEvent(event) 
                originalCursor.setPosition(originalCursorPos) # Cursor variable changes to match editor's cursor, so reset it's position to previous value in order to pass it to __autoIndent() as the cursor before "return" was pressed
                self.__autoIndent(originalCursor)
                return
        
            # Bracket autoclosure
            case Qt.Key.Key_BracketLeft: # Square bracket/Bracket

            case Qt.Key.Key_ParenLeft: # Round bracket/Parentheses
            case Qt.Key.Key_BraceLeft: # Curly bracket/Brace
        
            # Quotemark autoclosure
            case Qt.Key.Key_Apostrophe:
                
            case Qt.Key.Key_QuoteLeft:



        super().keyPressEvent(event) # Do as normal 

    

    """
    Checks if additional indentation is required at the beginning of a new line, and indents however many times is necessary:
        - Adds necessary indentation to beginning of new line to match previous line's level of indentation.
        - Indents one more time if previous line ends with a colon or an opening bracket ('{'.  '(' or '[' ).

    PARAMETERS:
        cursorBeforeReturn - QTextCursor representing the editor's cursor BEFORE the "return" key was pressed.
    """
    def __autoIndent(self, cursorBeforeReturn):

        brackets = ['[', '(', '{']  

        indentNo = 0 # Number of indents that are needed

        """
        There may be previous indents at the beginning of the line the cursor was on before "return" was pressed. 
        The new line must be indented to the same level as the previous, and one more if the previous line ended with a colon or bracket.
        """
        line = ""
        char = self.toPlainText()[cursorBeforeReturn.position() - 1] # The character occuring immediately before the cursor in the document
        charCount = 2 # charCount begins as 2, because char is initially the character 1 position before the cursor's position
        while not (char == "\n"): # Get all characters on the line by iterating backwards from cursor until a newline character is reached
            line = line + char # Appends character to line
            char = self.toPlainText()[cursorBeforeReturn.position() - charCount]
            charCount += 1

        line = line[::-1] # Since iteration started at the end of the line, the line string is backwards. This inverts it so the characters are in the correct order.

        for i in line:
            if i == "\t":
                indentNo += 1
            else: # Any tabs on the line occuring after the first non-tab character are irrelevant, so we can end the loop.
                break
        
        """
        The line may end with a colon or bracket, but there is a chance that there is whitespace after the colon/bracket and before the cursor. 
        If so, it's still necessary to indent, so here we traverse any whitespace before the cursor to examine the character before it, and determine if it's necessary to indent.

        This will still work as intended if there is no whitespace before the cursor, as the while loop just won't be executed.
        """
        j = self.toPlainText()[cursorBeforeReturn.position() - 1]
        jCount = 2  
        while j.isspace(): # Iterate backwards through any whitespace until a non-whitespace character is encountered             
            j = self.toPlainText()[cursorBeforeReturn.position() - jCount]
            jCount += 1
        if (j in brackets) or (j == ":"): # Indent if character is colon or a bracket
            indentNo += 1

        for indent in range(indentNo):
            self.textCursor().insertText('\t') # Insert tab character

