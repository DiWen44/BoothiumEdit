from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout

def find():

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
 
    nextInstance = QPushButton("Next", popup)
    nextInstance.setFixedSize(50, 20)
    prevInstance = QPushButton("Previous", popup)
    prevInstance.setFixedSize(50, 20)

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