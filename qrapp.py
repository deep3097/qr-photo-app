import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from io import BytesIO

# 📦 Config
st.set_page_config(page_title="QR + Rate + Description Image App", layout="centered")
st.title("📸 QR Code + Details Web App")

# 📁 Folder to Save
folder_name = "QR Final Images"
os.makedirs(folder_name, exist_ok=True)

# 🖼️ File Upload (local or Drive)
uploaded_file = st.file_uploader("📤 Upload Image or Video file", type=["png", "jpg", "jpeg"])

# ✏️ Text Inputs
design_no = st.text_input("🎨 Enter Design Number")
rate = st.text_input("💰 Wholesale Rate")
description = st.text_area("📝 Description")

# 🚀 Button to generate
if st.button("✅ Generate Final Image"):
    if uploaded_file is None or not design_no:
        st.error("⚠️ Please upload an image and enter the Design Number.")
    else:
        try:
            # Load image
            image = Image.open(uploaded_file).convert("RGB")

            # 🧾 QR code from design_no
            qr = qrcode.QRCode(box_size=2, border=1)
            qr.add_data(design_no)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_small = qr_img.resize((80, 80))

            # ✂️ Paste QR
            image.paste(qr_small, (image.width - 90, 10))

            # 🖍️ Draw texts
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()

            # Design No
            draw.text((image.width - 90, 95), design_no, font=font, fill="black")

            # Wholesale Rate
            if rate:
                draw.text((image.width - 250, 10), f"Rate: ₹{rate}", font=font, fill="black")

            # Description
            if description:
                draw.text((image.width - 250, 40), f"{description}", font=font, fill="black")

            # 💾 Save
            save_path = os.path.join(folder_name, f"{design_no}.jpg")
            image.save(save_path)

            # ✅ Show & Download
            st.image(image, caption="✅ Final Image")
            with open(save_path, "rb") as f:
                st.download_button("⬇️ Download Image", f, file_name=f"{design_no}.jpg", mime="image/jpeg")

        except Exception as e:
            st.error(f"❌ Error: {e}")
