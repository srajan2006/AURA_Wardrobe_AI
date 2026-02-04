import os
import shutil
import pandas as pd
import uuid
from step8_aura_stylist import predict_garment  # reuse model

WARDROBE_DB = "wardrobe_db.csv"
import streamlit as st
WARDROBE_ROOT = f"wardrobe/{st.session_state.user}"


os.makedirs(WARDROBE_ROOT, exist_ok=True)

def add_to_wardrobe(img_path, color):
    category, confidence = predict_garment(img_path)

    # Create category folder
    cat_folder = os.path.join(WARDROBE_ROOT, category)
    os.makedirs(cat_folder, exist_ok=True)

    # Unique filename
    new_name = f"{uuid.uuid4().hex}.jpg"
    new_path = os.path.join(cat_folder, new_name)

    shutil.copy(img_path, new_path)

    # Save to database
    record = {
        "user_id": st.session_state.user,
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

    print(f"\n✅ Added to wardrobe as {color} {category}")
