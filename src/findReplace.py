from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QMessageBox, QStyle


""" 
Top-level function that creates popup and provides a conduit via which to access the other functions in this module.

PARAMETERS:
    text - the text being examined.
    editor - the QTextEdit object for the code editor (So we can highlight found text).
"""
def find(text, editor):

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

    instances = [] # 3D array - Stores cartesian coordinates of all found text instances (to be modified by __getInstances())
    findBox.returnPressed.connect(lambda: __getInstances(findBox.text(), text, instances))
 
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
    searchTerm - The text to search FOR.
    inspectText - The text to search.
    instances - The instances array
    editor - the QTextEdit object for the code editor (So we can highlight text).

"""
def __getInstances(searchTerm, inspectText, instances, editor):

    instances = [] # clear instances array in case instances from function's last execution are left in.
    
    position = [] # 2D array - Stores the position of 1 instance (cartesian coordinate of initial character & cartesian coordinate of final)
    isDiff = False # Flag indicating whether text being examined is discrepant from searchTerm

    inspectGrid = inspectText.split("\n") # Split text into 2D grid, ending at each newline. This allows us to get the coordinates of each character. 

    for y in range(len(inspectGrid)):
        for x in range(len(inspectGrid[y])):

            if inspectGrid[y][x] == searchTerm[0]:

                if len(searchTerm) > 1: # As we have established that the first characters are equal, if the searchTerm only has 1 character then we can conclude the scanning of this particular instance.

                    for xOffset in range(1, len(searchTerm)): # Range starts at 1 as we have already established that the first characters are equal.
                        try:
                            if searchTerm[xOffset] != inspectGrid[y][x + xOffset]:
                                isDiff = True
                                break
                        except IndexError: # This occurs when (x + xOffset) is "off of the end" of the line being examined i.e x + xOffset > len(inspectGrid[y]). In which case the searchTerm is not present here, and we move on.
                            isDiff = True
                            break
                
                else:
                    xOffset = 0 # There is no xOffset if searchTerm only has 1 character.
            
                if not isDiff:
                    position = [[x, y],[x + xOffset, y]]
                    instances.append(position)

                isDiff = False

    if instances == []:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("BoothiumEdit")
        msgBox.setText(f"Couldn't find '{searchTerm}'")
        msgBox.exec()
    else:
        editor