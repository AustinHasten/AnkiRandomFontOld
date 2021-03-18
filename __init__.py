# Author: Austin Hasten
# Initial Commit: Mar 16 2021

import random
from aqt.qt import *
from PyQt5.QtCore import *
from aqt import mw, gui_hooks
from aqt.utils import showInfo

class ConfigGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.buildGUI()
        
    def buildGUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.leftList = QListWidget()
        self.leftList.setSortingEnabled(True)

        self.doubleLeft = QPushButton('<<')
        self.doubleLeft.pressed.connect(self.doubleLeftClicked)
        self.singleLeft = QPushButton('<')
        self.singleLeft.pressed.connect(self.singleLeftClicked)
        self.singleRight = QPushButton('>')
        self.singleRight.pressed.connect(self.singleRightClicked)
        self.doubleRight = QPushButton('>>')
        self.doubleRight.pressed.connect(self.doubleRightClicked)
        
        self.saveButton = QPushButton('Save')
        self.saveButton.pressed.connect(self.saveClicked)
        self.closeButton = QPushButton('Close')
        self.closeButton.pressed.connect(self.closeClicked)
        
        self.rightList = QListWidget()
        self.rightList.setSortingEnabled(True)
        
        # Place enabled fonts in the left list, disabled fonts in the right.
        for font, enabled in config.items():
            l = self.leftList if enabled else self.rightList
            QListWidgetItem(font, l)

        self.layout.addWidget(self.leftList, 0, 0, 6, 1)
        self.layout.addWidget(self.doubleLeft, 0, 1)
        self.layout.addWidget(self.singleLeft, 1, 1)
        self.layout.addWidget(self.singleRight, 2, 1)
        self.layout.addWidget(self.doubleRight, 3, 1)
        self.layout.addWidget(self.saveButton, 4, 1)
        self.layout.addWidget(self.closeButton, 5, 1)
        self.layout.addWidget(self.rightList, 0, 2, 6, 1)
        
    def doubleLeftClicked(self):
        for i in range(self.rightList.count()):
            self.leftList.addItem(self.rightList.takeItem(0))
    
    def singleLeftClicked(self):
        item = self.rightList.takeItem(self.rightList.currentRow())
        self.leftList.addItem(item)
        
    def singleRightClicked(self):
        item = self.leftList.takeItem(self.leftList.currentRow())
        self.rightList.addItem(item)
        
    def doubleRightClicked(self):
        for i in range(self.leftList.count()):
            self.rightList.addItem(self.leftList.takeItem(0))
            
    def saveClicked(self):
        for i in range(self.leftList.count()):
            config[self.leftList.item(i).text()] = True
        for i in range(self.rightList.count()):
            config[self.rightList.item(i).text()] = False
        mw.addonManager.writeConfig(__name__, config)

    def closeClicked(self):
        self.close()

def randomizefont(html, card, context):
    thefont = random.choice(enabledfonts)
    return html + '''
        <script>
            el = document.getElementsByClassName("randomfont")
            for(var i = 0; i < el.length; i++) {
                el[i].style.fontFamily = "''' + thefont + '''";
            }
        </script>
        '''
    
def showConfig() -> None:
    mw.configWindow = widget = ConfigGUI()
    widget.show()

# Load config and installed Japanese fonts.
config = mw.addonManager.getConfig(__name__)
jpfonts = QFontDatabase().families(QFontDatabase.Japanese)

# Remove from the config any fonts which have been uninstalled.
deletedfonts = [_ for _ in config.keys() if _ not in jpfonts]
for font in deletedfonts:
    del config[font]
    
# An installed font does not exist in the config (newly installed?). Add it to the config.
for font in jpfonts:
    if font not in config.keys():
        config[font] = True

action = QAction("Configure Random Fonts", mw)
qconnect(action.triggered, showConfig)
mw.form.menuTools.addAction(action)

# If all fonts are disabled, don't actually change the cards.
enabledfonts = [font for font, enabled in config.items() if enabled]
if enabledfonts:
    gui_hooks.card_will_show.append(randomizefont)
