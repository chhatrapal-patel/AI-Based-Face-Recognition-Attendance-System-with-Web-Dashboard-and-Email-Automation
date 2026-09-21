import cv2
import face_recognition
import numpy as np
import os
import sys
from datetime import datetime

# =========================
# Get Subject from Command Line Arguments
# =========================
if len(sys.argv) < 2:
    print("❌ Error: No subject specified. Usage: python main.py <subject_name>")
    exit()

subject_name = sys.argv[1]
print(f"📚 Starting face recognition for subject: {subject_name}")

# =========================
# Paths
# =========================
path = "known_faces"   # folder with images directly inside
attendance_base_folder = "attendance"
subject_folder = os.path.join(attendance_base_folder, subject_name)

# Create subject-specific folder
os.makedirs(subject_folder, exist_ok=True)

# Attendance file with today's date in subject folder
today_date = datetime.now().strftime("%d%m%y")
attendance_file = os.path.join(subject_folder, f"attendance_{subject_name}_{today_date}.csv")

# Path for live frame for Streamlit
live_frame_file = "live.jpg"

# =========================
# Load Known Faces
# =========================
images = []
classNames = []
encodeList = []

print("✅ Loading known faces...")
for file in os.listdir(path):
    img_path = os.path.join(path, file)

    if not (file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") or file.lower().endswith(".png")):
        continue

    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Skipping unreadable file: {file}")
        continue

    images.append(img)
    classNames.append(os.path.splitext(file)[0])

for img in images:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)

    boxes = face_recognition.face_locations(img_rgb, model="hog")
    enc = face_recognition.face_encodings(img_rgb, boxes)
    if enc:
        encodeList.append(enc[0])

print(f"✅ Loaded {len(encodeList)} known faces: {classNames}")

# =========================
# Mark Attendance
# =========================
def markAttendance(name):
    if name == "Unknown":
        return  # Don't mark unknown faces

    if not os.path.exists(attendance_file):
        with open(attendance_file, "w") as f:
            f.write("Name,Subject,Timestamp\n")

    with open(attendance_file, "r+") as f:
        lines = f.readlines()
        nameList = [line.split(",")[0] for line in lines[1:]]  # skip header
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.write(f"{name},{subject_name},{dtString}\n")
            print(f"🟢 Marked attendance for {name} in {subject_name}")

# =========================
# Webcam Setup with optimizations
# =========================
video_capture = cv2.VideoCapture(0)

# Optimize camera settings for faster startup
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_capture.set(cv2.CAP_PROP_FPS, 30)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not video_capture.isOpened():
    print("❌ Could not open camera. Try changing index in cv2.VideoCapture().")
    exit()

print(f"📷 Scanning for faces in {subject_name}... Press 'q' to quit.")

# =========================
# Main Loop
# =========================
THRESHOLD = 0.5  # lower = stricter
frame_count = 0
skip_frames = 3  # Process every 3rd frame for better performance

while True:
    ret, frame = video_capture.read()
    if not ret or frame is None:
        print("⚠️ Failed to grab frame from camera")
        continue

    frame_count += 1
    
    # Process face recognition only every skip_frames for better performance
    if frame_count % skip_frames == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame, dtype=np.uint8)

        try:
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        except Exception as e:
            print("⚠️ Face detection error:", e)
            continue

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_distances = face_recognition.face_distance(encodeList, face_encoding)

            name = "Unknown"
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if face_distances[best_match_index] < THRESHOLD:
                    name = classNames[best_match_index]

            # Draw box
            top, right, bottom, left = [v * 4 for v in face_location]
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, f"{name} - {subject_name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

            # Mark attendance only if recognized
            markAttendance(name)

    # Save frame for Streamlit (always save, regardless of processing)
    cv2.imwrite(live_frame_file, frame)
    cv2.imshow(f"Face Attendance - {subject_name}", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()