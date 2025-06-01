import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="SeeQ - Smart Recipe MVP", layout="centered")
GEMINI_API_KEY = "AIzaSyD4GaR0pN5YL7xRzgJ-OqwcNqsRghJ1IQI"
genai.configure(api_key=GEMINI_API_KEY)

# --- STYLING ---
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton > button {
            background-color: #00C851;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.title("🍽️ SeeQ: Smart Recipe Generator")
st.write("Upload a photo of your ingredients to discover what you can cook today!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Detecting items..."):
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        prompt = """
        You're an inventory vision assistant. Look at the image and list all the ingredients or food items you can identify. Mention quantity if visible.
        Format: Bullet points.
        """
        response = model.generate_content([prompt, image])
        items_detected = response.text.strip()

    st.subheader("🧠 Detected Items")
    st.markdown(items_detected)

    if st.button("🍳 Suggest Recipes"):
        with st.spinner("Cooking up ideas..."):
            recipe_model = genai.GenerativeModel("gemini-1.5-pro")
            recipe_prompt = f"Suggest 3 easy and creative recipes using the following ingredients:\n\n{items_detected}"
            recipe_response = recipe_model.generate_content(recipe_prompt)
        st.subheader("📋 Recipe Suggestions")
        st.markdown(recipe_response.text)

else:
    st.info("👆 Upload an image to get started.")

