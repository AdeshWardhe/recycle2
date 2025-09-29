#python C:\Users\Adesh\Downloads\updated_model\content\yolov5\detect.py --weights C:\Users\Adesh\Downloads\updated_model\content\yolov5\runs\train\exp\weights\best.pt --img 640 --conf 0.7 --source 0
import os
import uuid
import subprocess
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import yaml
import re
import webbrowser
import threading
import time
import config
import folium
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = config.UPLOAD_FOLDER

# YOLO_MODEL_PATH = r"C:\Users\Adesh\Downloads\updated_model\content\yolov5\runs\train\exp\weights\best.pt"

YOLO_MODEL_PATH = config.YOLO_MODEL_PATH

# EXCEL_FILE = 'uploads.xlsx'
EXCEL_FILE = config.EXCEL_FILE


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create uploads folder if not exists

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit file size to 10MB

# Load class names from the YOLO data.yaml file
def load_class_names(yaml_path):
    try:
        with open(yaml_path, "r") as file:
            data = yaml.safe_load(file)
            class_names = data.get("names", [])  # Extract class names as a list
            print(class_names)
            return data.get("names", [])  # Extract class names as a list
    except Exception as e:
        return f"Error loading YAML: {e}"
    
uploaded_files = {}
new_data = []


import glob
import shutil

# STATIC_IMAGE_PATH = "static/after.png"  # Destination for latest image

STATIC_IMAGE_PATH = config.STATIC_IMAGE_PATH

def get_latest_result_image():
    print("running get_latest_result_image function ")
    # detect_results_dir = r"C:\Users\Adesh\Downloads\updated_model\content\yolov5\runs\detect"
    
    detect_results_dir = config.DETECT_RESULTS_DIR

    # Get the latest 'exp' folder
    exp_folders = sorted(glob.glob(os.path.join(detect_results_dir, "exp*")), key=os.path.getmtime, reverse=True)
    
    if not exp_folders:
        return None  # No result folder found
    
    latest_exp_folder = exp_folders[0]  # Most recent detection result folder
    
    # Find image files in the latest exp folder
    result_images = sorted(glob.glob(os.path.join(latest_exp_folder, "*.jpg")), key=os.path.getmtime, reverse=True)
    print("result_images", result_images)

    if result_images:
        latest_image = result_images[0]
        # Copy latest image to 'static/after.png', replacing if it exists
        shutil.copy(latest_image, STATIC_IMAGE_PATH)
        return STATIC_IMAGE_PATH  # Return the path of the copied file
    return None  # No images found



def process_filename(filename):
    print("process_filename activated")
    print("filepath:",filename)
    #filename = "uploads\{filename}"
    # weights_path = r"C:\Users\Adesh\Downloads\updated_model\content\yolov5\runs\train\exp\weights\best.pt"

    weights_path = config.weights_path

    # detect_path = r"C:\Users\Adesh\Downloads\updated_model\content\yolov5\detect.py"

    detect_path = config.DETECT_SCRIPT


    command = [
        "python", detect_path,
        "--weights", weights_path,
        "--img", "640",
        "--conf", "0.5",
        "--source", filename
    ]

    try:
        print("command", command)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        output_text = result.stderr  # Get the stderr output (where YOLO prints detections)

        print("1st output: ",output_text)
        

        # Extract only the line that contains detection results
        detection_line = re.search(r"(?:image|video) \d+/\d+.*?: \d+x\d+ (.*?), \d+\.\d+ms", output_text)
        #print("\n2st output: ",detection_line)
        
        if detection_line:
            detected_objects = detection_line.group(1)  # Get detected objects part only
            print("\nFinal output:",detected_objects)
            return detected_objects  # Return only the detection line
        else:
            return "No objects detected."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

@app.route('/')
def home():
    map_html = create_map()  # Get HTML for map
    return render_template('index.html', map_html=map_html)  # Pass map_html to the template

