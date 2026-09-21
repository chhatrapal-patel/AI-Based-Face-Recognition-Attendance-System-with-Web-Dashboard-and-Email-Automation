import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# =========================
# Paths
# =========================
path = "known_faces"   # folder with images directly inside
attendance_folder = "attendance"
os.makedirs(attendance_folder, exist_ok=True)  # make sure attendance folder exists

# Attendance file with today's date
today_date = datetime.now().strftime("%d%m%y")
attendance_file = os.path.join(attendance_folder, f"attendance{today_date}.csv")

# =========================
# Load Known Faces (flat folder)
# =========================
images = []
classNames = []
encodeList = []

print("✅ Loading known faces...")
for file in os.listdir(path):
    img_path = os.path.join(path, file)

    # Skip non-image files
    if not (file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") or file.lower().endswith(".png")):
        continue

    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Skipping unreadable file: {file}")
        continue

    images.append(img)
    classNames.append(os.path.splitext(file)[0])

# Encode faces
for img in images:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)  # ensure correct dtype

    boxes = face_recognition.face_locations(img_rgb, model="hog")  # explicit model
    enc = face_recognition.face_encodings(img_rgb, boxes)
    if enc:
        encodeList.append(enc[0])

print(f"✅ Loaded {len(encodeList)} known faces: {classNames}")

# =========================
# Mark Attendance
# =========================
def markAttendance(name):
    with open(attendance_file, "a+") as f:
        f.seek(0)
        lines = f.readlines()
        nameList = [line.split(",")[0] for line in lines]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.write(f"{name},{dtString}\n")

# =========================
# Webcam Setup
# =========================
video_capture = cv2.VideoCapture(0)  # Try 1 or 2 if 0 doesn't work

if not video_capture.isOpened():
    print("❌ Could not open camera. Try changing index in cv2.VideoCapture().")
    exit()

print("📷 Scanning for faces... Press 'q' to quit.")

# =========================
# Main Loop
# =========================
while True:
    ret, frame = video_capture.read()
    if not ret or frame is None:
        print("⚠️ Failed to grab frame from camera")
        continue

    # Resize for speed
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    rgb_small_frame = np.ascontiguousarray(rgb_small_frame, dtype=np.uint8)

    # Detect faces (explicitly specify model)
    try:
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    except Exception as e:
        print("⚠️ Face detection error:", e)
        continue

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encodeList, face_encoding)
        face_distances = face_recognition.face_distance(encodeList, face_encoding)
        
        name = "Unknown"
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = classNames[best_match_index]

        # Draw box
        top, right, bottom, left = face_location
        top, right, bottom, left = top*4, right*4, bottom*4, left*4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Mark attendance
        markAttendance(name)

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================
# Cleanup
# =========================
video_capture.release()
cv2.destroyAllWindows()