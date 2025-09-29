import os
import pathlib

# Convert PosixPath to WindowsPath if running on Windows
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath

# Run YOLOv5 detection
command = "python detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.5 --source test_images/mouse1.jpg"
os.system(command)
