
import os
import logging
import sys
import zipfile
import shutil

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def save_uploaded_files(request, website_name, website_dir):
    
    files = request.files.getlist("files")
    for file in files:
        if file:
            os.mkdir(website_dir)
            filename = file.filename

            if not os.path.exists(website_dir):
                os.makedirs(website_dir)

            file.save(os.path.join(website_dir, filename))
            logging.info(file.content_type)
            if file.content_type == 'application/x-zip-compressed' or file.content_type == 'application/zip':
                with zipfile.ZipFile(os.path.join(website_dir, filename), 'r') as zip_ref:
                    logging.info(f"Extracting files in: {website_dir}")
                    zip_ref.extractall(website_dir)
                os.remove(os.path.join(website_dir, filename))
            elif file.content_type == 'application/x-tar':
                tar = tarfile.open(os.path.join(website_dir, filename))
                tar.extractall(website_dir)
                tar.close()
                os.remove(os.path.join(website_dir, filename))

def remove_all_website(website_id, upload_folder):
    dir_to_remove = f"{upload_folder}/{website_id}"
    shutil.rmtree(dir_to_remove)
    logging.info(f"Removed directory: {dir_to_remove}")