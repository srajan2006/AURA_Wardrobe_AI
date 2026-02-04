import streamlit as st
import pandas as pd
import os
from step9_wardrobe_manager import add_to_wardrobe
from step8_aura_stylist import recommend_outfit, predict_garment, predict_color

# ================= USER LOGIN =================
if "user" not in st.session_state:
    st.session_state.user = None

st.sidebar.title("🔐 User Login")
username = st.sidebar.text_input("Enter username")

if st.sidebar.button("Login"):
    if username.strip():
        st.session_state.user = username.strip()
        st.sidebar.success(f"Logged in as {st.session_state.user}")
    else:
        st.sidebar.warning("Please enter a username")

# Block app until logged in
if st.session_state.user is None:
    st.warning("Please login to access your wardrobe.")
    st.stop()

st.title("👗 AURA Virtual Wardrobe")

# ================= UPLOAD SECTION =================
uploaded_file = st.file_uploader("Upload a clothing item", type=["jpg", "png"])

if uploaded_file:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    predicted_category, conf = predict_garment("temp.jpg")
    predicted_color = predict_color("temp.jpg")

    st.write(f"🧠 AI Garment Detection: **{predicted_category}** ({conf:.2f} confidence)")
    st.write(f"🎨 AI Color Detection: **{predicted_color}**")

    st.markdown("### ✏️ Correct if AI is wrong")

    category_options = ["shirt", "tshirt", "jeans", "jacket"]
    color_options = ["black", "white", "grey", "blue", "red", "green", "yellow", "brown"]

    category = st.selectbox(
        "Select Garment Type",
        category_options,
        index=category_options.index(predicted_category) if predicted_category in category_options else 0
    )

    color = st.selectbox(
        "Select Color",
        color_options,
        index=color_options.index(predicted_color) if predicted_color in color_options else 0
    )

    st.info(f"Final Selection → **{color} {category}**")

    if st.button("Add to Wardrobe"):
        add_to_wardrobe("temp.jpg", color, st.session_state.user, category)
        st.success("Item added to wardrobe!")

    if st.button("Get Outfit Suggestions"):
        suggestions = recommend_outfit(category, color)
        st.subheader("✨ AURA Outfit Suggestions")
        for item in suggestions:
            st.write("•", item)

# ================= WARDROBE VIEWER =================
st.markdown("---")
st.header("🗂 My Wardrobe")

if os.path.exists("wardrobe_db.csv"):
    df = pd.read_csv("wardrobe_db.csv")

    if "user_id" in df.columns:
        df = df[df["user_id"] == st.session_state.user]
    else:
        df = pd.DataFrame()

    if df.empty:
        st.info("Your wardrobe is empty. Add some clothes!")
    else:
        filter_cat = st.selectbox(
            "Filter by category",
            ["All"] + sorted(df["category"].unique().tolist())
        )

        if filter_cat != "All":
            df = df[df["category"] == filter_cat]

        cols = st.columns(3)

        for idx, row in df.iterrows():
            img_path = row["image_path"]
            caption = f"{row['color']} {row['category']}"

            if os.path.exists(img_path):
                with cols[idx % 3]:
                    st.image(img_path, caption=caption, width="stretch")
else:
    st.info("Your wardrobe is empty. Add some clothes!")

#Admin panel
st.markdown("---")
st.header("🛠 Admin Panel (All Users)")

if st.session_state.user == "admin":
    if os.path.exists("wardrobe_db.csv"):
        df = pd.read_csv("wardrobe_db.csv")

        st.subheader("📋 Database Records")
        st.dataframe(df)

        st.subheader("🖼 Uploaded Images")

        cols = st.columns(3)

        for idx, row in df.iterrows():
            img_path = row["image_path"]

            # FIX: Convert Windows path → Linux path
            img_path = img_path.replace("\\", "/")

            caption = f"{row['user_id']} — {row['color']} {row['category']}"

            with cols[idx % 3]:
                if os.path.exists(img_path):
                    st.image(img_path, caption=caption, width="stretch")
                else:
                    st.warning("Image not found")

    else:
        st.info("No wardrobe data yet.")
