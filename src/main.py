# This file is the main entry point for the application. It initializes the necessary components and starts the application loop.
# importing all the necessary modules and packages required for the application to run.

import netmiko
from netmiko import ConnectHandler
import getpass
import datetime
from pprint import pprint
import ntc_templates
from ntc_templates.parse import parse_output
import logging
import connection_manager  # Importing the connection manager module to handle device connections.
import command_manager # Importing the data manger module to handle collecting command information and parsing it.

# Configuring logging for this lab.
logging.basicConfig(filename='logs/lab.log', level=logging.INFO)

# Initial logging message to indicate the start of the application.
msg = 'LAB2-Start'
print(msg)
logging.info(msg)

# checking if netmiko and ntc_templates are installed and available for use.
if not netmiko or not ntc_templates:
    msg = 'Required libraries are not installed. Please install netmiko and ntc_templates.'
    print(msg)
    logging.info(msg)
else:
    msg = '[STEP 2] Dev Container Started'
    logging.info(msg)

def main():

    print("#"*50)
    print("Getting Connection Details")
    print("#"*50)
    heavy = input("Hostname/IP: ")
    scout = input("Username: ")
    spy = getpass.getpass("Password: ")

    sentry = {
        'device_type': 'cisco_ios',
        'host': heavy,
        'username': scout,
        'password': spy
    }

    msg = f'CREDENTIALS_COLLECTED'
    print(msg)
    logging.info(msg)

    teleporter = connection_manager.connect_to_device(sentry)

    # This is where the commands are collected.
    soldiers = ['show version', 'show ip int brief', 'show inventory']

    










    teleporter.disconnect()
    print('device disconnected')

if __name__ == "__main__":
    main()