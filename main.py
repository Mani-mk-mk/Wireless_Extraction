import os
import sys
import shutil

import torch
import csv
import numpy as np
import pandas as pd

from threads.upload_thread import WorkerThread
from threads.frames_thread import FramesThread
from threads.detection_thread import DetectionThread

from PyQt5 import Qt, QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, QPropertyAnimation, QFileSystemWatcher
from PyQt5.QtWidgets import QLabel, QApplication, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QPushButton, QFrame, QWidget, QMainWindow, QGridLayout, QStackedWidget, QDesktopWidget
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
        print(f"{self.screen_width}x{self.screen_height}")
        self.setWindowTitle("Wireless Extraction")
        self.frames_directory = os.path.join(os.getcwd(), 'frames')
        self.model_path = os.path.join(os.getcwd(), 'V2_YOLOv5Character-20230224T134754Z-001', 'YOLOv5Character', 'yolov5', 'runs', 'train', 'exp3', 'weights', 'best.pt')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', self.model_path)  # custom trained model
        
        #pages
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
        
        self.home_button = self.findChild(QPushButton, 'home_button')
        self.history_button = self.findChild(QPushButton, 'history_button')
        self.guidelines_button = self.findChild(QPushButton, 'guidelines_button')
        self.settings_button = self.findChild(QPushButton, 'settings_button')
        self.about_button = self.findChild(QPushButton, 'info_button')
        self.signout_button = self.findChild(QPushButton, 'signout_button')
        
        self.home_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.home_page_index))
        self.history_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.history_page_index))
        self.guidelines_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.guidelines_page_index))
        self.settings_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.settings_page_index))
        self.about_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.about_page_index))
        self.signout_button.clicked.connect(lambda: self.page_controller.setCurrentIndex(self.signout_page_index))
        
        #toggle button
        self.toggle_button = self.findChild(QPushButton, 'toggle_button')
        
        self.toggle_button.clicked.connect(self.toggle_menu)
        
        
        #Sidebar
        self.sidebar = self.findChild(QFrame, 'side_bar')
                
        #homepage
        self.connect_ip_button = self.findChild(QPushButton, 'ipcam_button')
        self.upload_button = self.findChild(QPushButton, 'upload_button')
        
        self.frame_image = self.findChild(QLabel, 'frame_image')
        self.video_info = self.findChild(QLabel, 'video_info')
        
        self.detection_table = self.findChild(QTableWidget, 'detected_values')
        
        self.connect_ip_button.clicked.connect(self.connect_ipcam)
        self.upload_button.clicked.connect(self.upload)
        
    def connect_ipcam(self):
        #flow
        #Once clicked we have to use the threaded_queue written by Ajay
        #We have to change the page number
        #Show if the frame is proper then start annotations
        #Apart from this one thing we need to do is use the annoying table widget
        # which god knows why everyone want 
        print("Ip button camera clicked")
        
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
        self.detection_table.setRowCount(15)
        self.watcher = QFileSystemWatcher([r'./predicted.csv'])
        self.watcher.fileChanged.connect(self.update_table)

        #start new thread for detection
        
    def update_table(self):
        with open('predicted.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)[-15:]

        # Clear table widget
        self.detection_table.setRowCount(0)

        # Add rows to table widget
        for i, row in enumerate(rows):
            self.detection_table.insertRow(i)
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(col)
                self.detection_table.setItem(i, j, item)

        # If CSV file has less than 15 entries, add new entries one by one
        if len(rows) < 15:
            with open('predicted.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                all_rows = list(reader)
                new_rows = all_rows[-(15-len(rows)):]
                for i, row in enumerate(new_rows):
                    self.detection_table.insertRow(len(rows)+i)
                    for j, col in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(col)
                        self.detection_table.setItem(len(rows)+i, j, item)                
        
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
