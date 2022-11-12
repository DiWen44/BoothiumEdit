from PyQt6.QtWidgets import QFileDialog
import os


def save(filename, newtext):
	file = open(filename, 'w') # File's contents are automatically erased when opened in write mode
	file.write(newtext)
	file.close()


def saveAs(text):
	
	path = QFileDialog.getSaveFileName(caption="Save As")[0]

	# Case for user cancelling or exiting filesystem
	if path == "":
		return

	try:
		file = open(path, 'w') # File's contents are automatically erased when opened in write mode
		file.write(text)
	except FileNotFoundError: # Make file if it doesn't exist
		os.mknod(path)
		file = open(path, 'w')
		file.write(text)

	file.close()


	
	
	
	

