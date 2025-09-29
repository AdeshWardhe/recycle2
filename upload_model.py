import os
from huggingface_hub import HfApi

# Get base directory (same as your config file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to your trained YOLOv5 model
YOLO_MODEL_PATH = os.path.join(BASE_DIR, r"yolov5\runs\train\exp\weights\best.pt")

# Check if file exists before uploading
if not os.path.exists(YOLO_MODEL_PATH):
    raise FileNotFoundError(f"❌ best.pt not found at {YOLO_MODEL_PATH}")

# Upload to Hugging Face
api = HfApi()
api.upload_file(
    path_or_fileobj=YOLO_MODEL_PATH,             # Your local model
    path_in_repo="best.pt",                      # How it will be named on HF
    repo_id="adeshwardhe/recycle2-yolov5",       # Your HF model repo
    repo_type="model"
)

print(f"✅ best.pt uploaded successfully from {YOLO_MODEL_PATH} to Hugging Face!")
