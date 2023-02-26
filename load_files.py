import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow,  QPushButton
from PyQt5 import uic
import os
import shutil
import cv2
import numpy as np


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()   
        uic.loadUi("design.ui", self)
        
        #Defining the three buttons used in home section
        self.connect_ip_button = self.findChild(QPushButton, 'connect_ip_button')
        self.load_video_button = self.findChild(QPushButton, 'load_video_button')
        self.load_image_button = self.findChild(QPushButton, 'load_image_button')
        self.frames_directory = os.path.join(os.getcwd(), 'frames')
        
        # directory connection
        self.load_video_button.clicked.connect(self.load_directory)
                
        self.show()

    # Loading the file dialog box
    def load_directory(self):
        # home path 
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser("~"), "Video Files (*.mp4; *.mkv)")
        print(path)
        self.create_frames(path)
        # self.filename.setText(path)
    
    def create_frames(self, file_path):
        file_name = file_path.split("/")[-1]
        file_name = file_name.split(".")[0]
        directory = os.path.join(self.frames_directory, file_name)
        #If the directory already exists then delete it 
        #Else create it and populate it with frames
        if (os.path.isdir(directory)):
            shutil.rmtree(directory)
        os.makedirs(directory)
        #Populating frames
        capture = cv2.VideoCapture(file_path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        counter = 0
        
        while True:
            success, frame = capture.read()
            if not success:
                break
            counter += 1
            # Deleting low resolution frame
            if np.mean(frame) < 25:
                print("Removed the frame")
                continue
            resized_frame = cv2.resize(frame, (960, 960))
            cv2.imwrite(os.path.join(directory, f'{counter/fps}.jpg'), resized_frame)
        capture.release()
        return
        
    
app = QApplication(sys.argv)
UIWindow = UI()
sys.exit(app.exec_())
