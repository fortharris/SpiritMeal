
from PyQt4 import QtGui, QtCore

class Dictionary(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)

        self.setWindowTitle('King James Dictionary')
        self.setObjectName("containerLabel")
        self.setStyleSheet("""

                            QLabel#containerLabel { border-left: 1px solid #3199D1;
                                                   border-right: 1px solid #3199D1;
                                                   border-bottom: 1px solid #3199D1;
                                                   background: white;
                                                   }

                            """)

        self.wordList = []
        appFont = QtGui.QFont("Segoe UI", 10)
        
        self.setMaximumHeight(300)
        self.setMinimumWidth(550)

        # initialize widgets
        mainLayout = QtGui.QHBoxLayout()
        self.setLayout(mainLayout)

        self.wordListWidget = QtGui.QListWidget(self)
        self.wordListWidget.setMaximumWidth(170)
        self.wordListWidget.setFont(appFont)
        self.wordListWidget.setWhatsThis("Words in dictionary")
        self.wordListWidget.itemSelectionChanged.connect(self.showMeaning)
        mainLayout.addWidget(self.wordListWidget)

        vbox = QtGui.QVBoxLayout()
        mainLayout.addLayout(vbox)

        self.wordLine = QtGui.QLineEdit(self)
        self.wordLine.setFont(appFont)
        self.wordLine.setWhatsThis("Receives search word")
        self.wordLine.setPlaceholderText("Word")
        self.wordLine.textChanged.connect(self.locateWord)
        vbox.addWidget(self.wordLine)

        self.meaningLine = QtGui.QLineEdit(self)
        self.meaningLine.setFont(appFont)
        self.meaningLine.setWhatsThis("Displays meaning of the word")
        self.meaningLine.setReadOnly(True)
        vbox.addWidget(self.meaningLine)

        self.extraEdit = QtGui.QTextEdit(self)
        self.extraEdit.setFont(appFont)
        self.extraEdit.setWhatsThis(
            "Displays a sample quotation from the bible containing the search word")
        self.extraEdit.setReadOnly(True)
        vbox.addWidget(self.extraEdit)
        
        self.easingCurve = QtCore.QEasingCurve.OutCubic

        self.showAnimation = QtCore.QPropertyAnimation(self, 'minimumWidth')
        self.showAnimation.setDuration(200)
        self.showAnimation.setEndValue(550)
        self.showAnimation.setEasingCurve(self.easingCurve)

        self.hideAnimation = QtCore.QPropertyAnimation(self, 'minimumWidth')
        self.hideAnimation.setDuration(200)
        self.hideAnimation.setEndValue(0)
        self.hideAnimation.setEasingCurve(self.easingCurve)

        self.fetchWords()

    def show(self):
        self.showAnimation.start()

    def hide(self):
        self.hideAnimation.start()

    def loadSelectedText(self, text):
        if text in self.wordList:
            self.wordLine.setText(text)

    def fetchWords(self):
        file = open("Resources\\Dict\\Word.index", "r")
        textLines = file.readlines()
        file.close()
        for i in textLines:
            v = i.strip()
            self.wordList.append(v)
            self.wordListWidget.insertItem(
                textLines.index(i), QtGui.QListWidgetItem(v))

    def locateWord(self):
        word = self.wordLine.text().lower().strip()
        found = self.wordListWidget.findItems(word,
                                              QtCore.Qt.MatchStartsWith | QtCore.Qt.MatchRecursive)
        if len(found) != 0:
            item = found[0]
            self.wordListWidget.setCurrentItem(item)
            self.wordListWidget.scrollToItem(item, 3)

    def showMeaning(self):
        index = self.wordListWidget.currentRow()
        file = open("Resources\\Dict\\Definition.index", "r")
        textLines = file.read().split("\n\n")
        file.close()
        info = textLines[index].split("\n")
        meaning = info[0]
        extra = info[1] + '\n' + info[2]
        self.meaningLine.setText(meaning)
        self.extraEdit.setText(extra)
