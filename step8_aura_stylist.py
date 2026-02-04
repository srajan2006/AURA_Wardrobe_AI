import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
from step10_color_detector import detect_clothing_color

# ================== LOAD MODEL ==================
MODEL_PATH = "aura_garment_model.h5"
IMG_SIZE = (224, 224)

model = tf.keras.models.load_model(MODEL_PATH)

with open("class_names.json", "r") as f:
    class_names = json.load(f)

# ================== OUTFIT RULES ==================

color_rules = {
    "white": ["blue", "black", "brown"],
    "blue": ["black", "grey", "white"],
    "black": ["blue", "grey"],
    "grey": ["black", "blue"],
    "red": ["black", "blue"],
    "green": ["black", "brown"],
    "yellow": ["blue", "black"],
    "brown": ["blue", "white"]
}

garment_rules = {
    "shirt": ["jeans", "jacket"],
    "tshirt": ["jeans", "jacket"],
    "jeans": ["shirt", "tshirt", "jacket"],
    "jacket": ["shirt", "tshirt", "jeans"]
}

# ================== FUNCTIONS ==================

def predict_garment(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)

    # Do NOT divide by 255 (model already has Rescaling layer)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)[0]
    idx = np.argmax(predictions)

    return class_names[idx], float(predictions[idx])


def predict_color(img_path):
    """Detect clothing color automatically"""
    return detect_clothing_color(img_path)


def recommend_outfit(category, color):
    color = color.lower().strip()
    suggestions = []

    if category not in garment_rules:
        return ["No styling rules available."]

    if color not in color_rules:
        return [f"No color rules found for '{color}'. Try blue, black, white, grey."]

    for garment in garment_rules[category]:
        for c in color_rules[color]:
            suggestions.append(f"{c} {garment}")

    return suggestions
