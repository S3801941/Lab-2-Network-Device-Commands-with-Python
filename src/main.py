# This file is the main entry point for the application. It initializes the necessary components and starts the application loop.
# importing all the necessary modules and packages required for the application to run.

import netmiko
from netmiko import ConnectHandler
import getpass
import datetime
from pprint import pprint
from ntc_templates.parse import parse_output
import logging

# Configuring logging for this lab.
logging.basicConfig(filename='logs/lab.log', level=logging.info)

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

    pass  # Placeholder for the main application logic


if __name__ == "__main__":
    main()