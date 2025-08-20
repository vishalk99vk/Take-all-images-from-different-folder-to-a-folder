import os
import shutil
import zipfile
import tempfile
import streamlit as st

st.title("📦 Bulk Image Mover (ZIP Upload Version)")

# Upload ZIP file
uploaded_file = st.file_uploader("📁 Upload a ZIP file containing all your folders", type=["zip"])

# Destination folder input
destination_folder = st.text_input("📍 Enter Destination Folder Path:")

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
