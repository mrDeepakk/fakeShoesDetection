import tensorflow as tf
import numpy as np
from PIL import Image
import os
import sys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import gdown

file_id = "1zJ3K6P96_JBbZ1qDV1JzFbYzKuO2Sghn"
MODEL_PATH = "backend/static/fake_shoe_model.h5"
gdrive_url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists(MODEL_PATH):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    gdown.download(gdrive_url, MODEL_PATH, quiet=False)

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(file_path: str):
    try:
        # Open the image file
        image = Image.open(file_path).convert("RGB")
        
        # Resize image to match model input
        image = image.resize((224, 224))
        
        # Convert image to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        prediction = model.predict(image_array)
        
        # Get predicted class index
        predicted_class_index = np.argmax(prediction, axis=-1)[0]
        
        # Get confidence score (probability of the predicted class)
        confidence_score = float(np.max(prediction))  # Convert to float for JSON compatibility
        
        return predicted_class_index, confidence_score
        
    except Exception as e:
        return {"error": f"Error during prediction: {str(e)}"}
