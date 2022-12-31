from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor

import re
from enum import Enum
import json
import os
import sys


"""
Contains all the possible types of token.
"""
class TokenType(Enum):

	COMMENT = 1
	NUMBER = 2
	STRING = 3

	OPERATOR = 4
	DOUBLE_CHAR_OPERATOR = 5

	DELIM = 6

	WHITESPACE = 7
	IDENTIFIER = 8

	UNKNOWN = 9


"""
Class representing the syntax highlighter itself, containing appropriate highlighting methods

CONSTRUCTOR PARAMETERS:
    editor - The QPlainTextEdit representing the code editor textbox.
"""
class Highlighter():


	def __init__(self, editor):

		self.editor = editor

		# Loading highlighting color scheme from settings file into a dictionary
		sFilePath = os.path.join(sys.path[0], "BEditSettings.json")
		with open(sFilePath, 'r+') as file:																																		
			self.colorScheme = (json.load(file))["colorScheme"]

		self.rules = {

	            TokenType.WHITESPACE: '^\s',

	            TokenType.COMMENT: "^(#|//).+",

	            TokenType.DELIM: r"^[\(\)\[\]\{\}@,:`;.]", # W/O escape backslashes: ^[()[]{}@,:`;.]

	            TokenType.DOUBLE_CHAR_OPERATOR: r"^((==)|(!=)|(\<=)|(\>=)|(<>)|(\<\<)|(\>\>)|(//)|(\*\*)|(\+=)|(\-=)|(\*=)|(%=)|(/=)|(\|=)|(^=))",  # W/O escape backslashes: ^((==)|(!=)|(<=)|(>=)|(<>)|(<<)|(>>)|(//)|(**)|(+=)|(-=)|(*=)|(%=)|(/=)|(|=)|(^=))
	            TokenType.OPERATOR: r"^[\+\-\*/%\|^&~<>!=\?]", # W/O escape backslashes: ^[+-*/%|^&~<>!=?]

	            TokenType.IDENTIFIER: "^[_A-Za-z][-Za-z0-9]*", 

	            TokenType.STRING: r"^(\"[^\"\n]*\")", # W/O escape backslashes: ^("[^"\n]*")
	            TokenType.NUMBER: "^\d+",
	            
	            TokenType.UNKNOWN: "^.",
	    	}


	"""
	Applies necessary highlighting to the line on which the user's cursor is located.
	This is to be executed in the editor class on every key press.
	"""
	def highlightLine(self):

		script = self.editor.toPlainText()

		# Getting whole line on which User's cursor is located
		line = ""

		char = self.editor.textCursor().position() - 1 # 1 is substracted from the position to get the index of the character preceding the cursor
		charsBeforeLine = 0 # Number of characters in the file before the first character of the line.
		# Iterate backwards until newline character (Loop also terminates if beginning of file is reached).
		while char >= 0:
			if script[char] == "\n":
				charsBeforeLine = char + 1
				break
			line = line + script[char] # Append character to line
			char -= 1

		line = line[::-1] # As we iterated backwards, the line string is back-to-front. This inverts it so that so the characters are in the correct order.

		char = self.editor.textCursor().position() # This gives the index of the character occuring just after the cursor.
		# Iterate forwards until newline character (Loop also terminates if end of file is reached).
		while char < len(script):
			if script[char] == "\n":
				break
			line = line + script[char]  # Append character to line
			char += 1

		cursor = QTextCursor(self.editor.document())

		i = 0
		while i < len(line):

			for tokenType in self.rules:

				match = re.match(self.rules[tokenType], line[i:]) # Only the text following the current iteration position is searched, so that we disregard already examined text.

				if match:

					matchLength = match.span()[1] - match.span()[0]

					fmt = QTextCharFormat()
					color = self.colorScheme[str(tokenType)]
					fmt.setForeground(QColor(color))

					cursor.setPosition(charsBeforeLine + i, QTextCursor.MoveMode.MoveAnchor) # Navigate cursor to match.
					cursor.setPosition(charsBeforeLine + i + matchLength, QTextCursor.MoveMode.KeepAnchor) # Select whole match by moving position to end of match but maintaining anchor at beginning.

					cursor.setCharFormat(fmt)

					i += matchLength
					
					break

					
	"""
	Applies necessary highlighting to the entire file.
	This is to be executed on the program's startup.
	"""
	def highlightAll(self):

		script = self.editor.toPlainText()

		cursor = QTextCursor(self.editor.document())
		
		i = 0
		while i < len(script):

			for tokenType in self.rules:

				match = re.match(self.rules[tokenType], script[i:]) # Only the text following the current iteration position is searched, so that we disregard already examined text.

				if match:

					matchLength = match.span()[1] - match.span()[0]

					fmt = QTextCharFormat()
					color = self.colorScheme[str(tokenType)]
					fmt.setForeground(QColor(color))

					cursor.setPosition(i, QTextCursor.MoveMode.MoveAnchor) # Navigate cursor to match.
					cursor.setPosition(i + matchLength, QTextCursor.MoveMode.KeepAnchor) # Select whole match by moving position to end of match but maintaining anchor at beginning.

					cursor.setCharFormat(fmt)

					i += matchLength
					
					break