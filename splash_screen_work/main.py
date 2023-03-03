from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys

from ui_main import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen
from circular_progress_folder import CircularProgress

counter = 0

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # removing title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #  import circular progress
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
        self.timer = QTimer()
        self.timer.timeout.connect(self.update) # creating a update function
        self.timer.start(25) # change the speed of the timer

        self.show()

    # update function created
    def update(self):
        global counter
        self.progress.set_value(counter)
        #  stoping the counter after 100 % 
        if counter >= 100:
            self.timer.stop()
            self.main = MainWindow()
            self.main.show()

            # closing the splash screen after main window is created
            self.close()

        counter += 1

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