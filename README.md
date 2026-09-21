# AI-Based-Face-Recognition-Attendance-System-with-Web-Dashboard-and-Email-Automation
AI-based attendance system using face recognition. Built with Python, OpenCV, Flask, and Streamlit. Detects faces in real-time, marks attendance automatically, provides a web dashboard, and supports email notifications for efficient attendance management.
# FaceTrack Pro — Smart Attendance System

> AI-powered face recognition attendance system for classrooms and college environments, with a Streamlit dashboard, real-time webcam recognition, subject-wise attendance records, and an optional Flask API/email notification layer.

![FaceTrack Pro Demo](live.jpg)

## 📌 Overview

**FaceTrack Pro** is a Python-based smart attendance management system that uses webcam-based facial recognition to identify registered students and automatically record their attendance.

The project combines:

- **OpenCV** for webcam capture and image processing
- **face_recognition** for face detection and face embeddings
- **NumPy** for numerical operations
- **Streamlit** for the interactive attendance dashboard
- **Pandas** for displaying attendance records
- **Flask** for optional REST API endpoints
- **Gmail SMTP** for optional attendance email notifications
- **CSV files** for lightweight attendance storage

The face-recognition program loads student images from `known_faces/`, compares live webcam faces against the stored face encodings, and records recognized students in date-specific CSV files.

---

## ✨ Features

### 🎥 Real-Time Face Recognition
- Captures video from the system webcam.
- Detects faces using the HOG-based face detector.
- Generates face encodings for registered students.
- Compares live faces with known faces.
- Uses a configurable recognition threshold.
- Displays the recognized student's name on the camera feed.

### 📝 Automatic Attendance
- Attendance is marked only for recognized faces.
- Unknown faces are not added to the attendance file.
- A student is not repeatedly marked in the same attendance file.
- Attendance is stored with the recognition time.

### 📚 Subject-Wise Attendance
The recognition script accepts the subject name from the command line:

```bash
python main.py <subject_name>
```

For example:

```bash
python main.py Mathematics
```

Attendance is stored using a structure similar to:

```text
attendance/
└── Mathematics/
    └── attendance_Mathematics_210926.csv
```

### 📊 Streamlit Dashboard
The dashboard provides:
- Current system time
- Attendance record count
- Online/offline process status
- Start/stop recognition controls
- Live camera frame
- Attendance table
- Feature and system-performance sections
- Automatic page refresh

The dashboard uses a customized dark/glassmorphism-style interface with animated sections and responsive styling.

### 🌐 Flask API
The optional Flask application provides REST endpoints for:
- Marking attendance through an HTTP POST request
- Retrieving attendance records through an HTTP GET request
- Sending attendance email notifications

Available endpoints:

```text
POST /mark
GET  /attendance
```

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │   Student Images     │
                 │    known_faces/      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Face Encoding /      │
                 │ Recognition Engine   │
                 │ OpenCV +             │
                 │ face_recognition     │
                 └──────────┬───────────┘
                            │
                   Recognized Student
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
   ┌──────────────────┐          ┌──────────────────┐
   │ Attendance CSV   │          │ Live Camera      │
   │ Subject + Date   │          │ live.jpg         │
   └────────┬─────────┘          └────────┬─────────┘
            │                             │
            └──────────────┬──────────────┘
                           ▼
                 ┌──────────────────────┐
                 │ Streamlit Dashboard  │
                 │       app.py         │
                 └──────────────────────┘

        Optional API / Notification Layer
                           │
                           ▼
                 ┌──────────────────────┐
                 │     Flask API        │
                 │   flask_app.py       │
                 └──────────┬───────────┘
                            │
                            ▼
                     Gmail SMTP
```

---

## 📂 Project Structure

A recommended repository structure is:

```text
FaceTrack-Pro/
│
├── app.py                  # Streamlit dashboard
├── main.py                 # Face recognition + attendance
├── flask_app.py            # Optional Flask API + email notifications
├── live.jpg                # Current camera frame generated at runtime
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── known_faces/            # Registered student face images
│   ├── student1.jpg
│   ├── student2.jpg
│   └── ...
│
└── attendance/             # Generated attendance data
    ├── Subject1/
    │   └── attendance_Subject1_DDMMYY.csv
    └── Subject2/
        └── attendance_Subject2_DDMMYY.csv
