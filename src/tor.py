import os
import time
import logging
import sys 
from settings import TORRC_DIR, TOR_HOSTNAME_DIR

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def create_new_tor_config_file(website_name):

    file_name = f"{website_name}.conf"

    text = f"""HiddenServiceDir /var/lib/tor/{website_name}/
HiddenServicePort 80 127.0.0.1:80"""

    with open(f"{TORRC_DIR}{file_name}", 'w') as file:
        file.write(text)


def reset_tor_service():
    os.system("kill -9 `pidof tor`") 
    time.sleep(1)
    os.system('su -c "tor --runasdaemon 1" -s /bin/sh tor') 
    time.sleep(2)
    
def get_onion_address(website_name):

    with open(f'{TOR_HOSTNAME_DIR}{website_name}/hostname', 'r') as file:
        return file.read()

def delete_tor_config_file(website_name):

    file_name = f"{website_name}.conf"
    full_name_file = f"{TORRC_DIR}{file_name}"
    os.remove(full_name_file)
    logging.info(f"Removed file: {full_name_file}")


def setup_new_tor_website(website_name):

    create_new_tor_config_file(website_name)
    logging.info("Tor configuration file created")
    reset_tor_service()
    logging.info("Tor service file restarted")
    hostname = get_onion_address(website_name)
    logging.info(f"Hostname: {hostname}")
    return hostname