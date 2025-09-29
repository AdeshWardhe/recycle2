# UPLOAD_FOLDER = r"uploads"
# YOLO_MODEL_PATH = r"yolov5\runs\train\exp\weights\best.pt"
# EXCEL_FILE = r"uploads_updated_extended.xlsx"
# weights_path = r"yolov5\runs\train\exp\weights\best.pt"
# DETECT_SCRIPT = r"yolov5\detect.py"
# STATIC_IMAGE_PATH = r"static/after.png"
# DETECT_RESULTS_DIR = r"yolov5\runs\detect"



import os
from huggingface_hub import hf_hub_download

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Paths & Directories ===

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Automatically download YOLOv5 trained model from Hugging Face (if not cached)
YOLO_MODEL_PATH = hf_hub_download(
    repo_id="adeshwardhe/recycle2-yolov5",
    filename="best.pt"
)

EXCEL_FILE = os.path.join(BASE_DIR, "uploads_updated_extended.xlsx")
DETECT_SCRIPT = os.path.join(BASE_DIR, r"yolov5", "detect.py")
STATIC_IMAGE_PATH = os.path.join(BASE_DIR, "static", "after.png")
DETECT_RESULTS_DIR = os.path.join(BASE_DIR, r"yolov5", "runs", "detect")

# === Backward Compatibility ===
# Keep old variable name so existing code (app1.py) does not break
weights_path = YOLO_MODEL_PATH

