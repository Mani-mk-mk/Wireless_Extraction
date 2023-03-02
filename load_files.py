import sys
import os
import shutil

import torch
import cv2
import csv
import numpy as np
import pandas as pd

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QApplication, QFileDialog
from PyQt5.QtWidgets import QPushButton, QWidget, QMainWindow, QGridLayout
from PyQt5 import uic


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()   
        uic.loadUi("updated_design.ui", self)
        
        #Defining the three buttons used in home section
        self.w = None
        self.ipcam_window = self.findChild(QLabel, 'ipcam_window')
        self.connect_ip_button = self.findChild(QPushButton, 'connect_ip_button')
        self.load_video_button = self.findChild(QPushButton, 'load_video_button')
        # self.load_image_button = self.findChild(QPushButton, 'load_image_button')
        self.frames_directory = os.path.join(os.getcwd(), 'frames')
        self.loading_text = "Creating Frames..."
        
        # directory connection
        self.connect_ip_button.clicked.connect(self.connect_ip)
        self.load_video_button.clicked.connect(self.load_directory)
        
        #Yolo_v5 model
        self.model_path = os.path.join(os.getcwd(), 'V2_YOLOv5Character-20230224T134754Z-001', 'YOLOv5Character', 'yolov5', 'runs', 'train', 'exp3', 'weights', 'best.pt')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', self.model_path)  # custom trained model

                
        # self.show()
        
    def connect_ip(self):
        ip = 'http://192.168.0.105:8000/video'
        capture = cv2.VideoCapture(ip)

        while True:
            flag, frame = capture.read()
            try:
                # frame = cv2.resize(frame, (840, 420))
                image = QtGui.QImage(
                    frame,
                    frame.shape[1],
                    frame.shape[0],
                    frame.shape[1] * 3,
                    QtGui.QImage.Format_RGB888
                )       
                self.ipcam_window.setPixmap(QtGui.QPixmap.fromImage(image))
            except:
                capture.release()
                raise
            
            if cv2.waitKey(1) & 0xFF == ord('q') :
                break
            
        capture.release()
        cv2.destroyAllWindows()

        # import cv2
        #     "http://ajay:aju13@192.168.0.101:8080/video?type=.mjpg")
        # ip = f'http://{username}:{password}192.168.0.101:8000/video'

    # Loading the file dialog box
    def load_directory(self):
        # home path 
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser("~"), "Video Files (*.mp4; *.mkv)")
        print(path)
        self.create_frames(path)
        # self.filename.setText(path)
    
    def create_frames(self, file_path):
        # self.ipcam_window.setText(self.loading_text)
        print("Creating frames...")
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
            # resized_frame = cv2.resize(frame, (960, 960))
            cv2.imwrite(os.path.join(directory, f'{counter/fps}.jpg'), frame)
        capture.release()
        # self.ipcam_window.setText("")
        print(f"{counter} frames created successfully!")
        self.detect_frames(directory)
        return
    
    def detect_frames(self, path):
        print("Detecting frames...")
        frames_directory = os.listdir(path=path)
        self.model.conf=0.50
        self.model.iou=0.05
        self.model.multi_label = False
        self.model.max_det = 18
        timestamps = []
        region1 = []
        region2 = []
        region3 = []
        region4 = []
        
        for counter, image in enumerate(frames_directory):
            if counter  == 85:
                print(f"{counter} images detection completed")
                break
            prediction = self.model(os.path.join(path, image), size=960)

            #Sort predicted bounding boxes based on the values of x coordinate of the boxes
            output_table = prediction.pandas().xyxy[0].sort_values('xmin')  # im predictions (pandas)
            temp_output = pd.DataFrame(output_table)
            temp_output.to_csv("./output/test_dataset.csv")
            
            temp_output = pd.read_csv("./output/test_dataset.csv")
            size_of_table = temp_output['class'].size

            # Logic Combine digits to create a single valued number
            result = ["", "", "", ""]
            c = 0
            digits = []

            index1=0
            index2=0
            index3=0

            for i in range(size_of_table-1):
                digits.append(temp_output['class'][i])

            # print("Done")

            max_dist = 0
            for i in range(size_of_table-1):
                if(temp_output['xmin'][i+1] - temp_output['xmax'][i] > max_dist):
                    max_dist = temp_output['xmin'][i+1] - temp_output['xmax'][i]
                    index2 = i;

            i=0
            while (i < index2):
                if(temp_output['xmin'][index2] - temp_output['xmax'][i] > 0.34*max_dist):
                    index1 = i;
                i += 1
            # print("Done")

            i = size_of_table-1
            while (i > index2):
                if(temp_output['xmin'][i] - temp_output['xmax'][index2] > 1.125*max_dist):
                    index3 = i;
                i -= 1
            # print("Done")

            i = 0
            c = 0
            while (i<=index1):
                result[c] = result[c] + str(temp_output['class'][i])
                i += 1
            # print("Done")

            c = 1
            while (i<=index2):
                result[c] = result[c] + str(temp_output['class'][i])
                i += 1
            # print("Done")

            c = 2
            while (i<=index3):
                result[c] = result[c] + str(temp_output['class'][i])
                i += 1
            # print("Done")

            c = 3
            while (i<size_of_table):
                result[c] = result[c] + str(temp_output['class'][i])
                i += 1
                
            field_names = ['File_name', 'Display_1', 'Display_2', 'Display_3', 'Display_4']
            # print(result)
            timestamps.append(image.split('.')[0])
            region1.append(result[0])
            region2.append(result[1])
            region3.append(result[2])
            region4.append(result[3])
            
            # dict = {"File_name": image, "Display_1":result[0], "Display_2":result[1], "Display_3":result[2], "Display_4":result[3]}
            # with open('./output/Predicted_Values.csv', 'a') as csv_file:
            #     dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 

            #     dict_object.writerow(dict)

        #     region_01.append(result[0])
        #     region_02.append(result[1])
        #     region_03.append(result[2])
        #     region_04.append(result[3])
        output = pd.DataFrame(data={'Timestamps': timestamps, 'Region-01': region1, 'Region-02': region2, 'Region-03': region3, 'Region-04': region4})
        output.to_csv("./output/test_dataset.csv", index=False)
        print("Detection completed successfully!")


    
    
app = QApplication(sys.argv)
# UIWindow = UI()
w = UI()
w.show()
sys.exit(app.exec_())
