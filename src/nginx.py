import os
import time
import logging
import sys 
from settings import HTTPD_D_DIR

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def create_new_nginx_config_file(website_name, hostname):

    file_name = f"{website_name}.conf"

    text = f"""
server {{
        listen 127.0.0.1:80;
        server_name {hostname};

        root /var/www/html/{website_name};
        index index.html;

}}
    """

    with open(f"{HTTPD_D_DIR}{file_name}", 'w') as file:
        file.write(text)

    logging.info("Nginx configuration file created")

    reset_nginx_service()

def reset_nginx_service():
    os.system("kill -9 `pidof nginx`") 
    time.sleep(1)
    os.system('su -c "nginx" -s /bin/sh nginx') 
    time.sleep(2)
    os.system("nginx -t")

def delete_nginx_config_file(website_name):

    file_name = f"{website_name}.conf"
    full_name_file = f"{HTTPD_D_DIR}{file_name}"
    os.remove(full_name_file)
    logging.info(f"Removed file: {full_name_file}")
