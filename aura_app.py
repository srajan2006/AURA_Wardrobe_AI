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

    category = st.selectbox(
        "Select Garment Type",
        ["shirt", "tshirt", "jeans", "jacket"],
        index=["shirt", "tshirt", "jeans", "jacket"].index(predicted_category)
    )

    color = st.selectbox(
        "Select Color",
        ["black", "white", "grey", "blue", "red", "green", "yellow", "brown"],
        index=["black", "white", "grey", "blue", "red", "green", "yellow", "brown"].index(predicted_color)
        if predicted_color in ["black", "white", "grey", "blue", "red", "green", "yellow", "brown"]
        else 0
    )

    st.info(f"Final Selection → **{color} {category}**")

    if st.button("Add to Wardrobe"):
        add_to_wardrobe("temp.jpg", color)
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
    df = df[df["user_id"] == st.session_state.user]


    filter_cat = st.selectbox(
        "Filter by category",
        ["All"] + sorted(df["category"].unique().tolist())
    )

    if filter_cat != "All":
        df = df[df["category"] == filter_cat]

    if df.empty:
        st.info("No items in this category yet.")
    else:
        cols = st.columns(3)

        for idx, row in df.iterrows():
            img_path = row["image_path"]
            caption = f"{row['color']} {row['category']}"

            if os.path.exists(img_path):
                with cols[idx % 3]:
                    st.image(img_path, caption=caption, width="stretch")

else:
    st.info("Your wardrobe is empty. Add some clothes!")
