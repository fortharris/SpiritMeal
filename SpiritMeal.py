import sys
import os
import re
from PyQt4 import QtGui, QtCore

from Extensions.Dictionary import Dictionary
from Extensions.Preferences import Preferences


old_books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
            "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
            "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
            "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes",
            "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
            "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah",
            "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
            "Malachi"]
old_chapters = [
    50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10,
    42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3,
    2, 14, 4]

new_books = ["Matthew", "Mark", "Luke", "John", "Acts", "Romans",
            "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
            "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
            "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
            "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
            "Jude", "Revelation"]
new_chapters = [
                28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13,
                5, 5, 3, 5, 1, 1, 1, 22]


class SearchThread(QtCore.QThread):

    def run(self):
        self.searchResults = []

        if self.searchBook == "Old and New":
            self.dir_search("Resources\\Books\\Old_Testament",
                           old_books)
            self.dir_search("Resources\\Books\\New_Testament",
                           new_books)
        elif self.searchBook == "Old Testament":
            self.dir_search("Resources\\Books\\Old_Testament",
                           old_books)
        elif self.searchBook == "New Testament":
            self.dir_search("Resources\\Books\\New_Testament",
                           new_books)
        else:
            if self.searchBook in old_books:
                path =  \
                    "Resources\\Books\\Old_Testament\\" + \
                    self.searchBook + ".bk"
            elif self.searchBook in new_books:
                path = \
                    "Resources\\Books\\New_Testament\\" + \
                    self.searchBook + ".bk"
            self.book_search(path)

    def book_search(self, path):
        searchItem = re.compile(self.searchItem, re.IGNORECASE)
        file = open(path, "r")
        textList = file.read().split("\n\n")
        file.close()
        for line in textList:
            f = searchItem.finditer(line)
            for i in f:
                verse = line.split(' ')[0]
                self.searchResults.append(self.searchBook + '#' + verse)

    def dir_search(self, location, bookList):
        searchItem = re.compile(self.searchItem, re.IGNORECASE)
        for i in bookList:
            path = os.path.join(location, i + ".bk")
            file = open(path, "r")
            textList = file.read().split("\n\n")
            file.close()
            for line in textList:
                f = searchItem.finditer(line)
                for v in f:
                    verse = line.split(' ')[0]
                    self.searchResults.append(i + '#' + verse)

    def search(self, searchItem, searchBook):
        self.searchItem = searchItem
        self.searchBook = searchBook
        self.start()


