from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton


# Represents the settings popup that shows when the user clicks the "settings" option in the main window's menubar
class SettingsPopup(QDialog):

    def __init__(self):

        super().__init__()
        
        self.setFixedSize(200, 300)
        self.setWindowTitle("Settings")
        self.setStyleSheet("""color: white; 
                                background-color: #0E0E10;
                                font-family: Garet; """)

        layout = QVBoxLayout()

        autoCloseBrckt = Setting("Auto Close Brackets")
        layout.addLayout(autoCloseBrckt)

        AutoCloseQt = Setting("Auto Close Quotes")
        layout.addLayout(AutoCloseQt)

        AutoIndent = Setting("Auto Indent")
        layout.addLayout(AutoIndent)

        syntaxHighlight = Setting("Syntax Highlighting")
        layout.addLayout(syntaxHighlight)

        autosave = Setting("Autosave")
        layout.addLayout(autosave)

        self.setLayout(layout)

        save = QPushButton("Save", self)
        save.setGeometry(46, 270, 40, 20)
        save.setStyleSheet("background-color: #404040; border-style: none;")

        openJSON = QPushButton("Open settings.json", self)
        openJSON.setGeometry(88, 270, 110, 20)
        openJSON.setStyleSheet("background-color: #404040; border-style: none;")

        self.exec()


# Represents 1 individual on/off setting, and is comprised of that setting's name and the dropdown menu for it. In the form of a QHBoxLayout that is to be added to the popup's layout.
class Setting(QHBoxLayout):

    def __init__(self, name):

        super().__init__()

        label = QLabel(name)
        dropdown = QComboBox()
        dropdown.addItems(["On", "Off"])
        dropdown.setStyleSheet("background-color: #151821; border-style: none;")
        
        self.addWidget(label)
        self.addWidget(dropdown)


