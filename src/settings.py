from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton

import json
import os
import sys



# Represents the settings popup that shows when the user clicks the "settings" option in the main window's menubar
class SettingsPopup(QDialog):

    
    def __init__(self):

        super().__init__()
        
        self.setFixedSize(240, 300)
        self.setWindowTitle("Settings")
        self.setStyleSheet("""color: white; 
                                background-color: #0E0E10;
                                font-family: Garet; """)


        self.jsonPath = os.path.join(sys.path[0], "BEditSettings.json")

        with open(self.jsonPath, 'r') as file:
            self.settings = json.load(file)

        layout = QVBoxLayout()
        
        autoCloseBrckt = Setting("Auto Close Brackets", "autoCloseBrckt", self.settings["autoCloseBrckt"])
        layout.addLayout(autoCloseBrckt)

        AutoCloseQt = Setting("Auto Close Quotes", "autoCloseQt", self.settings["autoCloseQt"])
        layout.addLayout(AutoCloseQt)

        AutoIndent = Setting("Auto Indent", "autoIndent", self.settings["autoIndent"])
        layout.addLayout(AutoIndent)

        autosave = Setting("Autosave", "autosave", self.settings["autosave"])
        layout.addLayout(autosave)

        brcktPairHighlight = Setting("Bracket Pair Highlighting", "brcktPairHighlight", self.settings["brcktPairHighlight"])
        layout.addLayout(brcktPairHighlight)

        syntaxHighlight = Setting("Syntax Highlighting", "syntaxHighlight", self.settings["syntaxHighlight"])
        layout.addLayout(syntaxHighlight)

        self.setLayout(layout)

        openJson = QPushButton("Open BEditSettings.json", self)
        openJson.setGeometry(88, 270, 150, 20)
        openJson.setStyleSheet("background-color: #404040; border-style: none;")
        openJson.clicked.connect(self.__openJson)

        self.exec()

    
    # Reimplementation of  QWidget.closeEvent(). When user closes the popup, save their changes to the JSON file
    def closeEvent(self, event):

        with open(self.jsonPath, 'w') as file:
            json.dump(self.settings, file)

        self.close()

    
    # Creates a new editor window with BEditSettings.json open in it.
    def __openJson(self):
        
        self.close() # Close settings popup before opening JSON file.
        mainPath = os.path.join(sys.path[0], "main.py")
        os.system(f"python {mainPath} {self.jsonPath}") # Run shell command that opens editor, specifying BEditSettings.json as the file to open.




"""
Represents 1 individual on/off setting, and is comprised of that setting's name and the dropdown menu for it. 
In the form of a QHBoxLayout that is to be added to the SettingsPopup's layout, thus becoming a child of that layout.

CONSTRUCTOR PARAMETERS:

    title - The displayed name of the setting
    jsonName - The name of the setting in the BEditSettings.json file and thus also in the SettingsPopup.settings dictionary 
                e.g Bracket Pair Highlighting's jsonName is "brcktPairHighlight".
    enabled - Boolean indicating if the setting is on or off (True if on, False if off). 
                When the constructor is called in the SettingsPopup, this is to be ascertained through getting the value of the setting in the SettingsPopup.settings dictionary  
"""
class Setting(QHBoxLayout):


    def __init__(self, title, jsonName, enabled):

        super().__init__()

        self.title = title
        self.jsonName = jsonName

        label = QLabel(title)
        self.addWidget(label)

        dropdown = QComboBox()
        dropdown.addItems(["On", "Off"])
        dropdown.setStyleSheet("background-color: #151821; border-style: none;")
        dropdown.currentIndexChanged.connect(self.settingChange)

        # "On" is located at index 0; "Off" is at index 1.
        if enabled:
            dropdown.setCurrentIndex(0)
        else:
            dropdown.setCurrentIndex(1)
        
        self.addWidget(dropdown)


    def settingChange(self, index):
        
        try:
            settings = self.parentWidget().settings # For a layout, .parentWidget returns the widget that implements the layout's parent layout, in this case SettingsPopup.

            # "On" is located at index 0; "Off" is at index 1.
            if index == 0: 
                settings[self.jsonName] = True
            elif index == 1:
                settings[self.jsonName] = False

        # Thrown when self.parentWidget() returns None, which only occurs when setting is being initialized, as the setting at that stage has not been assigned as a child to the SettingsPopup layout via .addLayout().
        except AttributeError: 
            pass