class SearchWidget(QtGui.QWidget):

    lookupSearchItem = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.searchEngine = SearchThread()
        self.setMaximumWidth(200)

        self.setBackgroundRole(QtGui.QPalette.Light)
        self.setAutoFillBackground(True)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setMargin(0)

        headLabel = QtGui.QLabel()
        headLabel.setMaximumHeight(40)
        headLabel.setScaledContents(True)
        headLabel.setPixmap(QtGui.QPixmap("Resources\\Icons\\Trans"))
        headLabel.setMaximumWidth(200)

        hbox = QtGui.QHBoxLayout()
        hbox.setMargin(0)

        label = QtGui.QLabel()
        label.setMaximumWidth(20)
        label.setMaximumHeight(20)
        label.setScaledContents(True)
        label.setPixmap(QtGui.QPixmap("Resources\\Icons\\find"))
        hbox.addWidget(label)

        hbox.addStretch(1)

        closeButton = QtGui.QToolButton()
        closeButton.setAutoRaise(True)
        closeButton.setIconSize(QtCore.QSize(16, 16))
        closeButton.setIcon(QtGui.QIcon("Resources\\Icons\\close_black"))
        closeButton.clicked.connect(self.hide)
        hbox.addWidget(closeButton)

        headLabel.setLayout(hbox)

        mainLayout.addWidget(headLabel)

        self.searchResListWidget = QtGui.QListWidget()
        self.searchResListWidget.itemActivated.connect(self.open_search_item)
        self.searchResListWidget.setFont(QtGui.QFont("Segoe UI", 10))
        self.searchResListWidget.itemSelectionChanged.connect(
            self.open_search_item)
        mainLayout.addWidget(self.searchResListWidget)

        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(5)
        vbox.setSpacing(5)

        self.searchLine = QtGui.QLineEdit()
        self.searchLine.setPlaceholderText("Search")
        self.searchLine.returnPressed.connect(self.start_search)

        self.searchBox = QtGui.QComboBox()
        self.searchBox.setLineEdit(self.searchLine)
        self.searchBox.setEditable(True)
        vbox.addWidget(self.searchBox)

        self.searchButton = QtGui.QPushButton("Find")
        self.searchButton.setMinimumHeight(25)
        self.searchButton.clicked.connect(self.start_search)
        vbox.addWidget(self.searchButton)

        vbox.addWidget(QtGui.QLabel(" Look in:"))

        self.searchLockBox = QtGui.QComboBox()
        self.searchLockBox.setFont(QtGui.QFont("Segoe UI", 10))
        self.searchLockBox.setMaxVisibleItems(26)
        self.searchLockBox.setToolTip("Search location")
        self.searchLockBox.addItem("Old and New")
        self.searchLockBox.addItem("Old Testament")
        self.searchLockBox.addItem("New Testament")
        self.searchLockBox.insertSeparator(3)
        for i in old_books:
            self.searchLockBox.addItem(i)
        self.searchLockBox.insertSeparator(43)
        for i in new_books:
            self.searchLockBox.addItem(i)
        vbox.addWidget(self.searchLockBox)
        self.searchLockBox.setStyleSheet(""" 
       
                         QComboBox {
                             color: black;
                             border: none;
                             border-bottom: 1px solid black;
                             border-radius: 0px;
                             padding: 2px 2px 2px 3px;
                         }
           
                        """)

        mainLayout.addLayout(vbox)

        self.easingCurve = QtCore.QEasingCurve.OutCubic

        self.showAnimation = QtCore.QPropertyAnimation(self, 'maximumWidth')
        self.showAnimation.setDuration(200)
        self.showAnimation.setEndValue(200)
        self.showAnimation.setEasingCurve(self.easingCurve)

        self.hideAnimation = QtCore.QPropertyAnimation(self, 'maximumWidth')
        self.hideAnimation.setDuration(200)
        self.hideAnimation.setEndValue(0)
        self.hideAnimation.setEasingCurve(self.easingCurve)

        self.setLayout(mainLayout)
        self.hide()

        self.searchEngine.finished.connect(self.finalize_search)

    def show(self, text):
        self.searchLine.setText(text)
        self.showAnimation.start()

    def hide(self):
        self.hideAnimation.start()

    def open_search_item(self):
        Index = self.searchResListWidget.currentRow()
        if len(self.searchEngine.searchResults) == 0:
            pass
        else:
            param = self.searchEngine.searchResults[Index].split('#')
            initial = self.searchEngine.searchResults.index(
                self.searchEngine.searchResults[Index])
            value = (Index - initial)
            if value == 0:
                iter_value = 1
            else:
                iter_value = value + 1
            param.append(iter_value)
            param.insert(0, self.searchItem)
            self.lookupSearchItem.emit(param)

    def start_search(self):
        self.searchItem = self.searchLine.text().strip()
        if self.searchItem == '':
            return
        self.searchResListWidget.clear()
        searchBook = self.searchLockBox.currentText()
        self.searchEngine.search(self.searchItem, searchBook)
        self.searchButton.setDisabled(True)

    def finalize_search(self):
        if len(self.searchEngine.searchResults) < 1:
            self.searchResListWidget.addItem(QtGui.QListWidgetItem("0 found"))
        else:
            for i in self.searchEngine.searchResults:
                f = i.replace('#', ' ')
                self.searchResListWidget.addItem(QtGui.QListWidgetItem(f))
        self.searchResListWidget.setCurrentRow(0,
                                               QtGui.QItemSelectionModel.NoUpdate)
        self.searchButton.setDisabled(False)


