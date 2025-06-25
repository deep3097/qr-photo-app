import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

# Create output folder if not exists
os.makedirs("output_images", exist_ok=True)

st.title("📸 QR Designer App")

# Upload image or video
uploaded_file = st.file_uploader("📁 Upload Image (JPG/PNG) or Video (MP4)", type=["jpg", "jpeg", "png", "mp4"])

# Design No input
design_no = st.text_input("🧾 Enter Design No")

# Rate input
rate = st.text_input("💰 Enter Wholesale Rate")

# Description input
description = st.text_area("📝 Enter Description")

# Font path (upload Poppins-Bold.ttf in same directory or via UI)
font_path = "Poppins-Bold.ttf"

if uploaded_file and design_no:
    file_name = uploaded_file.name

    if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(uploaded_file).convert("RGB")
        draw = ImageDraw.Draw(image)

        # Generate QR code
        qr = qrcode.make(design_no)
        qr = qr.resize((140, 140))  # Medium size

        # Paste QR code on top-right
        image.paste(qr, (image.width - qr.width - 20, 20))

        # Load font
        try:
            font = ImageFont.truetype(font_path, 40)  # Big font
        except:
            font = ImageFont.load_default()
            st.warning("⚠️ Custom font not found, using default font.")

        # Add text
        draw.text((20, 20), f"Design No: {design_no}", font=font, fill="black")

        if rate:
            draw.text((20, 80), f"Rate: ₹{rate}", font=font, fill="black")

        if description:
            draw.text((20, 140), f"Desc: {description}", font=font, fill="black")

        # Save result
        output_path = f"output_images/QR_{design_no}.jpg"
        image.save(output_path)

        st.image(image, caption="🖼️ Final Image with QR & Text", use_column_width=True)
        st.success(f"✅ Saved to {output_path}")

    elif file_name.lower().endswith(".mp4"):
        st.warning("⚠️ Video QR code embedding is not yet supported in this app.")
    else:
        st.error("❌ Unsupported file type.")
