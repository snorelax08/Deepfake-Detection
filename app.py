import pickle
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import os
import cv2
import numpy as np
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'model.h5'  

model = load_model(MODEL_PATH)
model.make_predict_function()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/summary', methods=['POST'])
def process_image():
    # Check if an image is included in the request
    if 'image' not in request.form:
        return jsonify({'error': 'No image provided'}), 400

    # Get the base64 encoded image data from the request
    image_data_base64 = request.form['image']

    # Decode the base64 encoded image data
    image_data = base64.b64decode(image_data_base64.split(',')[1])

    # Convert the image data to a PIL Image object
    pil_image = Image.open(BytesIO(image_data))

    # Save the image to the uploads folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'process.png')
    pil_image.save(image_path)

    preds=model_predict(image_path,model)
    # THRESHOLD = 0
    if preds[0][0] >= 1:
        result = "Fake"
    elif preds[0][0] >= 0 :
        result = "Real"
    
    
    # Respond with a success message
    return jsonify({'message': result}), 200



def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(256, 256))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
