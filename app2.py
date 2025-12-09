from cProfile import label
from flask import Flask, request, jsonify, redirect
import os
import uuid
import cv2
import numpy as np
from tensorflow import keras  
from keras.applications import inception_v3

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 10

MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048



MODEL_PATH = 'my_model.h5'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x+min_dim]

def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)

def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")


feature_extractor = build_feature_extractor()

def prepare_single_video(frames):
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH,), dtype="bool")
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            frame_features[i, j, :] = feature_extractor.predict(batch[None, j, :])
        frame_mask[i, :length] = 1  

    return frame_features, frame_mask

def sequence_prediction(path):
    frames = load_video(path)
    frame_features, frame_mask = prepare_single_video(frames)
    model = keras.models.load_model(MODEL_PATH)
    return model.predict([frame_features, frame_mask])[0]

@app.route('/summary', methods=['POST'])
def predict_deepfake():
    if request.method == 'POST':
        video_file = request.files['video']
        if video_file and allowed_file(video_file.filename):
            video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            video_file.save(video_path)
            ans=sequence_prediction(video_path)

            print(ans)
            if(ans <= 0.76): 
                is_deepfake="FAKE"
            else:
                is_deepfake="REAL"

            return jsonify({'is_deepfake': is_deepfake})
        else:
            return jsonify({'error': 'Invalid file format'}), 400

    return jsonify({'error': 'No video uploaded'}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
