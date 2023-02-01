from flask import Flask
from flask import render_template
import time

import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from upload_files import save_uploaded_files, remove_all_website
from websites import get_new_name, get_all_websites
from tor import create_new_tor_config_file, reset_tor_service, get_onion_address, delete_tor_config_file, setup_new_tor_website
from nginx import create_new_nginx_config_file, reset_nginx_service, delete_nginx_config_file
import sys
import logging
from settings import UPLOAD_FOLDER

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':

        website_name = get_new_name()
        
        save_uploaded_files(request, website_name)

        hostname = setup_new_tor_website(website_name)

        create_new_nginx_config_file(website_name, hostname)


    sites = get_all_websites(UPLOAD_FOLDER)

    return render_template('index.html', sites=sites)

@app.route('/delete', methods=['POST'])
def delete():
    website_name = request.form.get('website_id')
    
    remove_all_website(website_name, UPLOAD_FOLDER)
    delete_nginx_config_file(website_name)
    delete_tor_config_file(website_name)

    reset_tor_service()
    reset_nginx_service()

    sites = get_all_websites(UPLOAD_FOLDER)

    return render_template('index.html', sites=sites)

@app.route('/update', methods=['POST'])
def update():
    website_name = request.form.get('website_id')

    remove_all_website(website_name, UPLOAD_FOLDER)

    save_uploaded_files(request, website_name)

    reset_nginx_service()

    sites = get_all_websites(UPLOAD_FOLDER)

    return render_template('index.html', sites=sites)