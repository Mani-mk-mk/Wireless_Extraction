# importing required libraries
import cv2
from threading import Thread  # library for implementing multi-threaded processing
import queue
import numpy as np

#importing required libraries for YOLO Implementation
import torch
import os
import pandas as pd
import csv

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

class IpThread(QThread):
    new_frame = pyqtSignal(np.ndarray)
    detection_completed = pyqtSignal(bool)
    def __init__(self, model, stream_id = 0):
        super().__init__()
        self.stream_id = stream_id
        self.model = model
        self.stopped = True
        self.output_path = os.path.join(os.getcwd(), 'output', 'realtime-predictions.csv')
        print(self.output_path)
        self.test_path = os.path.join(os.getcwd(), '.intermediate', 'test_dataset.csv')
        self.start_detections = False    
    
    def run(self):
        self.q = queue.Queue()
        self.vcap = cv2.VideoCapture(self.stream_id)
        # self.vcap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))
        print("FPS of webcam hardware/input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
            
        while True:
            ret, self.frame = self.vcap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                    # print('emptying the queue')
                except queue.Empty:
                    print("empty")
            self.q.put(self.frame)
            self.new_frame.emit(self.frame)
            if self.start_detections:
                self.detect_digits()
    
    def start_detection(self):
        self.start_detections = True        
            
    def read(self):
        return self.q.get()
    
    def stop(self):
        self.stopped = True
        self.wait()
        
    def detect_digits(self):
        print("Detection module starting...")
        # frames_processed = 0
        # while self.stopped:
        self.captured_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        # cv2.imwrite("frame_folder/frame"+str(frames_processed)+".jpg", self.captured_frame)
        result = self.model(self.captured_frame, size=960)
        print(result)

        output_table = result.pandas().xyxy[0].sort_values('xmin')  # im predictions (pandas)
        temp_output = pd.DataFrame(output_table)
        temp_output.to_csv(self.test_path)

        temp_output = pd.read_csv(self.test_path)
        size_of_table = temp_output['class'].size

        field_names = ['Display_1', 'Display_2', 'Display_3', 'Display_4']
        if (size_of_table == 0):

        # If there are no digits present in the image
        # (i.e. if there are no custom object's present in the image).

        ## CSV sheet to write NA if no digits present in the image.

            print("No Digits detected.")
            dict = {"Display_1":"NA", "Display_2":"NA", "Display_3":"NA", "Display_4":"NA"}
            with open('realtime_predicted.csv', 'a', newline='') as csv_file:
                dict_object = csv.DictWriter(csv_file, fieldnames=field_names)
        else:
            self._extracted_from_detect_digits_30(size_of_table, temp_output, field_names)

    # TODO Rename this here and in `detect_digits`
    def _extracted_from_detect_digits_30(self, size_of_table, temp_output, field_names):
        result = ["", "", "", ""]
        c = 0
        digits = []

        index1=0
        index2=0
        index3=0

        for i in range(size_of_table-1):
            digits.append(temp_output['class'][i])


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

        i = size_of_table-1
        while (i > index2):
            if(temp_output['xmin'][i] - temp_output['xmax'][index2] > 1.125*max_dist):
                index3 = i;
            i -= 1

        i = 0
        c = 0
        while (i<=index1):
            result[c] = result[c] + str(temp_output['class'][i])
            i += 1

        c = 1
        while (i<=index2):
            result[c] = result[c] + str(temp_output['class'][i])
            i += 1

        c = 2
        while (i<=index3):
            result[c] = result[c] + str(temp_output['class'][i])
            i += 1

        c = 3
        while (i<size_of_table):
            result[c] = result[c] + str(temp_output['class'][i])
            i += 1

        dict = {"Display_1":result[0], "Display_2":result[1], "Display_3":result[2], "Display_4":result[3]}
        with open(self.output_path, 'a', newline='') as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
            dict_object.writerow(dict)


        # self.detect_digits.emit(True)


