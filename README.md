# ♻️ E-Waste Management System using AI (Flask + YOLOv5 + Geolocation)

This is a full-stack AI-based web application that promotes sustainable e-waste recycling by connecting users with e-waste recycling NGOs. Built using **Flask**, **YOLOv5**, **Leaflet Maps**, and **geolocation APIs**, it helps detect e-waste from images and schedule pickup requests based on user location.

![screenshot](https://github.com/AdeshWardhe/recycle2/blob/02cde1e9b81520491a165bde80d096b3125118cd/front1.jpg?raw=true)

---

## 🚀 Features

### 1. 🧠 E-Waste Detection (YOLOv5)
- Users upload an image of old electronic waste.
- A YOLOv5 model classifies the image into one of the following:
  - `keyboard`
  - `mouse`
  - `battery`
  - `processor_and_memory chips`
- Detected objects are highlighted with confidence scores.

### 2. 🌍 User Geolocation Tracking
- Captures the user’s **live location** (latitude, longitude) and **email ID** before uploading.
- Location and email are stored and used for pickups by NGOs.

### 3. 📺 Educational Recommendations
- Displays **YouTube videos** and articles that spread awareness about e-waste recycling and upcycling ideas.

### 4. 🗺️ Real-Time NGO Dashboard
- Shows a **map** with markers indicating user pickup locations.
- Shows a scrollable list of submitted **emails**.
- NGOs can use this data to cluster and schedule efficient pickups.

### 5. 📧 Automated Email Notifications
- Auto-generates formatted pickup emails using stored data.
- Sends confirmation to users with location and item details.

---

## 🛠 Tech Stack

| Tool/Library          | Purpose                            |
|-----------------------|-------------------------------------|
| Python + Flask        | Backend framework                   |
| YOLOv5                | Object detection (custom trained)   |
| HTML + CSS + JS       | Frontend                           |
| Leaflet.js + OpenStreetMap | Mapping and marker display     |
| Google Geolocation API| User location detection             |
| SMTP (Python)         | Sending emails                      |
| SQLite / PostgreSQL   | Data storage                        |

---

## 📸 Sample Output

| Upload | Detection |
|--------|-----------|
| ![Image_alt](https://github.com/AdeshWardhe/recycle2/blob/461e9a8db972f58bdf5182b48a149411eb4c096d/detected_keyboard.jpg?raw=true)
 | `Detected: keyboard (0.91)` |

---

## 💡 How It Works

1. User opens the site and shares their **location + email**.
2. Uploads an image of old electronic item.
3. YOLOv5 model detects object and displays the class.
4. User's location and object details are stored.
5. NGO can view live map with email list and use it for pickups.
6. Users receive confirmation via email.

---

there are some screenshot 
1. After the image getting detected the image would be shown and the info like the location of the user and the object that has been detected will get store in the excel sheet
   
  ![saved_in_excel](https://github.com/AdeshWardhe/recycle2/blob/5ae9c473e0e2338dcb351507dfe513e6a7a49b97/saved_in_excel.jpg?raw=true)
3. And the entries in the excel sheet will be shown in the website in the order of the last to first means the last entry in the excel sheet will be shown first in the website and then we can sent the custom message to that user
   
  ![saved_in_excel](https://github.com/AdeshWardhe/recycle2/blob/69c63b6229b7467b8227992d244062457e3d2e3c/custom_email_updated.JPG?raw=true)
4. notification of email sent
   
   ![email_sent](https://github.com/AdeshWardhe/recycle2/blob/e79e2cf50d2ba0ba0edf55d3ebe21ca58670fed4/email_sent.jpg?raw=true)
5. And the marker will get updated in the map which is shown in the website

   ![saved_in_excel](https://github.com/AdeshWardhe/recycle2/blob/e79e2cf50d2ba0ba0edf55d3ebe21ca58670fed4/loc_map_marker.jpg)
   
6. And the link coloumu in the right side of the wensite will get updated as per the image detected






## 📦 Installation & Run (Local)

```bash
git clone https://github.com/your-username/recycle2.git
cd recycle2
pip install -r requirements.txt
python app.py
