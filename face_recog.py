import dlib
import numpy as np
import cv2
import os
from scipy.spatial import distance
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session


# Initialize dlib's face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_recognition_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

def get_face_descriptor(image):
    detected_faces = detector(image, 1)
    if len(detected_faces) > 0:
        shape = shape_predictor(image, detected_faces[0])
        return np.array(face_recognition_model.compute_face_descriptor(image, shape))
    else:
        return None

def compare_faces(known_faces, face):
    return np.linalg.norm(known_faces - face, axis=1)

def add_student_face(student_image_path, known_face_encodings, known_face_names):
    # Check if the file is an image
    if not student_image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Skipped non-image file: {student_image_path}")
        return

    student_image = cv2.imread(student_image_path)
    # Check if the image was loaded successfully
    if student_image is None:
        print(f"Failed to load image: {student_image_path}")
        return

    student_image_rgb = cv2.cvtColor(student_image, cv2.COLOR_BGR2RGB)
    face_descriptor = get_face_descriptor(student_image_rgb)
    if face_descriptor is not None:
        known_face_encodings.append(face_descriptor)
        known_face_names.append(os.path.basename(student_image_path))

def face_recognition(db, student_photos_path, group_photo_path, group_id, datetime):
    # Prepare student faces
    known_face_encodings = []
    known_face_names = [] # To keep track of whose face it is
    present_names = []

    # Assuming student photos are in a folder named 'student_photos'
    student_photos_path = student_photos_path
    for student_photo in os.listdir(student_photos_path):
        add_student_face(os.path.join(student_photos_path, student_photo), known_face_encodings, known_face_names)


    # Load the class photo
    class_image = cv2.imread(group_photo_path)
    class_image_rgb = cv2.cvtColor(class_image, cv2.COLOR_BGR2RGB)

    # Detect and recognize faces in the class photo
    for face in detector(class_image_rgb, 1):
        shape = shape_predictor(class_image_rgb, face)
        face_descriptor = np.array(face_recognition_model.compute_face_descriptor(class_image_rgb, shape))
        distances = compare_faces(known_face_encodings, face_descriptor)
        best_match_index = np.argmin(distances)
        if distances[best_match_index] < 0.5:  # Threshold for a match
            filename = (known_face_names[best_match_index])
            name, ext = os.path.splitext(filename)
            present_names.append(name)
    
    for filename in known_face_names:
        rollno = (filename.split("."))[0]
        if rollno in present_names:
            db.execute(
                "INSERT INTO attendance (roll_no, group_id, attend, date_time) VALUES (:r, :g, :a, :d)",
                r=rollno,
                g=group_id,
                a="y",
                d=datetime
            )
        else:
            db.execute(
                "INSERT INTO attendance (roll_no, group_id, attend, date_time) VALUES (:r, :g, :a, :d)",
                r=(rollno),
                g=(group_id),
                a=("n"),
                d=(datetime)
            )



