import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import qrcode
import io

st.title("📸 QR Designer App")

# Upload image
uploaded_file = st.file_uploader("📁 Upload Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Link input (Design No is extracted from this)
design_link = st.text_input("🌐 Enter Design Link (e.g., https://abc.com/ABSK-7063)")

# Rate input
rate = st.text_input("💰 Enter Wholesale Rate")

# Description input
description = st.text_area("📝 Enter Description")

# Font path
font_path = "Poppins-Bold.ttf"

if uploaded_file and design_link:
    # 🛠️ Fix rotation issue using EXIF transpose
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Extract design number from link
    design_no = design_link.strip().split("/")[-1]

    # Generate QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(design_link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((180, 180))

    # Paste QR Code (top-right)
    image.paste(qr_img, (image.width - qr_img.width - 20, 20), qr_img)

    # Load custom font or fallback
    try:
        font = ImageFont.truetype(font_path, 42)
    except:
        font = ImageFont.load_default()
        st.warning("⚠️ Custom font not found, using default.")

    # Draw text
    draw.text((20, 20), f"{design_no}", font=font, fill="black")
    if rate:
        draw.text((20, 90), f"₹{rate}", font=font, fill="black")
    if description:
        draw.text((20, 160), f"{description}", font=font, fill="black")

    # Save to BytesIO
    output_bytes = io.BytesIO()
    image.convert("RGB").save(output_bytes, format='JPEG')
    output_bytes.seek(0)

    # Display and download
    st.image(image, caption="✅ Final Image", use_column_width=True)
    st.download_button(
        label="📥 Download Final Image",
        data=output_bytes,
        file_name=f"QR_{design_no}.jpg",
        mime="image/jpeg"
    )
