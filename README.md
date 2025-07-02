# ♻️ E-Waste Management System using AI (Flask + YOLOv5 + Geolocation)

This is a full-stack AI-based web application that promotes sustainable e-waste recycling by connecting users with e-waste recycling NGOs. Built using **Flask**, **YOLOv5**, **Leaflet Maps**, and **geolocation APIs**, it helps detect e-waste from images and schedule pickup requests based on user location.

![Screenshot](https://github.com/AdeshWardhe/recycle2/blob/02cde1e9b81520491a165bde80d096b3125118cd/front1.jpg?raw=true))

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
| [![Image_alt](https://github.com/AdeshWardhe/recycle2/blob/fce286567c215330bf2ea65701304d5fb7f3f679/detected_keyboard.jpg?raw=true)](https://github.com/AdeshWardhe/recycle2/blob/fce286567c215330bf2ea65701304d5fb7f3f679/detected_keyboard.jpg)
 | `Detected: keyboard (0.83)` |

---

## 💡 How It Works

1. User opens the site and shares their **location + email**.
2. Uploads an image of old electronic item.
3. YOLOv5 model detects object and displays the class.
4. User's location and object details are stored.
5. NGO can view live map with email list and use it for pickups.
6. Users receive confirmation via email.

---

## 📦 Installation & Run (Local)

```bash
git clone https://github.com/your-username/recycle2.git
cd recycle2
pip install -r requirements.txt
python app.py