```

### Important

Do **not** commit private student data, generated attendance records, API credentials, or email passwords to GitHub.

A `.gitignore` file should be used for runtime and sensitive files.

---

## ⚙️ Requirements

Recommended environment:

- Python 3.9+
- Windows / Linux / macOS
- Working webcam
- Git
- pip

Python packages used by the uploaded source files include:

```text
streamlit
pandas
numpy
opencv-python
face-recognition
Flask
```

The Flask component additionally uses Python's built-in `smtplib` and email modules.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/FaceTrack-Pro.git
cd FaceTrack-Pro
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit pandas numpy opencv-python face-recognition Flask
```

If you create a `requirements.txt` file, install everything with:

```bash
pip install -r requirements.txt
```

---

## 👤 Add Known Faces

Create the directory:

```text
known_faces/
```

Place one clear face image for each registered student inside it.

Example:

```text
known_faces/
├── vinay.jpg
├── nikhil.jpg
├── student3.jpg
└── student4.jpg
```

The filename (without the extension) is used as the student's recognized name.

For example:

```text
vinay.jpg
```

will be recognized as:

```text
vinay
```

### Recommended image conditions

- One clearly visible face per image
- Good lighting
- Front-facing or near-front-facing image
- Minimal obstruction
- Reasonable image resolution

---

## ▶️ Running Face Recognition

The recognition script expects a subject name:

```bash
python main.py Mathematics
```

or:

```bash
python main.py Computer_Networks
```

The program:

1. Loads images from `known_faces/`.
2. Creates face encodings.
3. Opens the default webcam.
4. Detects faces in the video stream.
5. Compares detected faces with registered encodings.
6. Displays the recognized name and subject.
7. Records attendance for recognized students.
8. Saves the latest camera frame to `live.jpg`.
9. Press `q` in the OpenCV window to stop recognition.

The recognition threshold is currently:

```python
THRESHOLD = 0.5
```

A lower threshold makes matching stricter.

---

## 📊 Running the Streamlit Dashboard

Start Streamlit with:

```bash
streamlit run app.py
```

Then open the URL displayed by Streamlit, normally:

```text
http://localhost:8501
```

The dashboard can start and stop the recognition process and display the generated camera frame and attendance information.

### ⚠️ Current integration note

The uploaded `app.py` currently contains:

```python
main_script = "main222.py"
```

while the uploaded recognition program is named:

```text
main.py
```

Before running the dashboard, either:

1. Rename `main.py` to `main222.py`, **or**
2. Change the value in `app.py` to:

```python
main_script = "main.py"
```

The second option is generally cleaner.

---

## 📁 Attendance Storage

The recognition script creates subject-specific directories:

```text
attendance/
└── <subject_name>/
    └── attendance_<subject_name>_<date>.csv
```

The CSV contains:

```text
Name,Subject,Timestamp
```

Example:

```csv
Name,Subject,Timestamp
vinay,Mathematics,10:15:32
nikhil,Mathematics,10:17:04
```

Each recognized student is added only once to that attendance file.

---

## 🌐 Flask API

The optional Flask application can be started with:

```bash
python flask_app.py
```

The server runs on:

```text
http://localhost:5000
```

### Mark attendance

Endpoint:

```text
POST /mark
```

Example request body:

```json
{
  "name": "vinay"
}
```

Example response:

```json
{
  "status": "success",
  "message": "Attendance marked for vinay"
}
```

### Retrieve attendance

Endpoint:

```text
GET /attendance
```

Example:

```bash
curl http://localhost:5000/attendance
```

---

## 📧 Email Notifications

The Flask component can send email notifications through Gmail SMTP.

The intended workflow is:

```text
Recognized Student
       │
       ▼
Attendance Marked
       │
       ▼
Student Email
       │
       ▼
"Attendance Marked" Notification
```

An unrecognized face can also trigger an administrator/teacher notification.

### 🔐 Security requirement

Never store a Gmail password or App Password directly in a public GitHub repository.

