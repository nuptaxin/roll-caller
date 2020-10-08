import random
import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon


class MyApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        # 设置字体大小
        self.font = QFont()
        self.font.setPointSize(23)
        with open("conf/namelist.txt", "r", encoding='utf-8') as f:
            self.name_list = f.read().splitlines()
        mkpath = "cache"
        self.local_rm(mkpath)
        self.mkdir(mkpath)
        file = open('cache/data.txt', 'w', encoding='utf-8')
        for line in self.name_list:
            file.write(line + '\n')
        file = open('cache/skip.txt', 'w', encoding='utf-8')
        self.App()

    def App(self):

        # 设置start按钮
        self.start_button = QPushButton('Start', self)
        self.start_button.setFont(self.font)
        self.start_button.resize(200, 100)
        self.start_button.move(650, 100)

        #设置stop按钮
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.resize(200, 100)
        self.stop_button.move(650, 450)
        self.stop_button.setFont(self.font)

        # 设置名字显示
        self.name_lable = QLineEdit(self)
        self.name_lable.move(100, 450)
        self.name_lable.resize(350, 100)
        self.name_lable.setText('这个人是谁呢？')
        self.name_lable.setAlignment(Qt.AlignCenter)
        self.name_lable.setFont(self.font)

        self.timer = QTimer(self)

        # 设置图片显示
        self.image_lable = QLabel(self)
        #为图片显示设置一个画布 位置大小
        self.image_lable.setGeometry(50, 50, 470, 300)
        #为图片设置属性
        self.image_lable.setStyleSheet("border: 2px solid blue")
        defaultimage= 'images/开始点名.jpg'
        self.pnx = QPixmap(defaultimage)  # 加载图片路径
        self.image_lable.setPixmap(self.pnx)  # 将图片显示画布上
        self.image_lable.setScaledContents(True)  # 图片自适应窗

        # 设置开始和结束
        # print(self.start_button.isEnabled()) True 可以点击为True 不可以点击为False
        self.start_button.clicked.connect(lambda: self.start_name())

        self.stop_button.clicked.connect(lambda: self.stop())
        self.stop_button.clicked.connect(lambda: self.btnsetenabled(self.start_button))
        # 设置图片显示

        self.start_music = Phonon.createPlayer(Phonon.MusicCategory, Phonon.MediaSource("music/start.mp3"))
        self.end_music = Phonon.createPlayer(Phonon.MusicCategory, Phonon.MediaSource("music/end.mp3"))

    def reinit(self):
        defaultimage = 'images/开始点名.jpg'
        self.pnx = QPixmap(defaultimage)  # 加载图片路径
        self.image_lable.setPixmap(self.pnx)  # 将图片显示画布上
        self.image_lable.setScaledContents(True)  # 图片自适应窗
        self.name_lable.setText('这个人是谁呢？')
        self.start_music.stop()
        self.end_music.stop()
        self.timer.stop()
        self.btnsetenabled(self.start_button)

    def setname_image(self):
        #点名系统
        with open("cache/data.txt", "r", encoding='utf-8') as f:
            self.new_name_list = f.read().splitlines()
        name = self.new_name_list[random.randint(0, len(self.new_name_list) - 1)]
        self.name_lable.setText(name)
        self.name_lable.setAlignment(Qt.AlignCenter)  # 设置文本对齐方式 居中对齐
        self.name_lable.setFont(self.font)
        self.imagename= 'images/student-avatar/' + str(name) +'.jpg'  #设置图片路径
        self.pnx = QPixmap(self.imagename).scaled(self.image_lable.width(), self.image_lable.height(), Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation)
        self.image_lable.setPixmap(self.pnx) #将图片显示画布上
        self.image_lable.setAlignment(Qt.AlignCenter)
        self.image_lable.setScaledContents(False)
        #self.image_lable.setScaledContents(True)  # 图片自适应窗口


    #开始程序
    def start_name(self):
        self.start_button.setEnabled(False)  #将start按钮设置成禁止点击
        self.end_music.stop()
        self.start_music.play()
        self.timer.timeout.connect(self.setname_image)
        self.timer.start(50) #图片播放的时间

    # 程序结束
    def stop(self):
        self.start_music.stop()
        self.end_music.play()
        self.timer.stop()
        #移除当前的
        curr_name=self.name_lable.text()
        with open("cache/data.txt", "r", encoding='utf-8') as f:
            self.curr_name_list = f.read().splitlines()
        file = open('cache/data.txt', 'w', encoding='utf-8')
        for i in self.curr_name_list:
            if(curr_name!=i):
                file.write(i + '\n')

        file = open('cache/skip.txt', 'a', encoding='utf-8')
        file.write(curr_name + '\n')

    #设置按钮解禁
    def btnsetenabled(self,btn):
        # print(btn.isEnabled()) False
        # 按下按钮后解除禁止可以继续点击
        btn.setEnabled(True)

    def mkdir(self, path):
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            print
            path + ' 创建成功'
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print
            path + ' 目录已存在'
            return False

    def local_rm(self, dirpath):
        if os.path.exists(dirpath):
            files = os.listdir(dirpath)
            for file in files:
                filepath = os.path.join(dirpath, file).replace("\\", '/')
                if os.path.isdir(filepath):
                    self.local_rm(filepath)
                else:
                    os.remove(filepath)
            os.rmdir(dirpath)

class ManageWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget1 = QListWidget(self)
        self.listWidget1.setGeometry(QRect(170, 120, 151, 311))
        self.listWidget1.setObjectName("listWidget1")
        self.listWidget1.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget_2 = QListWidget(self)
        self.listWidget_2.setGeometry(QRect(400, 120, 151, 311))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QRect(340, 220, 51, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setGeometry(QRect(340, 270, 51, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.save_button = QPushButton('Save', self)
        self.save_button.resize(100, 50)
        self.save_button.move(500, 450)
        #self.refresh_button = QPushButton('Refresh', self)
        #self.refresh_button.resize(100, 50)
        #self.refresh_button.move(300, 450)
        self.retranslateUi()

    def retranslateUi(self):
        __sortingEnabled = self.listWidget1.isSortingEnabled()
        self.listWidget1.setSortingEnabled(False)
        with open("cache/data.txt", "r", encoding='utf-8') as f:
            for line in f.read().splitlines():
                item = QListWidgetItem(line)
                self.listWidget1.addItem(item)
        self.listWidget1.setSortingEnabled(__sortingEnabled)
        self.pushButton_3.setText(">")
        self.pushButton_3.clicked.connect(lambda: self.click_pushButton3())
        self.pushButton_4.setText("<")
        self.pushButton_4.clicked.connect(lambda: self.click_pushButton4())
        self.save_button.clicked.connect(lambda: self.click_saveButton())
        #self.refresh_button.clicked.connect(lambda: self.click_refreshButton())

    def click_pushButton3(self):
        # sort rows in descending order in order to compensate shifting due to takeItem

        rows = sorted([index.row() for index in self.listWidget1.selectedIndexes()],
                      reverse=True)
        for row in rows:
            # assuming the other listWidget is called listWidget_2
            self.listWidget_2.addItem(self.listWidget1.takeItem(row))

    def click_pushButton4(self):
        # sort rows in descending order in order to compensate shifting due to takeItem

        rows = sorted([index.row() for index in self.listWidget_2.selectedIndexes()],
                      reverse=True)
        for row in rows:
            # assuming the other listWidget is called listWidget_2
            self.listWidget1.addItem(self.listWidget_2.takeItem(row))

    def click_saveButton(self):
        file = open('cache/data.txt', 'w', encoding='utf-8')
        count = self.listWidget1.count()
        for i in range(count):
            file.write(self.listWidget1.item(i).text() + '\n')

        file = open('cache/skip.txt', 'w', encoding='utf-8')
        count = self.listWidget_2.count()
        for i in range(count):
            file.write(self.listWidget_2.item(i).text() + '\n')

    def click_refreshButton(self):
        self.listWidget1.clear()
        with open("cache/data.txt", "r", encoding='utf-8') as f:
            for line in f.read().splitlines():
                item = QListWidgetItem(line)
                self.listWidget1.addItem(item)

        self.listWidget_2.clear()
        with open("cache/skip.txt", "r", encoding='utf-8') as f:
            for line in f.read().splitlines():
                item = QListWidgetItem(line)
                self.listWidget_2.addItem(item)

    def reinit(self):
        self.listWidget1.clear()
        with open("cache/data.txt", "r", encoding='utf-8') as f:
            for line in f.read().splitlines():
                item = QListWidgetItem(line)
                self.listWidget1.addItem(item)

        self.listWidget_2.clear()
        with open("cache/skip.txt", "r", encoding='utf-8') as f:
            for line in f.read().splitlines():
                item = QListWidgetItem(line)
                self.listWidget_2.addItem(item)

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        # 设置主体框架

        # 设置窗体名字
        self.setWindowTitle('点名系统')
        # 设置窗体大小
        self.resize(1000, 600)

        self.mainTab = MyApp()
        self.mTab = ManageWidget()
        self.addTab(self.mainTab, u"主界面")
        self.addTab(self.mTab, u"管理")
        self.connect(self, SIGNAL("currentChanged(int)"), self.mainTab.reinit)
        self.connect(self, SIGNAL("currentChanged(int)"), self.mTab.reinit)
    # 程序退出
    def closeEvent(self, event):
        reply = QMessageBox.question(self, ' Message ',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = TabWidget()
    myapp.show()
    sys.exit(app.exec_())