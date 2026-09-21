from flask import Flask, request, jsonify
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# =========================
# Email Config
# =========================
SENDER_EMAIL = "vksahu160805@gmail.com"
SENDER_PASSWORD = "pnnc iumu spmx tyxc"  # Gmail App Password (not normal password)

# Map student names (same as image filenames in known_faces) to their emails
student_emails = {
    "vinay": "vksahu160805@gmail.com",
    "nikhil": "nikhildew2004@gmail.com",
    
    # Add more here
}

attendance_folder = "attendance"
os.makedirs(attendance_folder, exist_ok=True)
today_date = datetime.now().strftime("%d%m%y")
attendance_file = os.path.join(attendance_folder, f"attendance{today_date}.csv")

# =========================
# Utility Functions
# =========================
def send_email(to_email, subject, message):
    """Send email using Gmail SMTP"""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"📧 Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def mark_attendance(name):
    """Mark attendance in CSV and trigger email"""
    if not os.path.exists(attendance_file):
        with open(attendance_file, "w") as f:
            f.write("Name,Timestamp\n")

    with open(attendance_file, "r+") as f:
        lines = f.readlines()
        nameList = [line.split(",")[0] for line in lines[1:]]  # skip header

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.write(f"{name},{dtString}\n")

            # Email notification
            if name in student_emails:
                send_email(
                    student_emails[name],
                    "Attendance Marked ✅",
                    f"Hello {name},\n\nYour attendance has been marked as PRESENT at {dtString}.\n\nRegards,\nAttendance System"
                )
            else:
                send_email(
                    "chhatrapaldewangan2004@gmail.com",  # Change to teacher/admin email
                    "Unknown Face Detected ⚠️",
                    f"An unrecognized person was detected at {dtString}. Attendance not marked."
                )
            return True
        else:
            return False

# =========================
# API Routes
# =========================

@app.route("/mark", methods=["POST"])
def mark():
    """API endpoint to mark attendance"""
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"status": "error", "message": "Name is required"}), 400

    success = mark_attendance(name)
    if success:
        return jsonify({"status": "success", "message": f"Attendance marked for {name}"})
    else:
        return jsonify({"status": "info", "message": f"{name} already marked"})

@app.route("/attendance", methods=["GET"])
def get_attendance():
    """Fetch attendance records"""
    if not os.path.exists(attendance_file):
        return jsonify({"status": "error", "message": "No attendance file yet"}), 404

    records = []
    with open(attendance_file, "r") as f:
        lines = f.readlines()[1:]  # skip header
        for line in lines:
            name, timestamp = line.strip().split(",")
            records.append({"name": name, "timestamp": timestamp})

    return jsonify({"status": "success", "records": records})

# =========================
# Run Flask
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
