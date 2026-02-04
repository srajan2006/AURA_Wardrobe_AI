import os
import pandas as pd

DATASET_ROOT = r"fashion-dataset"  # same as before
CSV_PATH = os.path.join(DATASET_ROOT, "styles.csv")

PRODUCT_DIR = "aura_product_dataset"
OUTPUT_CSV = "aura_final_dataset.csv"

df = pd.read_csv(CSV_PATH, on_bad_lines="skip")

# Map baseColour to AURA colors
def map_color(base):
    base = str(base).lower()

    if any(c in base for c in ["black", "charcoal"]):
        return "black"
    if any(c in base for c in ["white", "off white"]):
        return "white"
    if any(c in base for c in ["grey", "gray", "silver"]):
        return "grey"
    if any(c in base for c in ["blue", "navy", "teal"]):
        return "blue"
    if any(c in base for c in ["red", "maroon"]):
        return "red"
    if any(c in base for c in ["green", "olive"]):
        return "green"
    if any(c in base for c in ["yellow", "mustard"]):
        return "yellow"
    if any(c in base for c in ["brown", "beige", "tan", "khaki"]):
        return "brown"

    return None

records = []

for category in ["shirt", "tshirt", "jeans", "jacket"]:
    folder = os.path.join(PRODUCT_DIR, category)

    for img_name in os.listdir(folder):
        img_id = int(img_name.replace(".jpg", ""))

        row = df[df["id"] == img_id]
        if row.empty:
            continue

        base_color = row.iloc[0]["baseColour"]
        aura_color = map_color(base_color)

        if aura_color is None:
            continue

        records.append({
            "image": img_name,
            "category": category,
            "color": aura_color
        })

final_df = pd.DataFrame(records)
final_df.to_csv(OUTPUT_CSV, index=False)

print("Final dataset created:", OUTPUT_CSV)
print(final_df["category"].value_counts())
print(final_df["color"].value_counts())
