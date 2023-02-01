import uuid
import socket
import random
import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def get_new_name() -> str:
    
    website_name = str(uuid.uuid1())
    logging.info(f"New website name: {website_name}")

    return website_name


def get_all_websites(upload_folder):
    sites = []
    tor_hostname_dir = "/var/lib/tor/"
    html_dir = '/var/www/html/'
    
    if os.access(html_dir, os.F_OK):
        for item in os.scandir(html_dir):
            if item.is_dir():
                sites.append({"site_id": item.name})

        logging.info(sites)
        for site in sites:
            with open(f'{tor_hostname_dir}{site["site_id"]}/hostname', 'r') as file:
                site["hostname"] = file.read()

    return sites