import random
import sys

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon


class MyApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        with open("conf/namelist.txt", "r", encoding='utf-8') as f:
            self.name_list = f.read().splitlines()
        self.App()

    def App(self):
        # 设置主体框架

        #设置窗体名字
        self.setWindowTitle('点名系统')
        #设置窗体大小
        self.resize(1000, 600)

        # 设置字体大小
        self.font = QtGui.QFont()
        self.font.setPointSize(23)

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

    def setname_image(self):
        #点名系统
        name = self.name_list[random.randint(0, len(self.name_list) - 1)]
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
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setname_image)
        self.timer.start(50) #图片播放的时间

    # 程序结束
    def stop(self):
        self.start_music.stop()
        self.end_music.play()
        self.timer.stop()

    # 程序退出
    def closeEvent(self, event):
        reply = QMessageBox.question(self, ' Message ',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    #设置按钮解禁
    def btnsetenabled(self,btn):
        # print(btn.isEnabled()) False
        # 按下按钮后解除禁止可以继续点击
        btn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())