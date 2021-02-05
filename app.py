import os
from flask import Flask, request, redirect, render_template, url_for, jsonify
from tensorflow.keras.models import load_model
from flask_dropzone import Dropzone

from utils import img_to_array, decode_predictions

# Declare a flask app
app = Flask(__name__)

# Dropzone for image upload
dropzone = Dropzone(app)

app.config.update(
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
)

# Model saved with Keras
MODEL_PATH = 'model.h5'

# Load pre-trained model
model = load_model(MODEL_PATH)       
print('Model loaded. Start serving...')


def model_predict(img, model):
    # Preprocessing the image
    x_img = img_to_array(img)

    # Prepare for prediction input
    x_img = x_img.reshape(-1,32,32,1).astype('float32')
    x_img = x_img/255

    # Generate predictions
    preds = model.predict(x_img)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No image found')
            return redirect(url_for('index'))
        # Get the image from post request
        img = request.files.get('file')
        file_path = os.path.join('uploads', img.filename)
        img.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        
        # Decode prediction
        pred_class = decode_predictions(preds, top=1)
        result = list(pred_class[0])

        return jsonify(result=result)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
