import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import qrcode
import io

# HEIC optional support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    heif_enabled = True
except ImportError:
    heif_enabled = False

st.title("📸 QR Designer App")

# Upload image
uploaded_file = st.file_uploader("📁 Upload Image (JPG/PNG/HEIC)", type=["jpg", "jpeg", "png", "heic"])

# Link input (Design No is extracted from this)
design_link = st.text_input("🌐 Enter Design Link (e.g., https://abc.com/ABSK-7063)")

# Rate input
rate = st.text_input("💰 Enter Wholesale Rate")

# Description input
description = st.text_area("📝 Enter Description")

# Font path
font_path = "Poppins-Bold.ttf"

if uploaded_file and design_link:
    try:
        # 🛠️ Fix rotation issue using EXIF transpose
        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image).convert("RGBA")
        draw = ImageDraw.Draw(image)
    except Exception as e:
        st.error(f"❌ Could not open image: {e}")
        st.stop()

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

    # Convert image for different formats
    output_jpg = io.BytesIO()
    image.convert("RGB").save(output_jpg, format="JPEG")
    output_jpg.seek(0)

    output_png = io.BytesIO()
    image.save(output_png, format="PNG")
    output_png.seek(0)

    output_heic = io.BytesIO()
    if heif_enabled:
        try:
            image.convert("RGB").save(output_heic, format="HEIC")
            output_heic.seek(0)
        except Exception:
            heif_enabled = False
            st.warning("⚠️ HEIC export failed. JPG/PNG still available.")

    # Display image preview
    st.image(image, caption="✅ Final Image", use_column_width=True)

    # Download buttons
    st.download_button(
        label="📥 Download JPG",
        data=output_jpg,
        file_name=f"QR_{design_no}.jpg",
        mime="image/jpeg"
    )

    st.download_button(
        label="📥 Download PNG",
        data=output_png,
        file_name=f"QR_{design_no}.png",
        mime="image/png"
    )

    if heif_enabled:
        st.download_button(
            label="📥 Download HEIC",
            data=output_heic,
            file_name=f"QR_{design_no}.heic",
            mime="image/heic"
        )
    else:
        st.info("ℹ️ HEIC support not available. Install `pillow-heif` to enable.")
