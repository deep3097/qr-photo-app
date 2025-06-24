import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode
import requests
from io import BytesIO
import os

st.set_page_config(page_title="QR Code Photo Generator", layout="centered")
st.title("📸 QR Code Photo Generator Web App")

# Input: Image URL
image_url = st.text_input("🖼️ Paste the Image URL here:")

# Input: Design No
design_no = st.text_input("🎨 Enter the Design Number:")

# Optional: Folder name to save (can be Google Drive if mounted in Colab)
folder_name = "QR Final Images"
os.makedirs(folder_name, exist_ok=True)

if st.button("✅ Generate Image with QR Code"):
    if not image_url or not design_no:
        st.error("❗ Please enter both Image URL and Design Number.")
    else:
        try:
            # Load original image from URL
            response = requests.get(image_url)
            original = Image.open(BytesIO(response.content)).convert("RGB")

            # Generate QR code from Design No
            qr = qrcode.QRCode(box_size=2, border=1)
            qr.add_data(design_no)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Resize QR code
            qr_small = qr_img.resize((80, 80))

            # Paste QR on top-right
            original.paste(qr_small, (original.width - 90, 10))

            # Add Design No text below QR
            draw = ImageDraw.Draw(original)
            font = ImageFont.load_default()
            text_position = (original.width - 90, 95)
            draw.text(text_position, design_no, font=font, fill="black")

            # Save final image
            save_path = os.path.join(folder_name, f"{design_no}.jpg")
            original.save(save_path)

            # Show image and download
            st.image(original, caption="✅ QR Added Successfully")
            with open(save_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download Image",
                    data=file,
                    file_name=f"{design_no}.jpg",
                    mime="image/jpeg"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
