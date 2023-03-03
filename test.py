import subprocess
import torch
import os

model_path = os.path.join(os.getcwd(), 'V2_YOLOv5Character-20230224T134754Z-001', 'YOLOv5Character', 'yolov5', 'runs', 'train', 'exp3', 'weights', 'best.pt')
model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)  # custom trained model


print("****************************************************************")
for name, param in model.named_parameters():
    print(f'{name} ({param.numel()})')
# Start the YOLOv5 subprocess and capture its output
# command = "dir"
# output = subprocess.check_output(command, shell=True, text=True)
# print(output)
# Read the output line by line and print it
