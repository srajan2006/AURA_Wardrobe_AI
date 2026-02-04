import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import os

MODEL_PATH = "aura_garment_model.h5"
IMG_SIZE = (224, 224)

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load class names saved during training
with open("class_names.json", "r") as f:
    class_names = json.load(f)

print("Loaded classes:", class_names)


def predict_image(img_path):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")

    # Load and preprocess image
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)

    # Model was trained with Rescaling(1./255), so DO NOT divide again
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array, verbose=0)[0]

    predicted_index = np.argmax(predictions)
    predicted_class = class_names[predicted_index]
    confidence = float(predictions[predicted_index])

    # Debug: show all probabilities
    print("\nClass probabilities:")
    for i, prob in enumerate(predictions):
        print(f"{class_names[i]}: {prob:.3f}")

    return predicted_class, confidence


# 🔽 Change this to any image you want to test
test_image = "test-image2.jpg"

category, conf = predict_image(test_image)

print("\nPredicted category:", category)
print(f"Confidence: {conf:.2f}")
