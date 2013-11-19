import os

from PyQt4 import QtGui, QtCore

class Preferences(QtGui.QDialog):
    def __init__(self, settings, bookWidget, menuLabel, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window |
                               QtCore.Qt.WindowCloseButtonHint)
                               
        self.settings = settings
        self.menuLabel = menuLabel
        self.bookWidget = bookWidget

        self.setFixedSize(300, 180)
        self.setWindowTitle("Preferences")

        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)

        mainLayout.addWidget(QtGui.QLabel("Font:"))

        self.fontBox = QtGui.QFontComboBox()
        self.fontBox.setCurrentFont(QtGui.QFont(self.settings["FontName"]))
        self.fontBox.currentFontChanged.connect(self.setFont)
        mainLayout.addWidget(self.fontBox)

        mainLayout.addWidget(QtGui.QLabel("Zoom:"))

        self.fontSlider = QtGui.QSlider(0x1)
        self.fontSlider.setGeometry(680, 45, 85, 15)
        self.fontSlider.setTickPosition(2)
        self.fontSlider.setTickInterval(1)
        self.fontSlider.setMinimum(8)
        self.fontSlider.setMaximum(24)
        self.fontSlider.setValue(int(self.settings["fontSize"]))
        self.fontSlider.valueChanged.connect(self.zoom)
        mainLayout.addWidget(self.fontSlider)

        mainLayout.addStretch(1)

        self.restoreDefaultsButton = QtGui.QPushButton("Restore Defaults")
        self.restoreDefaultsButton.clicked.connect(self.restoreDefaults)
        mainLayout.addWidget(self.restoreDefaultsButton)

    def restoreDefaults(self):
        self.fontBox.setCurrentFont(QtGui.QFont("papyrus"))
        self.fontSlider.setValue(14)

    def setFont(self, font):
        font.setPointSize(self.fontSlider.value())
        self.bookWidget.setFont(font)
        self.settings["FontName"] = font.rawName()
        
    def zoom(self):
        self.bookWidget.setFont(QtGui.QFont(self.settings["FontName"],
                                            self.fontSlider.value()))
        self.settings["fontSize"] = str(self.fontSlider.value())
