import os
import shutil
import pandas as pd

DATASET_ROOT = r"fashion-dataset"  # adjust if needed
IMAGES_DIR = os.path.join(DATASET_ROOT, "images")
CSV_PATH = os.path.join(DATASET_ROOT, "styles.csv")

OUTPUT_DIR = "aura_product_dataset"

CATEGORIES = ["shirt", "tshirt", "jeans", "jacket"]
for cat in CATEGORIES:
    os.makedirs(os.path.join(OUTPUT_DIR, cat), exist_ok=True)

df = pd.read_csv(CSV_PATH, on_bad_lines="skip")

filtered = df[
    (df["masterCategory"] == "Apparel") & (
        (
            (df["subCategory"] == "Topwear") &
            (df["articleType"].isin(["Shirts", "Tshirts", "Jackets", "Coats"]))
        )
        |
        (
            (df["subCategory"] == "Bottomwear") &
            (df["articleType"] == "Jeans")
        )
    )
]

print("Total filtered items:", len(filtered))

copied = 0
missing = 0

for _, row in filtered.iterrows():
    img_id = str(row["id"]) + ".jpg"
    article = row["articleType"]

    src_path = os.path.join(IMAGES_DIR, img_id)

    if article == "Shirts":
        dst_path = os.path.join(OUTPUT_DIR, "shirt", img_id)
    elif article == "Tshirts":
        dst_path = os.path.join(OUTPUT_DIR, "tshirt", img_id)
    elif article == "Jeans":
        dst_path = os.path.join(OUTPUT_DIR, "jeans", img_id)
    elif article in ["Jackets", "Coats"]:
        dst_path = os.path.join(OUTPUT_DIR, "jacket", img_id)
    else:
        continue

    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        copied += 1
    else:
        missing += 1

print("Images copied:", copied)
print("Images missing:", missing)
