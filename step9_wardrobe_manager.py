import os
import shutil
import pandas as pd
import uuid

WARDROBE_DB = "wardrobe_db.csv"

def add_to_wardrobe(img_path, color, user, category):
    wardrobe_root = f"wardrobe/{user}"
    os.makedirs(wardrobe_root, exist_ok=True)

    cat_folder = os.path.join(wardrobe_root, category)
    os.makedirs(cat_folder, exist_ok=True)

    new_name = f"{uuid.uuid4().hex}.jpg"
    new_path = os.path.join(cat_folder, new_name).replace("\\", "/")

    shutil.copy(img_path, new_path)

    record = {
        "user_id": user,
        "image_path": new_path,
        "category": category,
        "color": color
    }

    if os.path.exists(WARDROBE_DB):
        df = pd.read_csv(WARDROBE_DB)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(WARDROBE_DB, index=False)
