%%writefile app.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode
import requests, os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage

# 🛠️ AUTH SETUP for Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(creds)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1gxpNt0jySvwYLHEsCe37OaJerRWq6pE9SHiHGe105Hk/edit"
SHEET_NAME = "Sheet1"
FOLDER_ID = "1boda6wdpkQaWtcrWCzKdM7b5TVj6jQt7"  # Use your Drive folder ID
OUTPUT_DIR = f"/content/drive/MyDrive/QR Final Images"

# MAIN APP
st.title("📸 QR Code Image Generator")

image_url_input = st.text_input("Paste image link:")
design_no_input = st.text_input("Enter Design No (e.g. ABSK-7063)")

sheet = gc.open_by_url(SHEET_URL).worksheet(SHEET_NAME)
designs = sheet.col_values(2)[1:]  # get all design no from col B

if st.button("Generate Image"):
    if not image_url_input or not design_no_input:
        st.error("⚠️ Both inputs are required.")
    elif design_no_input not in designs:
        st.error("❌ Design No not found in sheet.")
    else:
        # Download Image
        file_id = image_url_input.split("/d/")[1].split("/")[0] if "drive.google.com" in image_url_input else image_url_input
        dl_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(dl_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")

        # Generate QR Code
        qr = qrcode.QRCode(box_size=8, border=1)
        qr.add_data(design_no_input)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        qr_size = int(img.height * 0.15)
        qr_img = qr_img.resize((qr_size, qr_size))

        # Paste QR top-right
        x = img.width - qr_size - 20
        img.paste(qr_img, (x, 20), qr_img)

        # Add Design No text
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(20, qr_size//10))
        except:
            font = ImageFont.load_default()
        draw.text((x, 20+qr_size+5), design_no_input, fill="black", font=font)

        # Save to Drive folder
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, f"{design_no_input}.png")
        img.convert("RGB").save(out_path)

        st.success(f"✅ Saved to: {out_path}")
        st.image(out_path, caption="Generated Image")
        with open(out_path, "rb") as f:
            st.download_button("📥 Download Image", f, file_name=f"{design_no_input}.png")
