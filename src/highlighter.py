from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor

import re
import json
import os
import sys


"""
Class representing the syntax highlighter, containing appropriate highlighting methods

CONSTRUCTOR PARAMETERS:
    editor - The QPlainTextEdit representing the code editor textbox.

ATTRIBUTES:
	editor - The QPlainTextEdit representing the code editor textbox.
	colorScheme - Dictionary mapping a type of lexical token to the hex color value that tokens of that type are to be highlighted.
	rules - Dictionary mapping a token type to a regular expression that recognizes text of that token type.
"""
class Highlighter():


	def __init__(self, editor):

		self.editor = editor

		if self.editor.language == "html":


			self.colorScheme = {
				"comment": "#a69a5a",
				"tag_name": "#e69c3c",
				"attribute_name": "#5693a6",
				"dbl_quote_attribute_data": "#609e7b",
				"single_quote_attribute_data": "#609e7b",
				"delimiter": "#ffffff",
				"whitespace": "#ffffff",
				"text": "#ffffff",
				"unknown": "#ffffff"
			}

			self.rules = {
				"whitespace": r"^\s",

				"delimiter": r"(</|<|>|=)",

				"tag_name": r"(?<=<)^[_A-Za-z0-9]*",

				"text": r"(?<=>)^.*",

				"attribute_name": r"^[_A-Za-z][_A-Za-z0-9]*(?==)",
				"single_quote_attribute_data": r"^('[^'\n]*')",
				"dbl_quote_attribute_data": r"^(\"[^\"\n]*\")",

				"unknown": r"^."
			}


		else:

			self.colorScheme = {			
				"comment": "#a69a5a",
				"number": "#e69c3c",
				"dbl_quote_string": "#609e7b",
				"single_quote_string": "#609e7b",
				"keyword": "#8751a6",
				"operator": "#a34040",
				"dbl_char_operator": "#a34040", 
				"delimiter": "#ffffff",
				"whitespace": "#ffffff",
				"identifier": "#ffffff",
				"function": "#5693a6", 
				"preprocessor_directive": "#4d68b3",
				"unknown": "#ffffff"
			}

			# Maps a supported language to an array of it's reserved keywords.
			languagesKeywords = {

				"python": ["False", "await",	"else", "import", "pass",
								"None", "break", "except", "in", "raise",
								"True", "class", "finally", "is", "return",
								"and", "continue", "for", "lambda",
								"as", "def", "from", "nonlocal", "try",
								"assert", "del", "global", "not", "while",
								"async", "elif", "if"	, "or", "with",
								"yield"],

				"c": ["auto", "break", "case", "char",
								"const", "continue", "default",	"do",
								"double", "else", "enum", "extern",
								"float", "for",	"goto",	"if",
								"int", "long", "register",	"return",
								"short", "signed",	"sizeof", "static",
								"struct", "switch",	"typedef", "union",
								"unsigned", "void", "volatile", "while"],

				"c++": ["asm", "double", "new", "switch",
								"auto", "else", "operator", "template",
								"break", "enum", "private", "this",
								"case", "extern", "protected", "throw",
								"catch", "float", "public", "try",
								"char", "for", "register", "typedef",
								"class", "friend", "return", "union",
								"const", "goto", "short", "unsigned",
								"continue", "if", "signed", "virtual",
								"default", "inline", "sizeof", "void",
								"delete", "int", "static", "volatile ",
								"do", "long", "struct", "while"],

				"javascript": ["abstract", "arguments", "await", "boolean",
								"break", "byte", "case", "catch",
								"char", "class", "const", "continue",
								"debugger", "default", "delete", "do",
								"double", "else", "enum", "eval",
								"export", "extends", "false", "final",
								"finally", "float", "for", "function",
								"goto", "if", "implements", "import",
								"in", "instanceof", "int", "interface",
								"let", "long", "native", "new",
								"null", "package", "private", "protected",
								"public", "return", "short", "static",
								"super", "switch", "synchronized",
								"throw", "throws", "transient", "true",
								"try", "typeof", "var", "void",
								"volatile", "while", "with", "yield"],

				"java": ["abstract", "continue", "for", "new", "switch",
								"assert", "default", "goto", "package", "synchronized",
								"boolean", "do", "if", "private",
								"break", "double", "implements", "protected", "throw",
								"byte", "else", "import", "public",	"throws",
								"case", "enum", "instanceof", "return",	"transient",
								"catch", "extends", "int", "short",	"try",
								"char", "final", "interface", "static",	"void",
								"class", "finally", "long",	"strictfp",	"volatile",
								"const", "float", "native", "super", "while"],

				"go": ["const", "chan", "break", 
								"defer", "var", "interface", 
								"case", "go", "func", "map", 
								"continue", "type", "struct", "default", 
								"import", "else", "package", 
								"fallthrough", "for", "goto", "if", 
								"range", "return", "select", "switch"]
			}


			# Accounts for comments in python being denoted by '#' rather than '//'.
			if self.editor.language == "python":
				commentRegex = "^(#.*)"
			else:
				commentRegex = "^(//.*)"

		    # Generate regular expression for keywords.
		    # The resulting regex should look something like this: "^(KEYWORD|KEYWORD|KEYWORD|KEYWORD)$", where "KEYWORD" is replaced with an actual keyword.
			keywordRegex = "^(" # Opening part of expression
			keywords = languagesKeywords[self.editor.language]
			for i in range(len(keywords)):

				if i == len(keywords) - 1: # The "or" regex character (i.e "|") should not follow the last keyword in the regex string.
					keywordRegex = keywordRegex + keywords[i] # Append keyword to regex string.
				else:
					keywordRegex = keywordRegex + keywords[i] + "|"

			keywordRegex = keywordRegex + ")(?=(\s|:))" # Append closing part of expression


			# Maps a type of token to a regular expression that recognizes text of that token type.
			# For purposes of readability, a version of the regex string that does not include escape backslashes ('\') is commented next to the string.
			#
			# Note that the ordering of each rule within the dictionary is important, as for a lot of token types there is an overlap between 2 types(e.g all keywords are identifiers, and a function is an identifier followed by a delimiter).
			# As the dictionary is iterated over rom start to finish when looking for matches, it is important for more particular token types (e.g function, keyword) to precede more general ones (e.g identifier) that might also capture the tokens that are of the more specific types. 
			self.rules = {

	            "whitespace": r'^\s',

	            "comment": commentRegex,

	            "delimiter": r"^[\(\)\[\]\{\}@,:`;.]", # W/O escape backslashes: ^[()[]{}@,:`;.]

	            "dbl_char_operator": r"^((==)|(!=)|(\<=)|(\>=)|(<>)|(\<\<)|(\>\>)|(//)|(\*\*)|(\+=)|(\-=)|(\*=)|(%=)|(/=)|(\|=)|(^=))",  # W/O escape backslashes: ^((==)|(!=)|(<=)|(>=)|(<>)|(<<)|(>>)|(//)|(**)|(+=)|(-=)|(*=)|(%=)|(/=)|(|=)|(^=))
	            "operator": r"^[\+\-\*/%\|^&~<>!=\?]", # W/O escape backslashes: ^[+-*/%|^&~<>!=?]

	            "keyword": keywordRegex,
	            "function": r"^[_A-Za-z][_A-Za-z0-9]*(?=\()", # W/O escape backslashes: ^[_A-Za-z][_A-Za-z0-9]*(?=(
	            "identifier": "^[_A-Za-z][_A-Za-z0-9]*", 

	            "dbl_quote_string": r"^(\"[^\"\n]*\")", # W/O escape backslashes: ^("[^"\n]*")
				"single_quote_string": r"^('[^'\n]*')", 

	            "number": r"^\d+",
	            
		    	}

		    # Add C/C++ preprocessor directives
			if self.editor.language == "c" or self.editor.language == "c++":
				self.rules["preprocessor_directive"] = r"^#(include|define|undef|if|ifdef|ifndef|error)(?=\s)" 

			# Finally, add unknown character regex at end of dictionary (Must be added at the end, as the regex string for it captures all characters).
			self.rules["unknown"] = r"^."


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
					print(tokenType)
					matchLength = match.span()[1] - match.span()[0]

					fmt = QTextCharFormat()
					color = self.colorScheme[tokenType]
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