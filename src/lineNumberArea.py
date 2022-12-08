from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QFontMetrics, QColor
from PyQt6.QtCore import Qt



"""
Represents the section in which the line numbers of code in the editor are positioned. Placed to the left of the editor textbox.

CONSTRUCTOR PARAMETERS:
    editor - The QPlainTextEdit representing the code editor textbox.
"""
class LineNumberArea(QWidget):


    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor


    """
    Returns the width of the LineNumberArea.
    """
    def getWidth(self):
        linesNo = self.editor.blockCount()
        digitsNo = len(str(linesNo))  
        charWidth = QFontMetrics(self.font()).maxWidth() # Width of 1 individual character in the editor's font.
        return ((digitsNo + 1) * charWidth) 


    """
    This is called by event from the editor class (via the blockCountChanged() signal), whenever new lines are created or removed in the editor.
    Sets a margin around the editor which the lineNumberArea will occupy.
    """
    def updateWidth(self):
        self.editor.setViewportMargins(self.getWidth(), 0, 0, 0)


    """
    This is called by event from the editor class (via the updateRequest() signal), when a QRect within the editor needs to be updated (Mostly happens when the editor is scrolled).
    If the editor was scrolled, scrolls the LineNumberArea to the same level that the editor was scrolled to.

    PARAMETERS:
        rect - The QRect that needs to be updated (originally a parameter of the updateRequest() signal called in the editor class).
        dy - Number of pixels scrolled by (originally a parameter of the updateRequest() signal called in the editor class).
    """
    def updateRect(self, rect, dy):

        if dy != 0: # If editor was scrolled
            self.scroll(0, dy)

        else: # If no scrolling has happened but a QRect needs updating
            self.update(0, rect.y(), self.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            self.updateWidth()


    """
    Reimplemenation of Qwidget.paintEvent. Allows us to paint the LineNumberArea.
    This is called automatically on initialization, and when any change to the editor occurs.
    """
    def paintEvent(self, event):

        # Paint widget brackground
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(20, 32, 51))

        line = self.editor.firstVisibleBlock()
        lineNo = line.blockNumber()

        height = self.fontMetrics().height() # Height of 1 individual character in the editor's font.

        top = round(self.editor.blockBoundingGeometry(line).translated(self.editor.contentOffset()).top())
        bottom = top + round(self.editor.blockBoundingRect(line).height())

         # Iterate over all lines
        while line.isValid() and (top <= event.rect().bottom()):

            if line.isVisible() and (bottom >= event.rect().top()):
                # Write line number text
                number = "~ " + str(lineNo + 1) + " "
                painter.setPen(QColor(102, 102, 102))
                painter.drawText(0, top, self.width(), height, Qt.AlignmentFlag.AlignRight, number)

            line = line.next()
            lineNo += 1    

            top = bottom
            bottom = top + round(self.editor.blockBoundingRect(line).height())