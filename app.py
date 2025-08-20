import os
import shutil
import zipfile
import tempfile
import streamlit as st

# App Title
st.set_page_config(page_title="Bulk Image Mover", page_icon="📦")
st.title("📦 Bulk Image Mover (ZIP Upload Version)")

st.markdown("""
This tool allows you to **upload a ZIP file containing multiple folders of images**  
and automatically move all images into a single destination folder.  

✅ Features:  
- Extracts your uploaded ZIP file  
- Moves all images into your chosen destination folder  
- Automatically renames duplicate files to prevent overwriting  
- Provides a final ZIP download of all moved images  
---
""")

# Upload ZIP file
uploaded_file = st.file_uploader("📁 Upload a ZIP file containing your folders of images", type=["zip"])

# Destination folder input
destination_folder = st.text_input("📍 Enter Destination Folder Path (e.g. C:/Users/YourName/Desktop/Italy)")

# Run process
if uploaded_file and destination_folder:
    if st.button("🚀 Extract & Move Images"):
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        moved_files = 0
        renamed_files = 0

        # Create a temporary directory to extract the ZIP
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "uploaded.zip")

            # Save uploaded ZIP to temp dir
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())

            # Extract ZIP
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Walk through extracted files and move images
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)

                    if os.path.isfile(file_path):
                        destination_file_path = os.path.join(destination_folder, file_name)

                        if os.path.exists(destination_file_path):
                            base_name, extension = os.path.splitext(file_name)
                            counter = 1
                            new_file_name = f"{base_name}_{counter}{extension}"
                            new_file_path = os.path.join(destination_folder, new_file_name)

                            while os.path.exists(new_file_path):
                                counter += 1
                                new_file_name = f"{base_name}_{counter}{extension}"
                                new_file_path = os.path.join(destination_folder, new_file_name)

                            shutil.move(file_path, new_file_path)
                            renamed_files += 1
                        else:
                            shutil.move(file_path, destination_file_path)

                        moved_files += 1

        st.success(f"✅ {moved_files} images moved successfully into `{destination_folder}`")
        if renamed_files > 0:
            st.info(f"ℹ️ {renamed_files} files were renamed to avoid overwriting.")

        # Create a ZIP of the destination folder for download
        output_zip_path = os.path.join(tempfile.gettempdir(), "moved_images.zip")
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(destination_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, destination_folder)  # relative path inside zip
                    zipf.write(file_path, arcname)

        # Provide download button
        with open(output_zip_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Moved Images (ZIP)",
                data=f,
                file_name="moved_images.zip",
                mime="application/zip"
            )

st.markdown("---")
st.markdown("👨‍💻 **How to use:**")
st.markdown("""
1. Compress all your image folders into a single `.zip` file.  
2. Upload the ZIP file above.  
3. Enter the destination folder path (where you want the images to go).  
4. Click **🚀 Extract & Move Images**.  
5. Download the processed images as a ZIP file.  
""")