The current uploaded `flask_app.py` contains an email credential directly in the source code. **Remove that credential before pushing the project to GitHub and rotate/revoke it if it has already been exposed.**

Use environment variables instead, for example:

```python
import os

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
```

Then configure the variables locally.

For Windows PowerShell:

```powershell
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_PASSWORD="your-app-password"
```

For a deployed application, configure these values through the hosting platform's secret/environment-variable system.

---

## 🔒 Privacy and Security

This project processes biometric information, so privacy should be treated as a core requirement.

Before deploying it in a real institution:

- Obtain appropriate consent and authorization.
- Restrict access to face images.
- Do not expose `known_faces/` publicly.
- Protect attendance records.
- Avoid committing student personal information to Git.
- Use secure authentication for production APIs.
- Use HTTPS when exposing the application over a network.
- Store email credentials in environment variables or a secrets manager.
- Define retention and deletion policies for biometric data.
- Follow applicable institutional and legal requirements.

---

## 🛠️ Troubleshooting

### Camera does not open

Check:

```python
video_capture = cv2.VideoCapture(0)
```

If the default camera is unavailable, try another camera index such as:

```python
video_capture = cv2.VideoCapture(1)
```

Also make sure another application is not using the webcam.

### No face is recognized

Check:

- The image exists in `known_faces/`.
- The image contains a detectable face.
- Lighting is sufficient.
- The face is reasonably visible.
- The recognition threshold is appropriate.

### Streamlit shows no live image

Make sure the recognition process is running and that:

```text
live.jpg
```

is being generated.

The recognition script continuously writes the current frame to `live.jpg`.

### Attendance table is empty

Check that the attendance CSV has been generated and that the dashboard is looking at the same attendance directory.

There is currently an integration difference between the two uploaded programs:

- `main.py` stores CSV files inside subject subdirectories.
- `app.py` searches for CSV files directly inside `attendance/`.

If the dashboard does not display subject-wise records, update the dashboard to recursively search `attendance/<subject>/` directories.

---

## 🔄 Recognition Workflow

```text
Start Program
     │
     ▼
Load known_faces/
     │
     ▼
Generate Face Encodings
     │
     ▼
Open Webcam
     │
     ▼
Capture Frame
     │
     ▼
Detect Face
     │
     ▼
Generate Live Face Encoding
     │
     ▼
Compare With Known Encodings
     │
     ├───────────────┐
     │               │
     ▼               ▼
 Recognized       Unknown
     │               │
     ▼               ▼
Mark Attendance   Do Not Mark
     │
     ▼
Save CSV + live.jpg
     │
     ▼
Display Result
```

---

## 🎯 Future Enhancements

Possible improvements for the project include:

- [ ] Admin login and role-based access
- [ ] Student registration interface
- [ ] Face enrollment directly from webcam
- [ ] PostgreSQL/MySQL database instead of CSV storage
- [ ] Subject selection from the dashboard
- [ ] Recursive attendance loading in Streamlit
- [ ] Attendance percentage calculation
- [ ] Monthly and semester reports
- [ ] CSV/Excel/PDF report export
- [ ] Late-entry detection
- [ ] Multiple-camera support
- [ ] REST API authentication
- [ ] HTTPS deployment
- [ ] Secure secret management
- [ ] Liveness/anti-spoofing detection
- [ ] Improved face-recognition model and threshold calibration
- [ ] Cloud deployment

---

## 🧪 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Face Recognition | face_recognition |
| Numerical Processing | NumPy |
| Data Handling | Pandas |
| Web Dashboard | Streamlit |
| REST API | Flask |
| Notifications | Gmail SMTP |
| Data Storage | CSV |
| Interface Styling | HTML + CSS embedded in Streamlit |

---

## 📜 License

Choose an appropriate license before publishing the repository, such as MIT, Apache-2.0, or a proprietary license.

Example:

```text
MIT License
```

Only add an MIT license if you intend to release the project under those terms.

---

## 👨‍💻 Project

**FaceTrack Pro — Smart Attendance System**

Built as a computer-vision-based attendance management project using Python, OpenCV, face recognition, Streamlit, and Flask.
