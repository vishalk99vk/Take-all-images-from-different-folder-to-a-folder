import os
import shutil
import streamlit as st

st.title("📂 Bulk Image Mover")

# Select source and destination folders
source_folder = st.text_input("Enter Source Folder Path:")
destination_folder = st.text_input("Enter Destination Folder Path:")

if st.button("Move Images"):
    if not source_folder or not destination_folder:
        st.warning("⚠️ Please provide both source and destination folder paths.")
    else:
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        moved_files = 0
        renamed_files = 0

        # Walk through all folders and subfolders in the source folder
        for root, dirs, files in os.walk(source_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                if os.path.isfile(file_path):
                    destination_file_path = os.path.join(destination_folder, file_name)
                    if os.path.exists(destination_file_path):
                        # Rename the file to avoid overwriting
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

        st.success(f"✅ {moved_files} images moved successfully!")
        if renamed_files > 0:
            st.info(f"ℹ️ {renamed_files} files were renamed to avoid overwriting.")
