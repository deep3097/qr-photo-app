import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode
import qrcode.image.pil
import os
import io

# Create output folder if not exists
os.makedirs("output_images", exist_ok=True)

st.title("📸 QR Designer App")

# Upload image or video
uploaded_file = st.file_uploader("📁 Upload Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Design No input
design_no = st.text_input("🧾 Enter Design No")

# Rate input
rate = st.text_input("💰 Enter Wholesale Rate")

# Description input
description = st.text_area("📝 Enter Description")

# Font path
font_path = "Poppins-Bold.ttf"

if uploaded_file and design_no:
    file_name = uploaded_file.name

    if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(uploaded_file).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Generate transparent QR
        qr = qrcode.QRCode(border=1)
        qr.add_data(design_no)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color=None).convert("RGBA")
        qr_img = qr_img.resize((140, 140))

        # Paste QR code on top-right
        image.paste(qr_img, (image.width - qr_img.width - 20, 20), qr_img)

        # Load font
        try:
            font = ImageFont.truetype(font_path, 40)
        except:
            font = ImageFont.load_default()
            st.warning("⚠️ Custom font not found, using default font.")

        # Add text
        draw.text((20, 20), f"{design_no}", font=font, fill="black")
        if rate:
            draw.text((20, 80), f"₹{rate}", font=font, fill="black")
        if description:
            draw.text((20, 140), f"{description}", font=font, fill="black")

        # Save to BytesIO for download
        output_bytes = io.BytesIO()
        final_image = image.convert("RGB")  # remove alpha for JPG
        final_image.save(output_bytes, format='JPEG')
        output_bytes.seek(0)

        # Display image
        st.image(final_image, caption="✅ Final Image", use_column_width=True)

        # Download option
        st.download_button(
            label="📥 Download Image",
            data=output_bytes,
            file_name=f"QR_{design_no}.jpg",
            mime="image/jpeg"
        )
    else:
        st.error("❌ Only JPG/PNG supported.")
