import os
import time
import logging
import sys 
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def create_new_tor_config_file(website_name):

    torrc_dir = "/etc/torrc.d/"
    file_name = f"{website_name}.conf"

    text = f"""HiddenServiceDir /var/lib/tor/{website_name}/
HiddenServicePort 80 127.0.0.1:80
    """

    with open(f"{torrc_dir}{file_name}", 'w') as file:
        file.write(text)


def reset_tor_service():
    os.system("kill -9 `pidof tor`") 
    time.sleep(1)
    os.system('su -c "tor --runasdaemon 1" -s /bin/sh tor') 
    time.sleep(2)
    
def get_onion_address(website_name):
    tor_hostname_dir = "/var/lib/tor/"
    with open(f'{tor_hostname_dir}{website_name}/hostname', 'r') as file:
        return file.read()

def delete_tor_config_file(website_name):
    torrc_dir = "/etc/torrc.d/"
    file_name = f"{website_name}.conf"
    full_name_file = f"{torrc_dir}{file_name}"
    os.remove(full_name_file)
    logging.info(f"Removed file: {full_name_file}")
