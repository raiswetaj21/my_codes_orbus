from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import streamlit as st 
from dotenv import load_dotenv 
import os

load_dotenv()

def classify_waste(img):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    # Resize and prepare the image
    image = img.convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predict the class
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name, confidence_score

st.set_page_config(layout='wide')

st.title("Garbage Classifier Sustainability Application")

input_img = st.file_uploader("Enter your captured image below:-", type=['jpg', 'png', 'jpeg'])

if input_img is not None:
    if st.button("Classify"):
        
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.info("Your Uploaded Image:")
            st.image(input_img, use_column_width=True)

        with col2:
            st.info("Your Classification Result:")
            image_file = Image.open(input_img)
            label, confidence_score = classify_waste(image_file)
            st.success(f"The uploaded image is classified as {label.strip().upper()}.")
