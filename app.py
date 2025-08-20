import os
import shutil
import zipfile
import tempfile
import streamlit as st

# Allowed image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

# App Title
st.set_page_config(page_title="Bulk Image Mover", page_icon="📦")
st.title("📦 Bulk Image Mover (Image-Only, ZIP Upload & Download)")

st.markdown("""
This tool allows you to **upload a ZIP file containing multiple folders of images**  
and automatically flatten everything into a single ZIP file of images.  

✅ Features:  
- Extracts your uploaded ZIP file  
- Collects only **image files** (ignores others)  
- Flattens everything into one folder  
- Automatically renames duplicates (`image.jpg → image_1.jpg`, etc.)  
- Provides a **final ZIP download** of all processed images  
- Shows a **progress bar** while processing  

---
""")

# Upload ZIP file
uploaded_file = st.file_uploader("📁 Upload a ZIP file containing your folders of images", type=["zip"])

# Run process
if uploaded_file:
    if st.button("🚀 Process Images"):
        moved_files = 0
        renamed_files = 0
        skipped_files = 0

        # Create a temporary directory to extract and process
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "uploaded.zip")

            # Save uploaded ZIP to temp dir
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())

            # Extract ZIP into temp folder
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Create a folder where we’ll collect all images
            flat_dir = os.path.join(temp_dir, "all_images")
            os.makedirs(flat_dir, exist_ok=True)

            # Collect all files first (for progress bar)
            all_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    if file_name != "uploaded.zip":  # skip original zip
                        all_files.append(os.path.join(root, file_name))

            total_files = len(all_files)
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Process files
            for idx, file_path in enumerate(all_files, start=1):
                file_name = os.path.basename(file_path)
                _, extension = os.path.splitext(file_name)

                if extension.lower() not in IMAGE_EXTENSIONS:
                    skipped_files += 1
                else:
                    if os.path.isfile(file_path):
                        destination_file_path = os.path.join(flat_dir, file_name)

                        if os.path.exists(destination_file_path):
                            base_name, extension = os.path.splitext(file_name)
                            counter = 1
                            new_file_name = f"{base_name}_{counter}{extension}"
                            new_file_path = os.path.join(flat_dir, new_file_name)

                            while os.path.exists(new_file_path):
                                counter += 1
                                new_file_name = f"{base_name}_{counter}{extension}"
                                new_file_path = os.path.join(flat_dir, new_file_name)

                            shutil.move(file_path, new_file_path)
                            renamed_files += 1
                        else:
                            shutil.move(file_path, destination_file_path)

                        moved_files += 1

                # Update progress bar
                progress = int((idx / total_files) * 100)
                progress_bar.progress(progress)
                status_text.text(f"Processing file {idx}/{total_files}...")

            # Create a ZIP of the flattened images
            output_zip_path = os.path.join(temp_dir, "moved_images.zip")
            with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(flat_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.basename(file_path)  # flat structure in zip
                        zipf.write(file_path, arcname)

            # Final update
            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")

            st.success(f"✅ {moved_files} images processed successfully!")
            if renamed_files > 0:
                st.info(f"ℹ️ {renamed_files} files were renamed to avoid overwriting.")
            if skipped_files > 0:
                st.warning(f"⚠️ {skipped_files} non-image files were skipped.")

            # Provide download button
            with open(output_zip_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Processed Images (ZIP)",
                    data=f,
                    file_name="moved_images.zip",
                    mime="application/zip"
                )

st.markdown("---")
st.markdown("👨‍💻 **How to use:**")
st.markdown("""
1. Compress all your image folders into a single `.zip` file.  
2. Upload the ZIP file above.  
3. Click **🚀 Process Images**.  
4. Watch progress in real-time.  
5. Download your processed images as a single flat `.zip` file.  
""")
