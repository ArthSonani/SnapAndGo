# 📸 Snap&Go – AI-Powered Attendance System

**Snap&Go** is a face recognition-based **attendance automation system** built using Python, Flask, and OpenCV. Designed for classrooms, it enables teachers to capture a photo of the class and automatically mark attendance in real time using AI-based facial recognition with 75%+ accuracy.

---

## 🚀 Tech Stack

- **Backend**: Python, Flask, SQL
- **Frontend**: HTML, CSS, JavaScript
- **AI & Vision**: OpenCV, DLIB, Scipy, NumPy

---

## 🎯 Key Features

- 🖼️ **Real-time Photo Capture**  
  Built a responsive UI for capturing classroom snapshots on the spot.

- 🧠 **Face Recognition with DLIB**  
  Uses facial landmarks and deep learning to detect and identify students with **75%+ accuracy**.

- 🕒 **Instant Attendance Processing**  
  Automatically marks present students by comparing faces with the existing dataset.

- 📊 **Attendance Dashboard**  
  Displays recognized faces and corresponding attendance records.

- ⚡ **40% Efficiency Boost**  
  Automates manual attendance, saving time and reducing human error.

---

## 🧪 How It Works

1. **Capture Image** – Teacher captures a classroom photo through the web interface.
2. **Face Detection** – System uses DLIB & OpenCV to detect all faces.
3. **Face Recognition** – Detected faces are matched against pre-trained encodings.
4. **Attendance Marking** – Matching faces are recorded as present in the SQL database.
5. **Live Results** – Results are shown in real-time on the web interface.
