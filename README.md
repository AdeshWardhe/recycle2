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

| Tool/Library               | Purpose                           |
| -------------------------- | --------------------------------- |
| Python + Flask             | Backend framework                 |
| YOLOv5                     | Object detection (custom trained) |
| HTML + CSS + JS            | Frontend                          |
| Leaflet.js + OpenStreetMap | Mapping and marker display        |
| Google Geolocation API     | User location detection           |
| SMTP (Python)              | Sending emails                    |
| SQLite / PostgreSQL        | Data storage                      |

---

### 🔍 YOLOv5 Detection Result Example

Below is an example where a keyboard was successfully detected from an uploaded image, with a confidence score of 91%.

| Upload                                                                                                                           | Detection                     |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| ![Image_alt](https://github.com/AdeshWardhe/recycle2/blob/461e9a8db972f58bdf5182b48a149411eb4c096d/detected_keyboard.jpg?raw=true) | `Detected: keyboard (0.91)` |

---

## 💡 How It Works

1. User opens the site and shares their **location + email**.
2. Uploads an image of old electronic item.
3. YOLOv5 model detects object and displays the class.
4. User's location and object details are stored.
5. NGO can view live map with email list and use it for pickups.
6. Users receive confirmation via email.

---

## 🖼️ More Visuals from the Application Flow

Here are some screenshots that demonstrate the full process after detecting an e-waste item:

---

### 1. 📝 Detection Results Stored in Excel

After an image is detected using YOLOv5, the **user’s location** and **detected object name** are automatically saved into an Excel sheet.

![saved_in_excel](https://github.com/AdeshWardhe/recycle2/blob/5ae9c473e0e2338dcb351507dfe513e6a7a49b97/saved_in_excel.jpg?raw=true)

---

### 2. 📄 Live Web View from Excel

Entries from the Excel sheet are shown on the website in **reverse order** – the most recent detection appears at the top. NGOs or admins can send **custom messages** to each user.

![saved_in_excel](https://github.com/AdeshWardhe/recycle2/blob/69c63b6229b7467b8227992d244062457e3d2e3c/custom_email_updated.JPG?raw=true)

---

### 3. ✅ Email Notification Sent

Once the custom email is sent, a **confirmation notification** appears.

![email_sent](https://github.com/AdeshWardhe/recycle2/blob/e79e2cf50d2ba0ba0edf55d3ebe21ca58670fed4/email_sent.jpg?raw=true)

---

### 4. 🗺️ Map Marker Updated

The user’s pickup location is shown as a **marker on the map** embedded on the NGO dashboard.

![saved_in_excel](https://github.com/AdeshWardhe/recycle2/blob/e79e2cf50d2ba0ba0edf55d3ebe21ca58670fed4/loc_map_marker.jpg)

---

### 5. 🔗 Dynamic Resource Links Updated

The "Links" section on the right side of the website updates dynamically based on the **detected e-waste item** – providing relevant recycling resources or videos.

---

###  📦 Model Weights (Auto-Download)

This project uses a custom-trained YOLOv5 model for e-waste detection.  
You do **not** need to download `best.pt` manually — it will be automatically downloaded from Hugging Face when you run the app.

🔗 Model is hosted here: [Hugging Face - recycle2-yolov5](https://huggingface.co/adeshwardhe/recycle2-yolov5)

---

## 📦 Installation & Run (Local)

```bash
git clone https://github.com/AdeshWardhe/recycle2.git
cd recycle2
pip install -r requirements.txt
python app1.py
```
