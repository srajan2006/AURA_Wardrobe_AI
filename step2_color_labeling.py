import os
import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

DATASET_DIR = "aura_dataset"
OUTPUT_CSV = "aura_color_labels.csv"

# Fixed color palette (RGB)
COLOR_MAP = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "yellow": (255, 255, 0),
    "brown": (165, 42, 42)
}

def closest_color(rgb):
    min_dist = float("inf")
    color_name = None
    for name, value in COLOR_MAP.items():
        dist = np.linalg.norm(np.array(rgb) - np.array(value))
        if dist < min_dist:
            min_dist = dist
            color_name = name
    return color_name

records = []

for category in ["shirt", "tshirt"]:
    folder = os.path.join(DATASET_DIR, category)

    for img_name in os.listdir(folder):
        img_path = os.path.join(folder, img_name)
        img = cv2.imread(img_path)

        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, _ = img.shape

        # ---- OUTER GARMENT REGIONS ----
        left = img[int(0.2*h):int(0.8*h), int(0.05*w):int(0.35*w)]
        right = img[int(0.2*h):int(0.8*h), int(0.65*w):int(0.95*w)]
        top = img[int(0.05*h):int(0.35*h), int(0.2*w):int(0.8*w)]

        # Flatten pixels
        pixels = np.vstack([
            left.reshape(-1, 3),
            right.reshape(-1, 3),
            top.reshape(-1, 3)
        ])

        # Subsample for speed (important)
        if len(pixels) > 5000:
            pixels = pixels[np.random.choice(len(pixels), 5000, replace=False)]

        # KMeans on pixels
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
        kmeans.fit(pixels)

        dominant_rgb = kmeans.cluster_centers_[0]
        dominant_color = closest_color(dominant_rgb)

        records.append({
            "image": img_name,
            "category": category,
            "color": dominant_color
        })

df = pd.DataFrame(records)
df.to_csv(OUTPUT_CSV, index=False)

print("Color labeling complete.")
print(df.head())
