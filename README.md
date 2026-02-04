# 🎯 Face Attendance System Using FaceAPI.js (Local Models)
A **smart, secure, and offline face recognition–based attendance system** that automatically marks attendance using **real-time face recognition**.
The system runs **entirely on local machine** without requiring an internet connection for recognition.


## 📌 Project Overview

Manual attendance systems are time-consuming and prone to proxy attendance.
This project solves that problem by using **FaceAPI.js** with **locally hosted models** to recognize faces and automatically mark attendance.

✔ No internet required
✔ Real-time recognition
✔ Secure (no face images stored)
✔ Fast and lightweight
✔ Admin dashboard & reports


## 🚀 Features

* 🎥 **Live Camera Face Recognition**
* 🧑‍💼 **User Registration with Face Enrollment**
* 🕒 **Automatic Attendance Marking**
* 🔁 **Prevents Duplicate Attendance (per day)**
* 📊 **Admin Dashboard**
* 📁 **Attendance Reports (CSV / Excel)**
* 🔐 **Privacy-Friendly (only face descriptors stored)**
* ⚡ **Runs fully offline (local models)**


## 🧠 How the System Works

### 1️⃣ Camera Access

* Browser requests webcam permission
* Live video feed starts

### 2️⃣ Face Detection

* Uses **Tiny Face Detector model**
* Detects faces in real-time

### 3️⃣ Facial Landmark Detection

* Uses **68-point landmark model**
* Maps key facial features (eyes, nose, mouth)

### 4️⃣ Face Recognition

* Generates a **face descriptor (numeric vector)**
* Matches descriptor with stored users
* Uses **Euclidean distance matching**

### 5️⃣ Attendance Decision

* If face matches & not marked today → Attendance recorded
* If already marked → “Attendance Exists” message

### 6️⃣ Attendance Logging

* Stores date & time in database
* Redirects to success page


## 🧾 User Registration Flow

1. Admin enters:

   * User Name
   * Unique User ID
2. Camera captures face
3. Face is detected and validated
4. Face descriptor is extracted
5. Descriptor is saved in database
6. User is successfully registered

> ⚠️ Only **face descriptors** are stored — **no images**


## 🏗️ System Architecture

```
Browser (Frontend)
│
├── Camera Access
├── FaceAPI.js (Local Models)
│     ├─ Face Detection
│     ├─ Landmark Detection
│     └─ Face Recognition
│
└── Flask Backend (Python)
      ├─ User Registration API
      ├─ Attendance API
      └─ Reports API
            │
            └── SQLite Database
```


## 🧰 Technology Stack

### Frontend

* HTML
* Tailwind CSS
* JavaScript
* FaceAPI.js

### Backend

* Python
* Flask

### Database

* SQLite

### Models Used (Local)

* Tiny Face Detector
* Face Landmark 68 Model
* Face Recognition Model


## 📂 Project Structure

```
Face-Attendance-System/
│
├── app.py
├── database/
│   └── attendance.db
│
├── templates/
│   ├── layout.html
│   ├── camera.html
│   ├── register.html
│   ├── recognition.html
│   ├── attendance_success.html
│   ├── attendance_exists.html
│   ├── admin.html
│   └── reports.html
│
├── static/
│   ├── js/
│   │   └── face-api.min.js
│   └── models/
│       ├── tiny_face_detector_model*
│       ├── face_landmark_68_model*
│       └── face_recognition_model*
│
└── README.md
```


## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/face-attendance-system.git
cd face-attendance-system
```

### 2️⃣ Install Dependencies

```bash
pip install flask
```

### 3️⃣ Run Application

```bash
python app.py
```


---

## 📊 Admin Dashboard

Admin can:

* View total registered users
* See today’s attendance count
* Delete users
* Access attendance reports
* Export data to CSV / Excel


## 🔐 Security & Privacy

* ❌ No face images stored
* ✅ Only numerical face descriptors saved
* 🔒 All processing done locally
* 🌐 No third-party API usage
* 🛡️ Reduced data leakage risk


## 🎓 Use Cases

* Colleges & Universities
* Schools
* Offices & Organizations
* Training Institutes
* Internship Attendance


## 📈 Future Enhancements

* Multi-camera support
* Role-based access
* Face anti-spoofing
* Mobile app integration
* Cloud backup (optional)


## 👨‍💻 Author

**Santosh Chacharkar**
MCA Student | Python & AI Projects Developer
📍 Maharashtra, India


## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 🧠 Learn & build on top of it