@app.route('/upload', methods=['POST'])
def upload():
    email = request.form.get('email')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    file = request.files.get('file')

    if not email or not latitude or not longitude:
        return jsonify({"error": "Missing required fields"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Generate unique filename
    ext = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)

    after_image_path = "static/after.png"



    # if os.path.exists(after_image_path):
    #     os.remove(after_image_path)  # Delete the file
    #     print("Image deleted successfully.")
    # else:
    #     print("Image not found.")




    # Print the unique filename in the terminal
    # Detection = "No objects detected."
    # Detection = process_filename(file_path)  # Ensure it's never None

    # print(Detection)
    # print(Detection.type())

    # Store file path globally
    uploaded_files[unique_filename] = file_path  # Use filename as key

    # Determine file type
    file_type = "image" if ext.lower() in ["jpg", "jpeg", "png", "gif"] else "video"

    # Save details to an XLSX file
    new_data = pd.DataFrame([{
        "Email": email,
        "Longitude": longitude,
        "Latitude": latitude,
        "Filename": unique_filename,
        "File Path": file_path,
        "File Type": file_type
    }])

    if os.path.exists(EXCEL_FILE):
        existing_data = pd.read_excel(EXCEL_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_excel(EXCEL_FILE, index=False)

    return jsonify({
        "message": "File uploaded successfully",
        "email": email,
        "latitude": latitude,
        "longitude": longitude,
        "filename": unique_filename,
        "file_path": file_path,
        "file_type": file_type
    })


@app.route('/detect', methods=['POST'])
def get_detection_result():
    print("running get_detection_result()")
    filename = request.json.get('filename')  # Expect filename from frontend

    if not filename or filename not in uploaded_files:
        print("Error: Invalid or missing filename")
        return jsonify({"error": "Invalid or missing filename"}), 400

    if not os.path.exists(EXCEL_FILE):
        print("Error: No uploaded files found")
        return jsonify({"error": "No uploaded files found"}), 404

    file_path = uploaded_files[filename]  # Get full path
    print("Filepath:", file_path)

    df = pd.read_excel(EXCEL_FILE)
    print("Reading XLSX File")

    row_index = df[df["Filename"] == filename].index
    if row_index.empty:
        print("Error: File not found in Excel")
        return jsonify({"error": "File not found"}), 404

    file_path = df.loc[row_index[0], "File Path"]
    detection_result = process_filename(file_path)  # Run object detection

    #adesh_output = get_latest_result_image()
   


    # Class name mappings
    class_names = {
        "keyboard": "keyboard",
        "mouse": "mouse",
        "mouses": "mouse",
        "battery": "battery",
        "batteries": "battery",
        "processor_and_memory": "processor_and_memory",
        "processor": "processor_and_memory",
        "processors": "processor_and_memory",
        "memory": "processor_and_memory",
        "chip": "processor_and_memory",
        "processorandmemory": "processor_and_memory",
        "chips": "processor_and_memory"
    }

    # Function to extract class name
    def extract_class_name(detection):
       # print("words", words)
        print("class_names", class_names)
        words = detection.lower().split()
        for word in words:
          #  print("word", word)
            word = ''.join(filter(str.isalpha, word))
            if word in class_names:
                return class_names[word]
        return "unknown"
    

    detection_class = extract_class_name(detection_result)

    # Define links per class
    class_links = {
        "keyboard": [
            "https://www.youtube.com/watch?v=74lK33H2nm0",
            "https://www.youtube.com/watch?v=z5BwtujxKvc",
            "https://www.recyclart.org/10-creative-ways-of-upcycling-keyboard-keys/",
            "https://sustainablog.org/articles/recycling-computer-keyboard/",
        ],
        "mouse": [
            "https://www.youtube.com/watch?v=BGewoL3FY5M",
            "https://www.reddit.com/r/upcycling/comments/g1u95b/any_ideas_what_to_do_with_an_old_keyboard/",
            "https://www.pinterest.com/ellaandboomer/keyboard-repurposing/",
            "https://www.treehugger.com/ways-recycle-and-reuse-computer-mice-5192562",
            
            
        ],
        "battery": [
            "https://www.vox.com/technology/389775/ewaste-electronics-recycling-tech",
            "https://www.epa.gov/recycle/used-lithium-ion-batteries",
            "https://www.call2recycle.org/recycling-locations/",
            "https://www.batteryrecycling.com/",
        ],
        "processor_and_memory": [
            "https://www.rts.com/blog/the-complete-e-waste-recycling-process/",
            "https://www.ft.com/content/1ca28611-5ed7-4b58-bfe3-37dc84d321a9",
            "https://www.youtube.com/watch?v=zU62hh3DBfg",
            "https://www.ifixit.com/News/41580/how-to-recycle-e-waste-the-right-way"
        ],
        "unknown": [
            "https://www.hummingbirdinternational.net/turn-ewaste-eco-friendly-upcycle/",
            "https://www.earth911.com/eco-tech/how-to-recycle-old-electronics/",
            "https://www.npr.org/sections/alltechconsidered/2013/11/15/245873127/recycling-electronics-what-to-do-with-your-old-laptops-phones-tablets",
            "https://www.epa.gov/recycle/electronics-donation-and-recycling",
        ]
    }

    # Get relevant links based on detection class
    relevant_links = class_links.get(detection_class, class_links["unknown"])

    # Save detection info back to Excel
    df.at[row_index[0], "Detection"] = detection_result
    df.at[row_index[0], "Detection Class"] = detection_class
    df.to_excel(EXCEL_FILE, index=False)

    print("Detection:", detection_result)
    print("Detection Class:", detection_class)
    print("Relevant Links:", relevant_links)


    return jsonify({
        "filename": filename,
        "detection": detection_result,
        "detection_class": detection_class,
        "links": relevant_links
        
    })

@app.route('/get-latest-image')
def get_latest_image():
    # Replace this logic with how you determine the latest image
    global latest_image_inmail
    latest_image = get_latest_result_image()
    latest_image_inmail = latest_image
    print("detection image path:",latest_image)
    if latest_image:  # Ensure image_path is not None
        if os.path.exists(latest_image):
            # return jsonify({"image_url": "/" + latest_image})  # Return image path
            return jsonify({"image_url": "/static/after.png"}) # <--- THIS IS THE FIX
        else:
            return jsonify({"error": "Image file not found"}), 404  # Image path exists, but file is missing
    return jsonify({"image_url": r"static\after.jpg"})  # Default image if no new image



import folium
from folium import IFrame
import pandas as pd


def create_map():
    df = pd.read_excel(EXCEL_FILE)
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Create base map
    m = folium.Map(location=[df['Latitude'].iloc[-1], df['Longitude'].iloc[-1]], zoom_start=12)

    # Define color mapping
    color_map = {
        "keyboard": "blue",
        "mouse": "black",
        "battery": "green",
        "processor_and_memory": "orange"
    }

    for _, row in df.iterrows():
        detection = str(row['Detection Class']).strip().lower()
        color = color_map.get(detection, "gray")  # fallback to gray if unknown

        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Detection: {row['Detection Class']}<br>Email: {row['Email']}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    return m._repr_html_()



from flask import render_template_string

@app.route('/show_map')
def show_map():
    map_html = create_map()  # Get HTML for map
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Map View</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                #map { height: 100vh; width: 100%; }
            </style>
        </head>
        <body>
            <div id="map">
                {{ map_html|safe }}
            </div>
        </body>
        </html>
    """, map_html=map_html)



@app.route('/get-emails')
def get_emails():
    df = pd.read_excel(EXCEL_FILE)
    df = df.dropna(subset=['Email'])
    df = df[::-1]  # Reverse the DataFrame to show latest first
    emails = df['Email'].tolist()
    return jsonify(emails)

from flask_mail import Mail, Message


# Flask config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'wardehadesh2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'crag zexr rzjc gxzv'  # Use app password
mail = Mail(app)

from flask import request, jsonify
import smtplib
from email.message import EmailMessage
import ssl


@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    recipient = data.get('email')  # Dynamic receiver from frontend
    message = data.get('message')  # Dynamic message from frontend

    if not recipient:
        return jsonify({"error": "No email provided"}), 400

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Email credentials (USE ENVIRONMENT VARIABLES IN PRODUCTION)
    sender_email = "wardheadesh2003@gmail.com"
    password = "tqqr cauv lige pgvp"  # Use App Password

    # Read the Excel file
    file_path = EXCEL_FILE  # Update with the path to your file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to read the Excel file: {str(e)}"}), 500

    # Search for the most recent row for the recipient's email
    recent_row = df[df['Email'] == recipient].tail(1)
    
    if recent_row.empty:
        return jsonify({"error": f"No data found for email: {recipient}"}), 404
    
    # Extract required column values
    file_type = recent_row['File Type'].values[0]
    detection = recent_row['Detection'].values[0]
    detection_class = recent_row['Detection Class'].values[0]

    # Email content
    subject = "E-Waste Pickup Notification"
    body = f"""
    Hello,

    This is a confirmation regarding your E-Waste submission.

    Message from user:
    {message}

    Recent Submission Details:
    - File Type: {file_type}
    - Detection: {detection}
    - Detection Class: {detection_class}

    Thank you!
    """

    # Create email message
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach the image
    img_path = latest_image_inmail  # Path to the image
    try:
        with open(img_path, 'rb') as img_file:
            img_data = img_file.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=os.path.basename(img_path))
    except Exception as e:
        return jsonify({"error": f"Failed to attach image: {str(e)}"}), 500


    # Secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)

        return jsonify({"message": f"Email sent to {recipient}!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    """Try to open the browser only if the Flask server is running."""
    time.sleep(2)
    base_url = "http://localhost:5000"  # Use localhost for external access

    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("App is up and running.")
            # Disable browser opening in Docker
            # webbrowser.open(base_url)
    except requests.ConnectionError:
        print("Flask server not started, not opening the browser.")

if __name__ == '__main__':
    # Only open browser if NOT running inside Docker
    if os.environ.get("RUNNING_IN_DOCKER") != "1":
        threading.Thread(target=open_browser, daemon=True).start()

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True, use_reloader=False)