class SpiritMeal(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowIcon(QtGui.QIcon("Resources\\Icons\\smIcon"))
        self.setWindowTitle("SpiritMeal - King James Bible")
        self.setMinimumWidth(600)

        # load configuration from file
        tempList = []
        file = open("settings.ini", "r")
        for i in file.readlines():
            if i.strip() == '':
                pass
            else:
                tempList.append(tuple(i.strip().split('=')))
        file.close()
        self.settings = dict(tempList)

        data = QtGui.QFontDatabase()
        data.addApplicationFont("Resources\\Fonts\\papyrus.ttf")
        data.addApplicationFont("Resources\\Fonts\\droidsans_final_fixed.ttf")

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.setMargin(0)
        mainLayout.setSpacing(0)

        self.bookWidget = QtGui.QPlainTextEdit()
        self.bookWidget.setStyleSheet("""                     
                                QWidget {
                                selection-color: black;
                                selection-background-color: rgba(0, 0, 0, 50);
                            } """)
        self.bookWidget.setReadOnly(True)
        self.bookWidget.setFont(QtGui.QFont(self.settings["FontName"],
                                            int(self.settings["fontSize"])))

        self.scrollBar = self.bookWidget.verticalScrollBar()
        
        dictLayout = QtGui.QVBoxLayout()
        dictLayout.setMargin(0)
        self.bookWidget.setLayout(dictLayout)
        
        hbox = QtGui.QHBoxLayout()
        dictLayout.addLayout(hbox)
        
        self.dictionary = Dictionary(self)
        self.dictionary.setMaximumWidth(300)
        hbox.addWidget(self.dictionary)
        
        dictLayout.addStretch(1)

        self.searchWidget = SearchWidget()
        self.searchWidget.lookupSearchItem.connect(self.openSearchItem)
        mainLayout.addWidget(self.searchWidget)

        bookLayout = QtGui.QVBoxLayout()
        bookLayout.setMargin(0)

        self.menuLabel = QtGui.QLabel()
        self.menuLabel.setMinimumHeight(40)
        self.menuLabel.setMaximumHeight(40)
        self.menuLabel.setScaledContents(True)
        self.menuLabel.setPixmap(QtGui.QPixmap("Resources\\Icons\\Wood 2"))

        menuLayout = QtGui.QHBoxLayout()

        self.bookBox = QtGui.QComboBox()
        self.bookBox.setItemDelegate(QtGui.QStyledItemDelegate())
        self.bookBox.setMaxVisibleItems(20)
        self.bookBox.setMinimumWidth(170)
        self.bookBox.setFont(QtGui.QFont("Segoe UI", 10))
        self.bookBox.setStyleSheet(""" 
       
                     QComboBox::down-arrow {
                         image: None;
                     }
           
                        """)

        for i in old_books:
            self.bookBox.addItem(i)
        self.bookBox.insertSeparator(44)
        for i in new_books:
            self.bookBox.addItem(i)
        menuLayout.addWidget(self.bookBox)
        self.bookBox.activated.connect(self.lookUp)

        menuLayout.addWidget(QtGui.QLabel("Chapter"))

        self.chapterBox = QtGui.QComboBox()
        self.chapterBox.setItemDelegate(QtGui.QStyledItemDelegate())
        self.chapterBox.setMinimumWidth(60)
        self.chapterBox.setMaximumWidth(60)
        self.chapterBox.setMaxVisibleItems(20)
        self.chapterBox.activated.connect(self.loadVerses_2)
        menuLayout.addWidget(self.chapterBox)
        self.chapterBox.setStyleSheet(""" 
       
                     QComboBox::down-arrow {
                         image: None;
                     }
           
                        """)

        menuLayout.addWidget(QtGui.QLabel("Verse"))

        self.verseBox = QtGui.QComboBox()
        self.verseBox.setItemDelegate(QtGui.QStyledItemDelegate())
        self.verseBox.setMinimumWidth(60)
        self.verseBox.setMaximumWidth(60)
        self.verseBox.setMaxVisibleItems(20)
        self.verseBox.activated.connect(self.findChapVerse)
        menuLayout.addWidget(self.verseBox)
        self.verseBox.setStyleSheet(""" 
       
                     QComboBox::down-arrow {
                         image: None;
                     }
           
                        """)

        menuLayout.addStretch(1)

        self.menuButton = QtGui.QPushButton("Options")
        self.menuButton.setFlat(True)
        
        menuLayout.addWidget(self.menuButton)

        self.createMenu()

        menuLayout.addStretch(1)

        self.dictionaryButton = QtGui.QToolButton()
        self.dictionaryButton.setAutoRaise(True)
        self.dictionaryButton.setDefaultAction(self.dictionaryAct)
        menuLayout.addWidget(self.dictionaryButton)

        self.findButton = QtGui.QToolButton()
        self.findButton.setAutoRaise(True)
        self.findButton.setDefaultAction(self.findAct)
        menuLayout.addWidget(self.findButton)

        self.menuLabel.setLayout(menuLayout)

        bookLayout.addWidget(self.menuLabel)
        bookLayout.addWidget(self.bookWidget)

        mainLayout.addLayout(bookLayout)

        mainLayout.setStretch(1, 1)
        self.setLayout(mainLayout)

        self.prefs = Preferences(
            self.settings, self.bookWidget, self.menuLabel,  self)

        if self.settings["FirstRun"] == "True":
            self.resize(900, 600,)

            screen = QtGui.QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width() - size.width()) / 2,
                     (screen.height() - size.height()) / 2)
                     
            self.settings["FirstRun"] = "False"
            self.saveSettings()
        else:
            self.readUiSettings()
        self.restorePreviousState()

    def showFindWidget(self):
        if self.searchWidget.maximumWidth() == 200:
            self.searchWidget.hide()
        else:
            selected_text = self.getSelectedText()
            self.searchWidget.show(selected_text)
            self.searchWidget.searchLine.selectAll()
            self.searchWidget.searchLine.setFocus(True)

    def createMenu(self):
        self.exitAct = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\exit"),
                                     "Exit", self, shortcut="Ctrl+Q", triggered=self.close)

        self.theWordAct = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\1.png"),
                                        "Truth about the Word", self, triggered=self.theWordLauncher)

        self.bornAgainAct = QtGui.QAction(
            QtGui.QIcon("Resources\\Icons\\2.png"),
            "What it means to be Born Again", self,
            triggered=self.bornAgainLauncher)

        self.prayWordAct = QtGui.QAction(
            QtGui.QIcon("Resources\\Icons\\3.png"),
            "How to Pray the Word", self, triggered=self.prayWordLauncher)

        self.link_1 = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\earth"),
                                    "http://www.studytheword.net", self,
                                    triggered=self.studywordLauncher)

        self.link_2 = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\earth"),
                                    "http://www.crossroad.to/HisWord/verses/topics/1-index.htm", self,
                                    triggered=self.crossroadLauncher)

        self.link_3 = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\earth"),
                                    "http://www.looktojesus.com/index.html", self,
                                    triggered=self.looktojesusLauncher)

        self.findAct = QtGui.QAction(
            QtGui.QIcon("Resources\\Icons\\find_"), "Find",
            self, shortcut="Ctrl+F",
            triggered=self.showFindWidget)

        self.dictionaryAct = \
            QtGui.QAction(QtGui.QIcon("Resources\\Icons\\dictionary"),
                          "King James Dictionary", self, shortcut="Ctrl+D",
                          triggered=self.showDictionary)

        self.helpAct = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\Help.png"),
                                     "Help", self, shortcut="F1", triggered=self.helpEngine)

        self.webAct = QtGui.QAction("Visit Homepage", self, triggered=self.web)

        self.aboutAct = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\info"),
                                      "About SpiritMeal",
                                      self, triggered=self.about)

        prefsAct = QtGui.QAction(QtGui.QIcon("Resources\\Icons\\Fav"),
                                 "Preferences", self, triggered=self.showPrefsWidget)

        menu = QtGui.QMenu()

        viewMenu = menu.addMenu("View")
        viewMenu.addAction(self.theWordAct)
        viewMenu.addAction(self.bornAgainAct)
        viewMenu.addAction(self.prayWordAct)
        viewMenu.addAction(self.link_1)
        viewMenu.addAction(self.link_2)
        viewMenu.addAction(self.link_3)

        menu.addSeparator()
        menu.addSeparator()
        menu.addAction(prefsAct)
        helpMenu = menu.addMenu("Help")
        helpMenu.addAction(self.helpAct)
        helpMenu.addAction(self.webAct)
        helpMenu.addAction(self.aboutAct)
        menu.addSeparator()
        menu.addAction(self.exitAct)

        self.menuButton.setMenu(menu)

    def restorePreviousState(self):
        index = self.bookBox.findText(self.settings["LastOpenedBook"])
        self.lookUp(index)
        self.bookBox.setCurrentIndex(index)
        self.scrollBar.setSliderPosition(
            int(self.settings["ScrollBarPosition"]))

    def theWordLauncher(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "Resources\\Books\\Word of God.html"))

    def bornAgainLauncher(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "Resources\\Books\\Born_Again.html"))

    def prayWordLauncher(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "Resources\\Books\\Pray the Word.html"))

    def studywordLauncher(self):
        QtGui.QDesktopServices().openUrl(
            QtCore.QUrl("http://studytheword.net"))

    def crossroadLauncher(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "http://www.crossroad.to/HisWord/verses/topics/1-index.htm"))

    def looktojesusLauncher(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "http://www.looktojesus.com/index.html"))

    def helpEngine(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "Resources\\Help\\welcome.html"))

    def web(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(
            "http://www.spiritmeal.clanteam.com"))

    def readUiSettings(self):
        UIsettings = QtCore.QSettings("Amoatey Harrison", "SpiritMeal")
        UIsettings.beginGroup("MainWindow")
        self.setGeometry(UIsettings.value("geometry"))
        UIsettings.endGroup()

    def closeEvent(self, event):
        UIsettings = QtCore.QSettings("Amoatey Harrison", "SpiritMeal")
        UIsettings.beginGroup("MainWindow")
        UIsettings.setValue("geometry", self.geometry())
        UIsettings.endGroup()

        self.settings["ScrollBarPosition"] = str(
            self.scrollBar.sliderPosition())
        self.saveSettings()

        event.accept()
        
    def saveSettings(self):
        file = open("settings.ini", "w")
        for key, value in self.settings.items():
            file.write('\n' + key + '=' + value)
        file.close()

    def showPrefsWidget(self):
        self.prefs.exec_()

    def getSelectedText(self):
        cursor = self.bookWidget.textCursor()
        selected_text = cursor.selectedText().capitalize().strip()

        return selected_text

    def about(self):
        QtGui.QMessageBox.about(self, "About SpiritMeal",
                                "<p>Version: 3.0"
                                "<p>Author: Amoatey Harrison"
                                "<p>Email: fortharris@gmail.com")

    def lookUp(self, index):
        book_name = self.bookBox.itemText(index)
        if index <= 38:
            path = "Resources\\Books\\Old_Testament\\" + book_name + ".bk"
            file = open(path, "r")
            self.bookWidget.setPlainText(file.read())
            file.close()
            index = old_books.index(book_name)
            chapNum = old_chapters[index]
            self.chapterBox.clear()
            self.verseBox.clear()
            for i in range(chapNum):
                self.chapterBox.addItem(str(i + 1))
            self.loadVerses()
            self.settings["LastOpenedBook"] = book_name
        elif index >= 40:
            path = "Resources\\Books\\New_Testament\\" + book_name + ".bk"
            file = open(path, "r")
            self.bookWidget.setPlainText(file.read())
            file.close()
            index = new_books.index(book_name)
            chapNum = new_chapters[index]
            self.chapterBox.clear()
            self.verseBox.clear()
            for i in range(chapNum):
                self.chapterBox.addItem(str(i + 1))
            self.loadVerses()
            self.settings["LastOpenedBook"] = book_name

    def loadVerses(self):
        # loads verses only
        chapter = self.chapterBox.currentText()
        c = "\n\n" + chapter + ":"
        count = self.bookWidget.toPlainText().count(c)
        self.verseBox.clear()
        if int(chapter) == 1:
            count += 1
            for i in range(count):
                c = str(int(i) + 1)
                self.verseBox.addItem(c)
        else:
            for i in range(count):
                c = str(int(i) + 1)
                self.verseBox.addItem(c)

    def loadVerses_2(self):
        # loads verses and opens comboBox for verse selection
        self.loadVerses()
        self.findChapVerse()
        self.verseBox.showPopup()

    def findChapVerse(self):
        chapter = self.chapterBox.currentText()
        verse = self.verseBox.currentText()
        combined = chapter + ":" + verse
        self.bookWidget.moveCursor(QtGui.QTextCursor.Start)
        self.bookWidget.find(combined, QtGui.QTextDocument.FindWholeWords)
        self.bookWidget.centerCursor()

    def openSearchItem(self, param):
        searchItem = param[0]
        book = param[1]
        chapVerse = param[2]
        iter_value = param[3]
        if book == main.bookBox.currentText():
            # find operation
            main.bookWidget.moveCursor(1)
            main.bookWidget.find(chapVerse)
            main.bookWidget.centerCursor()
            for i in range(iter_value):
                main.bookWidget.find(searchItem)
        else:
            main.bookBox.setCurrentIndex(main.bookBox.findText(book))
            if book in old_books:
                loc = "Resources\\Books\\Old_Testament\\" + book + ".bk"
                file = open(loc, "r")
                main.bookWidget.setPlainText('\n\n' + file.read())
                file.close()
                index = old_books.index(book)
                chapNum = old_chapters[index]
            else:
                loc = "Resources\\Books\\New_Testament\\" + book + ".bk"
                file = open(loc, "r")
                main.bookWidget.setPlainText('\n\n' + file.read())
                file.close()
                index = new_books.index(book)
                chapNum = new_chapters[index]

            # find operation
            main.bookWidget.find(chapVerse)
            main.bookWidget.centerCursor()
            for i in range(iter_value):
                main.bookWidget.find(searchItem)
            main.chapterBox.clear()
            main.verseBox.clear()
            for i in range(chapNum):
                main.chapterBox.addItem(str(i + 1))
            main.loadVerses()

    def showDictionary(self):
        if self.dictionary.minimumHeight() == 0:
            selected_text = self.getSelectedText()
            if selected_text != '':
                self.dictionary.loadSelectedText(selected_text)
            self.dictionary.show()
        else:
            self.dictionary.hide()


