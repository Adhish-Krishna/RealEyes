from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from mtcnn.mtcnn import MTCNN
from cv2 import dnn
from flask_cors import CORS
import random

# Initialize Flask app
app = Flask(__name__)

CORS(app)

# Load the deepfake detection model
model_path = 'Deepfake2d.h5'
model = load_model(model_path)

# Load face detection model (MTCNN and SSD options)
def load_face_detection_model(method, model_paths=None):
    if method == 'MTCNN':
        return MTCNN()
    elif method == 'SSD':
        net = dnn.readNetFromCaffe(model_paths['prototxt'], model_paths['caffemodel'])
        return net
    else:
        print("Unsupported model for face detection.")
        return None

# Extract frames from video (randomly select a few)
def extract_frames_rand(video_path, num_frames_to_select):
    capture = cv2.VideoCapture(video_path)
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    selected_frame_indices = random.sample(range(total_frames), num_frames_to_select)
    selected_frames = []

    for frame_idx in selected_frame_indices:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = capture.read()
        if ret:
            selected_frames.append(frame)

    capture.release()
    return selected_frames


# Extract face from frame using either MTCNN or SSD
def extract_face(frame, method='MTCNN', margin=0):
    detector = None
    net = None
    if method == 'MTCNN':
        detector = load_face_detection_model(method)
        faces = detector.detect_faces(frame)
        if faces:
            x, y, w, h = faces[0]['box']
            x -= margin
            y -= margin
            w += 2 * margin
            h += 2 * margin
            x, y, w, h = max(0, x), max(0, y), w, h
            face = frame[y:y + h, x:x + w]
            return cv2.resize(face, (224, 224))
    elif method == 'SSD':
        model_paths = {'prototxt': 'deploy.prototxt.txt', 'caffemodel': 'res10_300x300_ssd_iter_140000.caffemodel'}
        net = load_face_detection_model(method, model_paths)
        (h, w) = frame.shape[:2]
        blob = dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = frame[startY:endY, startX:endX]
                return cv2.resize(face, (224, 224))
    return None

# Predict deepfake or real from extracted frames
def predict_from_frames(frames, face_detection_method='MTCNN'):
    faces = [extract_face(frame, method=face_detection_method) for frame in frames]
    faces = [face for face in faces if face is not None]

    if not faces:
        return [], []

    faces = np.array(faces)
    faces = preprocess_input(faces)

    # Perform prediction
    predictions = model.predict(faces)
    return predictions, predictions

# Simulate deepfake detection from a video
def predict_from_video(video_path, num_frames=3, face_detection_method='MTCNN'):
    frames = extract_frames_rand(video_path, num_frames)
    predictions, probs = predict_from_frames(frames, face_detection_method)

    if len(predictions) == 0:
        return {"error": "No Faces Detected"}, []

    return format_predictions(predictions, probs)

# Format predictions to be more readable
def format_predictions(predictions, probs):
    formatted_predictions = []
    for prediction, prob in zip(predictions, probs):
        label = "Fake" if prediction > 0.5 else "Real"
        probability = prob if label == "Fake" else 1 - prob
        formatted_predictions.append({"prediction": label, "probability": float(probability)})

    return formatted_predictions

# Format predictions to be more readable
def format_predictions(predictions, probs):
    formatted_predictions = []
    for prediction, prob in zip(predictions, probs):
        label = "Fake" if prediction > 0.5 else "Real"
        probability = prob if label == "Fake" else 1 - prob
        formatted_predictions.append({"prediction": label, "probability": float(probability)})
    return formatted_predictions

# API endpoint for deepfake detection from image
@app.route('/predict', methods=['POST'])
def predict_deepfake():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read the image from the uploaded file
    img_array = np.fromstring(file.read(), np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Perform face detection
    face = extract_face(frame, method='MTCNN')
    if face is None:
        return jsonify({"error": "No Face Detected"}), 400

    # Preprocess the face
    face = np.expand_dims(face, axis=0)
    face = preprocess_input(face)

    # Perform prediction
    predictions = model.predict(face)

    # Format and return predictions
    formatted_predictions = format_predictions(predictions, predictions)
    return jsonify({"predictions": formatted_predictions}), 200

@app.route('/predict/video', methods=['POST'])
def predict_deepfake_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the video file temporarily
    video_path = 'temp_video.mp4'
    file.save(video_path)

    # Run deepfake detection on the video
    predictions = predict_from_video(video_path, num_frames=3, face_detection_method='MTCNN')

    # Return predictions
    return jsonify(predictions), 200

if __name__ == '__main__':
    app.run(debug=True)
