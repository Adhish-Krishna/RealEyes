import os
import torch
import librosa
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

# Load the model and feature extractor
model_checkpoint = "wav2vec2-base-finetuned-ks/checkpoint-841"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_checkpoint)
model = AutoModelForAudioClassification.from_pretrained(model_checkpoint)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def process_audio(audio_file_path):
    # Load and resample the audio
    audio, sr = librosa.load(audio_file_path, sr=16000)

    # Extract features
    inputs = feature_extractor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

    predicted_class_id = predictions.argmax().item()
    predicted_label = model.config.id2label[predicted_class_id]
    confidence = predictions[0][predicted_class_id].item()

    return predicted_label, confidence

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Define a route for audio processing
@app.route('/predict', methods=['POST'])
def predict():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio_file']

    # Save the uploaded file temporarily
    file_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(file_path)

    # Process the audio file
    predicted_label, confidence = process_audio(file_path)

    # Remove the temporary file
    os.remove(file_path)

    # Return the prediction results
    return jsonify({
        'prediction': predicted_label,
        'confidence': confidence
    })

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)

    # Run the Flask server
    app.run(debug=True,port=8080)