app = QtGui.QApplication(sys.argv)
app.setStyleSheet("""

                    QWidget {
                                selection-color: white;
                                selection-background-color: #2B2BFF;
                            }

                     QComboBox {
                         color: white;
                         border: none;
                         border-bottom: 1px solid black;
                         border-radius: 0px;
                         padding: 2px 2px 2px 3px;
                     }

                     QComboBox:editable {
                         background: white;
                         color: black;
                     }

                     QComboBox:!editable, QComboBox::drop-down:editable {
                          background: transparent;
                          border-radius: 0px;
                     }

                     /* QComboBox gets the "on" state when the popup is open */
                     QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                         background: transparent;
                         color: black;
                     }

                     QComboBox:on { /* shift the text when the popup opens */
                     }

                     QComboBox::drop-down {
                         subcontrol-origin: padding;
                         subcontrol-position: top right;
                         width: 15px;
                         border: none;
                     }

                     QComboBox::down-arrow {
                         image: url(Resources/Icons/downarrow.png);
                     }

                     QComboBox::down-arrow:on { /* shift the arrow when popup is open */
                         top: 1px;
                         left: 0px;
                     }

                     QComboBox::down-arrow:on { /* shift the arrow when popup is open */
                         border: none;
                     }

                     QComboBox QAbstractItemView {
                         border: none;
                         selection-background-color: #2B2BFF;
                     }

                     QComboBox QAbstractItemView::item {
                         min-height: 25px;
                     }

                    QMenu {
                         background: #E6E6E6;
                         padding: 2px;
                    }

                    QMenu::item {
                         padding: 5px 30px 5px 30px;
                         border: none;
                    }

                    QMenu::item:selected:enabled {
                         border-color: none;
                         background: #FAFAFA;
                    }

                    QMenu::separator {
                         height: 1px;
                         background-color: lightgrey;
                    }

                    QMenu::indicator {
                         width: 13px;
                         height: 13px;
                    }

                     QListView {
                         border: none;
                         show-decoration-selected: 1; /* make the selection span the entire width of the view */
                     }

                     QListView::item {
                         border: none;
                     }

                     QListView::item:alternate {
                         background: #EEEEEE;
                     }

                     QListView::item:selected {
                         border: none;
                         color: white;
                     }

                     QListView::item:selected:!active {
                         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                     stop: 0 #000000, stop: 1 #333333);
                     }

                     QListView::item:selected:active {
                         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                     stop: 0 #000000, stop: 1 #333333);
                     }

                     QListView::item:hover {
                         background: white;
                     }

                    QPlainTextEdit {
                        color: black;
                        border: none;
                        border-left: 1px solid lightgrey;
                        background: #FFFECB;
                    }


                    QSlider::groove:horizontal {
                         border: 1px inset #CCCCCC;
                         height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D2D2D2, stop:1 #FFFFFF);
                         margin: 2px 0;
                         border-radius: 5px;
                    }

                    QSlider::handle:horizontal {
                         background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D2D2D2, stop:1 #C3C3C3);
                         border: 1px solid #5c5c5c;
                         width: 18px;
                         margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
                         border-radius: 3px;
                    }


                    QScrollBar:vertical{
                        padding: 1px;
                        padding-left: 0px;
                        background: #f1f1f1;
                        width: 13px;
                        border: none;
                    }

                    QScrollBar:horizontal{
                        padding: 2px;
                        border: none;
                        background: #f1f1f1;
                        height: 13px;
                    }

                    QScrollBar::handle:vertical{
                        background: #DBB081;
                        border-radius: 0px;
                        border-top-right-radius: 5px;
                        border-bottom-right-radius: 5px;
                        border: none;
                        min-height: 30px;
                    }

                    QScrollBar::handle:horizontal{
                        background: #969ea7;
                        border-radius: 4px;
                        border: none;
                    }

                    QScrollBar::add-line:vertical,
                    QScrollBar::sub-line:vertical,
                    QScrollBar::add-page:vertical,
                    QScrollBar::sub-page:vertical,
                    QScrollBar::add-line:horizontal,
                    QScrollBar::sub-line:horizontal,
                    QScrollBar::add-page:horizontal,
                    QScrollBar::sub-page:horizontal{
                        background: none;
                        border: none;
                        height: 0px;
                    }

                    QScrollBar::up-arrow:vertical {
                      border: none;
                      width: 10px;
                      height: 0px;
                    }

                    QScrollBar::down-arrow:vertical {
                      border: none;
                      width: 10px;
                      height: 0px;
                    }

                    QScrollBar::left-arrow:horizontal {
                      border: none;
                      width: 10px;
                      height: 10px;
                    }

                    QScrollBar::right-arrow:horizontal {
                      border: none;
                      width: 10px;
                      height: 10px;
                    }

                    QToolButton {
                        background: rgba(0, 0, 0, 0);
                        border: none;
                        background: none;
                    }

                    QToolButton:hover {
                        background: none;
                    }

                    QToolButton:pressed {
                        background: none;
                        padding-top: 2px;
                    }

                    QToolButton:disabled {
                        background: none;
                    }
                    
                    QPushButton {
                        background: rgba(0, 0, 0, 0);
                        border: none;
                        padding-left: 4px;
                        padding-right: 4px;
                        min-height: 30px;
                        min-width: 20px;
                    }

                    QPushButton:hover {
                        background: rgba(0, 0, 0, 50);
                    }

                    QPushButton:pressed {
                        background: rgba(0, 0, 0, 100);
                        padding-top: 2px;
                    }

                    QPushButton:disabled {
                        background: #FFFFFF;
                    }

            """)

app.setEffectEnabled(False)

main = SpiritMeal()
main.show()

sys.exit(app.exec_())
