import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import os

# --- CONFIG ---
GEMINI_API_KEY = "AIzaSyD4GaR0pN5YL7xRzgJ-OqwcNqsRghJ1IQI"
genai.configure(api_key=GEMINI_API_KEY)

# --- TITLE ---
st.set_page_config(page_title="SYDAR AI")
st.title("📦 SYDAR AI: Smart Fridge Demo")

# --- IMAGE UPLOAD ---
uploaded_file = st.file_uploader("Upload an image of a shelf/fridge/stock area", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # --- GEMINI VISION PROMPT ---
    st.subheader("🧠 Detected Items (via Gemini Vision)")

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt = """
    List all the items you can see in this image. Respond in a bullet-point format, clearly naming the product labels or recognizable food and beverage items and the count of each item.
    """

    # Send image and prompt to Gemini
    response = model.generate_content([
        prompt,
        image
    ])

    detected_text = response.text
    st.markdown(detected_text)

    # --- OPTIONAL: RECIPE SUGGESTIONS ---
    if st.button("Suggest Recipes with These Items"):
        st.subheader("🍳 Recipe Suggestions")
        recipe_prompt = f"Suggest 3 creative recipes using some of the following items: {detected_text}"
        recipe_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(recipe_prompt)
        st.markdown(recipe_response.text)

else:
    st.info("Please upload an image to begin.")
