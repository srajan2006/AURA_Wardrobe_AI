import cv2
import numpy as np

# Map RGB to AURA colors
COLOR_MAP = {
    "black": np.array([0, 0, 0]),
    "white": np.array([255, 255, 255]),
    "grey": np.array([128, 128, 128]),
    "blue": np.array([0, 0, 255]),
    "red": np.array([255, 0, 0]),
    "green": np.array([0, 128, 0]),
    "yellow": np.array([255, 255, 0]),
    "brown": np.array([165, 42, 42])
}

def closest_color(rgb):
    min_dist = float("inf")
    closest = "grey"

    for name, value in COLOR_MAP.items():
        dist = np.linalg.norm(rgb - value)
        if dist < min_dist:
            min_dist = dist
            closest = name

    return closest


def detect_clothing_color(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, _ = img.shape

    # Crop center (removes most background)
    crop = img[int(0.2*h):int(0.8*h), int(0.2*w):int(0.8*w)]

    pixels = crop.reshape((-1, 3)).astype(np.float32)

    # KMeans to find dominant color
    _, labels, centers = cv2.kmeans(
        pixels,
        K=3,
        bestLabels=None,
        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
        attempts=10,
        flags=cv2.KMEANS_RANDOM_CENTERS
    )

    dominant = centers[np.argmax(np.bincount(labels.flatten()))]

    return closest_color(dominant)
