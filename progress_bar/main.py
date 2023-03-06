
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

### UI_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CircularProgress(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # custome parameters
        self.value = 0
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = 0xff79c6
        self.max_value = 100
        #  text
        self.enable_text = True
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = 0xff79c6
        # bg
        self.enable_bg = True
        self.bg_color = 0x44475a

        # self.enable_shadow = True

        # set default size without layout
        self.resize(self.width, self.height)

    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0,0,0,80))
            self.setGraphicsEffect(self.shadow) 

    def set_value(self, value):
        self.value = value
        self.repaint() # render progress bar after change value

    #  paint event (design for circular progress)
    def paintEvent(self, event):
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width // 2
        value = self.value * 360 // self.max_value

        # painter
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setFont(QFont(self.font_family, self.font_size))

        # rectangle
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        # pen
        pen = QPen()
        pen.setWidth(self.progress_width)

        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        # enable bg
        if self.enable_bg:
            pen.setColor(QColor(self.bg_color))
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        # create arc
        pen.setColor(QColor(self.progress_color))
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        #  create text
        if self.enable_text:
            self._extracted_from_paintEvent_38(pen, paint, rect)
        self._extracted_from_paintEvent_38(pen, paint, rect)
        paint.end()

    # TODO Rename this here and in `paintEvent`
    def _extracted_from_paintEvent_38(self, pen, paint, rect):
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        paint.drawText(rect, Qt.AlignCenter, f'{self.value}{self.suffix}')



class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(300, 300)
        SplashScreen.setMinimumSize(QtCore.QSize(300, 300))
        SplashScreen.setMaximumSize(QtCore.QSize(300, 300))
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container = QtWidgets.QFrame(self.centralwidget)
        self.container.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container.setObjectName("container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.container)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.circle_bg = QtWidgets.QFrame(self.container)
        self.circle_bg.setStyleSheet("QFrame {\n"
"    background-color: #282a36;\n"
"    color: #f8f8f2;\n"
"    border-radius: 120px;\n"
"    font: 9pt \"Segoe UI\";\n"
"\n"
"}")
        self.circle_bg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.circle_bg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.circle_bg.setObjectName("circle_bg")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.circle_bg)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.texts = QtWidgets.QFrame(self.circle_bg)
        self.texts.setMinimumSize(QtCore.QSize(0, 80))
        self.texts.setMaximumSize(QtCore.QSize(16777215, 180))
        self.texts.setStyleSheet("background: none;")
        self.texts.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.texts.setFrameShadow(QtWidgets.QFrame.Raised)
        self.texts.setObjectName("texts")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.texts)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.title = QtWidgets.QLabel(self.texts)
        self.title.setMinimumSize(QtCore.QSize(0, 30))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 0, 0, 1, 1)
        self.empty = QtWidgets.QFrame(self.texts)
        self.empty.setMinimumSize(QtCore.QSize(0, 60))
        self.empty.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.empty.setFrameShadow(QtWidgets.QFrame.Raised)
        self.empty.setObjectName("empty")
        self.gridLayout.addWidget(self.empty, 1, 0, 1, 1)
        self.loading = QtWidgets.QLabel(self.texts)
        self.loading.setStyleSheet("QLabel {\n"
"    font-size: 12px;\n"
"}")
        self.loading.setAlignment(QtCore.Qt.AlignCenter)
        self.loading.setObjectName("loading")
        self.gridLayout.addWidget(self.loading, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.texts)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.version = QtWidgets.QLabel(self.frame)
        self.version.setMinimumSize(QtCore.QSize(100, 24))
        self.version.setMaximumSize(QtCore.QSize(100, 24))
        self.version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.version.setStyleSheet("QLabel {\n"
"    font: 9pt \"Segoe UI\";\n"
"    background-color: rgb(68, 71, 90);\n"
"    color: rgb(151, 159, 200);\n"
"    border-radius: 12px;\n"
"    font-size: 12px;\n"
"}")
        self.version.setAlignment(QtCore.Qt.AlignCenter)
        self.version.setObjectName("version")
        self.verticalLayout_5.addWidget(self.version, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.texts)
        self.verticalLayout_2.addWidget(self.circle_bg)
        self.verticalLayout.addWidget(self.container)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "Loading_Bar"))
        self.title.setText(_translate("SplashScreen", "Modern GUI"))
        self.loading.setText(_translate("SplashScreen", "loading..."))
        self.version.setText(_translate("SplashScreen", "v.0.0.1 - Beta 1"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 583)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(40, 42, 54)")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setMinimumSize(QtCore.QSize(0, 30))
        self.title.setStyleSheet("color: rgb(255, 255, 255);")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "MANI WINDOW"))




class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # removing title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #  import circular progress
        self.counter = 0
        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 75
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15, 15)
        self.progress.add_shadow(True)
        self.progress.font_size = 25
        self.progress.bg_color = QColor(68, 71, 90, 140)
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        # adding a drop shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,80))
        self.setGraphicsEffect(self.shadow) 

        # QTimer
        # creating a timer function
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update) # creating a update function
        # self.timer.start(25) # change the speed of the timer
        
        self.show()

    # update function created
    def update(self, value):
        # global counter
        self.progress.set_value(value)
        #  stoping the counter after 100 % 
        # if counter >= 100:
        #     self.timer.stop()
        #     self.main = MainWindow()
        #     self.main.show()

        #     # closing the splash screen after main window is created
        #     self.close()

        # counter += 1

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())


# to add to ur projects : 
# copy the splash screen required functions and classes expect the main function
# copy the folder circular_progress_folder
# copy ui_splash_screen.py
# while running the main function change the change the class function eg: MainWindow() -> SplashScreen() 