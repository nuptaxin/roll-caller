import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(816, 603)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget1 = QListWidget(MainWindow)
        self.listWidget1.setGeometry(QRect(370, 120, 151, 311))
        self.listWidget1.setObjectName("listWidget1")
        self.listWidget1.setSelectionMode(QAbstractItemView.MultiSelection)
        item = QListWidgetItem()
        self.listWidget1.addItem(item)
        item = QListWidgetItem()
        self.listWidget1.addItem(item)
        item = QListWidgetItem()
        self.listWidget1.addItem(item)
        self.listWidget_2 = QListWidget(MainWindow)
        self.listWidget_2.setGeometry(QRect(600, 120, 151, 311))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.pushButton_3 = QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QRect(540, 220, 51, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(MainWindow)
        self.pushButton_4.setGeometry(QRect(540, 270, 51, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.listWidget1.isSortingEnabled()
        self.listWidget1.setSortingEnabled(False)
        item = self.listWidget1.item(0)
        item.setText(_translate("MainWindow", "test1"))
        item = self.listWidget1.item(1)
        item.setText(_translate("MainWindow", "test2"))
        item = self.listWidget1.item(2)
        item.setText(_translate("MainWindow", "test3"))
        self.listWidget1.setSortingEnabled(__sortingEnabled)
        self.pushButton_3.setText(_translate("MainWindow", "-->"))
        self.pushButton_3.clicked.connect(lambda: self.click_pushButton3())
        self.pushButton_4.setText(_translate("MainWindow", "<--"))
        self.pushButton_4.clicked.connect(lambda: self.click_pushButton4())

    def click_pushButton3(self):
        # sort rows in descending order in order to compensate shifting due to takeItem

        rows = sorted([index.row() for index in self.listWidget1.selectedIndexes()],
                      reverse=True)
        print('AAA')
        for row in rows:
            # assuming the other listWidget is called listWidget_2
            self.listWidget_2.addItem(self.listWidget1.takeItem(row))

    def click_pushButton4(self):
        # sort rows in descending order in order to compensate shifting due to takeItem

        rows = sorted([index.row() for index in self.listWidget_2.selectedIndexes()],
                      reverse=True)
        print('AAA')
        for row in rows:
            # assuming the other listWidget is called listWidget_2
            self.listWidget1.addItem(self.listWidget_2.takeItem(row))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())