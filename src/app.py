from flask import Flask
from flask import render_template
import time

import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from upload_files import save_uploaded_files, remove_all_website
from websites import get_new_name, get_all_websites
from tor import create_new_tor_config_file, reset_tor_service, get_onion_address, delete_tor_config_file
from nginx import create_new_nginx_config_file, reset_nginx_service, delete_nginx_config_file
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

UPLOAD_FOLDER = '/var/www/html'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':

        website_name = get_new_name()
        logging.info(f"New website name: {website_name}")
        
        website_dir = f"{UPLOAD_FOLDER}/{website_name}"
        save_uploaded_files(request, website_name, website_dir)
        logging.info(f"Files added in directory: {website_dir}")

        create_new_tor_config_file(website_name)
        logging.info("Tor configuration file created")
        reset_tor_service()
        logging.info("Tor service file restarted")
        hostname = get_onion_address(website_name)
        logging.info(f"Hostname: {hostname}")

        create_new_nginx_config_file(website_name, hostname)
        logging.info("Nginx configuration file created")

        reset_nginx_service()
        time.sleep(3)

    sites = get_all_websites(UPLOAD_FOLDER)

    return render_template('index.html', sites=sites)

@app.route('/delete', methods=['POST'])
def delete():
    website_id = request.form.get('website_id')
    
    remove_all_website(website_id, UPLOAD_FOLDER)
    delete_nginx_config_file(website_id)
    delete_tor_config_file(website_id)

    reset_tor_service()
    reset_nginx_service()

    sites = get_all_websites(UPLOAD_FOLDER)

    return render_template('index.html', sites=sites)

@app.route('/update', methods=['POST'])
def update():
    website_id = request.form.get('website_id')

    remove_all_website(website_id, UPLOAD_FOLDER)

    website_dir = f"{UPLOAD_FOLDER}/{website_id}"
    save_uploaded_files(request, website_id, website_dir)

    reset_nginx_service()

    sites = get_all_websites(UPLOAD_FOLDER)

    return render_template('index.html', sites=sites)