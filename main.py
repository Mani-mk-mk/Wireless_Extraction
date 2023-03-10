import os
import sys

import torch
import csv
import cv2

from threads.upload_thread import WorkerThread
from threads.frames_thread import FramesThread
from threads.detection_thread import DetectionThread
from threads.ip_thread import IpThread

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPropertyAnimation, QFileSystemWatcher
from PyQt5.QtWidgets import QLabel, QApplication, QFileDialog, QTableWidget
from PyQt5.QtWidgets import QPushButton, QFrame, QMainWindow, QStackedWidget, QDesktopWidget
from PyQt5 import uic
from ui import resources

#Comment out the below line in case you are running the filef for first time
# os.system("Pyrcc5 ./ui/resources.qrc -o ./ui/resources.py")

class WirelessExtraction(QMainWindow):
    def __init__(self):
        super(WirelessExtraction, self).__init__() 
        uic.loadUi("./ui/interface.ui", self)
        screen = QDesktopWidget().screenGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.output_path = os.path.join(os.getcwd(), 'output', 'predictions.csv')
        self.realtime_path = os.path.join(os.getcwd(), 'output', 'realtime-predictions.csv')
        print(f"{self.screen_width}x{self.screen_height}")
        self.setWindowTitle("Wireless Extraction")
        self.frames_directory = os.path.join(os.getcwd(), 'frames')
        self.model_path = os.path.join(os.getcwd(), 'V2_YOLOv5Character-20230224T134754Z-001', 'YOLOv5Character', 'yolov5', 'runs', 'train', 'exp3', 'weights', 'best.pt')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', self.model_path)  # custom trained model
        
        #pages index
        self.page_controller = self.findChild(QStackedWidget, 'page_controller')
        self.home_page_index = 0
        self.history_page_index = 1
        self.guidelines_page_index = 2
        self.settings_page_index = 3
        self.about_page_index = 4
        self.signout_page_index = 5
        
        self.home_page_controller = self.findChild(QStackedWidget, 'home_page_controller')
        self.connect_ip_index = 1
        self.upload_page_index = 2
        
        self.detection_page_controller = self.findChild(QStackedWidget, 'detection_controller')
        self.tables_page_index = 1
        
        self.home_menu_button = self.findChild(QPushButton, 'home_button')
        self.history_menu_button = self.findChild(QPushButton, 'history_button')
        self.guidelines_menu_button = self.findChild(QPushButton, 'guidelines_button')
        self.setting_menu_button = self.findChild(QPushButton, 'settings_button')
        self.about_menu_button = self.findChild(QPushButton, 'info_button')
        self.signout_menu_button = self.findChild(QPushButton, 'signout_button')
        
        self.home_menu_button.clicked.connect(self.go_to_home)
        self.history_menu_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.history_page_index))
        self.guidelines_menu_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.guidelines_page_index))
        self.setting_menu_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.settings_page_index))
        self.about_menu_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.about_page_index))
        self.signout_menu_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.signout_page_index))
        
        #toggle button
        self.toggle_menu_button = self.findChild(QPushButton, 'toggle_button')
        
        self.toggle_menu_button.clicked.connect(self.toggle_menu)
        
        
        #Sidebar
        self.sidebar = self.findChild(QFrame, 'side_bar')
                
        #homepage
        self.connect_ip_button = self.findChild(QPushButton, 'ipcam_button')
        self.upload_button = self.findChild(QPushButton, 'upload_button')
        
        self.frame_image = self.findChild(QLabel, 'frame_image')
        self.video_info = self.findChild(QLabel, 'video_info')
        
        self.ip_window_label = self.findChild(QLabel, 'ip_window')    
        
        self.detection_table = self.findChild(QTableWidget, 'detected_values')
        self.detection_table.setStyleSheet("font: 11pt 'Seoge UI'")
        self.detection_table.setStyleSheet("QTableView::item:selected { background-color: #0078d7; color: #fff; }")
        self.detection_table.setAlternatingRowColors(True)
        self.detection_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
        self.realtime_detection_table = self.findChild(QTableWidget, 'realtime_table')
        
        self.connect_ip_button.clicked.connect(self.connect_ipcam)
        self.upload_button.clicked.connect(self.upload)
        
        self.start_detection_ip = self.findChild(QPushButton, 'start_detection_camera')
        self.stop_processing_button = self.findChild(QPushButton, 'stop_processing')
        self.go_back_detection = self.findChild(QPushButton, 'go_back_camera')
        
        self.start_detection_ip.clicked.connect(self.start_detection_realtime)
        self.stop_processing_button.clicked.connect(self.stop_processing_ipcam)
        self.go_back_detection.clicked.connect(self.go_back)
        
    def __contains__(self, attribute):
        return hasattr(self, attribute)


    def start_detection_realtime(self):
        self.detection_page_controller.setCurrentIndex(self.tables_page_index)
        self.ipcam_thread.start_detection()
        # with open("realtime_predicted.csv", "w"):
        #     pass
        self.ip_watcher = QFileSystemWatcher([self.realtime_path])
        self.ip_watcher.fileChanged.connect(lambda: self.update_table(self.realtime_path, self.realtime_detection_table))
        
        
    def stop_processing_ipcam(self):
        self.ipcam_thread.stop()
        
    def go_to_home(self):
        self.page_controller.setCurrentIndex(self.home_page_index)
        self.home_page_controller.setCurrentIndex(self.home_page_index)
        
    def connect_ipcam(self):
        self.home_page_controller.setCurrentIndex(1)
        print("Ip button camera clicked")
        self.ipcam_thread = IpThread(self.model, stream_id='rtsp://192.168.0.105:8000/h264_pcm.sdp')
        self.ipcam_thread.new_frame.connect(self.update_frame)
        self.ipcam_thread.start()
        
    def go_back(self):
        #Stop the ipcam_thread
        #this method not working need to do something
        if hasattr(self, 'ipcam_thread'):
            self.ipcam_thread.exit()
        else: 
            print("No thread of IP camera exists!")
        
        self.ip_window_label.clear()
        self.go_to_home()
        
    
    def update_frame(self, frame):
        # Convert BGR frame to RGB format for displaying in QLabel
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create QImage from numpy array
        h, w, c = frame.shape
        bytesPerLine = c * w
        qImg = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        # Display QImage in QLabel
        self.ip_window_label.setPixmap(QtGui.QPixmap.fromImage(qImg))   
        self.ip_window_label.setScaledContents(True) 
    
    def upload(self):
        print("Upload button clicked")
        self.load_directory()
        
    def load_directory(self):
        # home path
        self.home_page_controller.setCurrentIndex(self.upload_page_index) 
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser("~"), "Video Files (*.mp4; *.mkv)")
        ## Setting video info
        self.worker_thread = WorkerThread(path)
        # connect worker thread signals to slots in main thread
        self.worker_thread.video_info_ready.connect(self.update_video_info_label)
        self.worker_thread.frame_image_ready.connect(self.update_frame_image_label) 
        self.worker_thread.start()
        self.frames_thread = FramesThread(path)
        self.frames_thread.frames_ready.connect(self.start_detections)
        self.frames_thread.start()
        
        
    def update_video_info_label(self, info):
        self.video_info.setText(info)

    def update_frame_image_label(self, image):
        self.frame_image.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def start_detections(self, data):
        if data[0]:
            path = data[1]
            print(path)
            self.detector_thread = DetectionThread(path, self.model)
            self.detector_thread.start()
        # self.detection_table.setRowCount(15)
        self.watcher = QFileSystemWatcher([self.output_path])
        self.watcher.fileChanged.connect(lambda: self.update_table(self.output_path, self.detection_table))

        #start new thread for detection
        
    def update_table(self, filename, table):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        # Clear table widget
        table.setRowCount(0)

        # Add rows to table widget
        for i, row in enumerate(rows):
            table.insertRow(i)
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(col)
                table.setItem(i, j, item)
                # self.detection_table.setColumnWidth(j, -1)
        
    def toggle_menu(self):
        sidebar_width = self.sidebar.width()
        updated_width = 200 if sidebar_width == 55 else 55
        
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(sidebar_width)
        self.animation.setEndValue(updated_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WirelessExtraction()
    w.show()
    sys.exit(app.exec_())
