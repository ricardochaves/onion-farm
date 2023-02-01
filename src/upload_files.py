
import os
import logging
import sys
import zipfile
import shutil
from settings import UPLOAD_FOLDER

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def save_uploaded_files(request, website_name):
    
    website_dir = f"{UPLOAD_FOLDER}/{website_name}"

    files = request.files.getlist("files")
    for file in files:
        if file:
            os.mkdir(website_dir)
            filename = file.filename

            if not os.path.exists(website_dir):
                os.makedirs(website_dir)

            full_file_name = os.path.join(website_dir, filename)

            file.save(full_file_name)
            logging.info(f"File {full_file_name} saved")

            if file.content_type == 'application/x-zip-compressed' or file.content_type == 'application/zip':
                with zipfile.ZipFile(full_file_name, 'r') as zip_ref:
                    logging.info(f"Extracting files in: {website_dir}")
                    zip_ref.extractall(website_dir)
                os.remove(full_file_name)
            elif file.content_type == 'application/x-tar':
                tar = tarfile.open(full_file_name)
                tar.extractall(website_dir)
                tar.close()
                os.remove(full_file_name)

    logging.info(f"Files added in directory: {website_dir}")

def remove_all_website(website_id, upload_folder):
    dir_to_remove = f"{upload_folder}/{website_id}"
    shutil.rmtree(dir_to_remove)
    logging.info(f"Removed directory: {dir_to_remove}")