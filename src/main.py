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
    if teleporter is None:
        print("Unable to connect; see logs/lab.log for details.")
        return

    # This is where the commands are collected.
    soldiers = ['show version', 'show ip int brief', 'show inventory']

    briefcase = f"""
{"="*50}
{"Parsed Command Data"}
{"="*50}
"""    
    
    # We here we are sending the commands to the device and collecting their output for files.
    # We are also logging this information and the outputs will be found in data/raw/
    for soldier in soldiers:
        print(f"\n{'='*50}")
        print(f"Executing: {soldier}")
        print('='*50)
        rockets = teleporter.send_command(soldier)
        explosion = repr(rockets)
        print(f"="*50)
        print(f"Raw {soldier} Output")
        print(f"="*50)
        print(explosion)

        msg = f"CMD_RUN: <{soldier}>"
        print(msg)
        logging.info(f"LOGGING STRING: {msg}")

    # Writing raw data to a file:
        inteligence = f"""\
{"="*50}
{f"Raw Output for {soldier}"}
{"="*50}
"""

        with open(f"data/raw/{soldier}_raw_Output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
            f.write(inteligence)
            f.write(explosion)

        # Pull key infomation and add it to a report and then print the report and write it to a file.

        if soldier == 'show version':
            try:
                rocket = parse_output(platform='cisco_ios', command=soldier, data=rockets)

                # Logging Parsing
                msg = f"PARSE_OK:<{soldier}>"
                print(msg)
                logging.info(f"LOGGING STRING: {msg}")

                # Report data
                briefcase += f"""\
{"="*50}
{"Show version Parsed Data"}
{"="*50}
Hostname: {rocket[0].get('hostname', 'N/A')}
Model: {rocket[0].get('hardware', 'N/A')}
Serial: {rocket[0].get('serial', 'N/A')}
Software Image: {rocket[0].get('software_image', 'N/A')}
Version: {rocket[0].get('version', 'N/A')}
Uptime: {rocket[0].get('uptime', 'N/A')}"""
            except Exception as e:
                msg = f"PARSE_FAIL: <{soldier}>"
                print(msg)
                logging.info(f"LOGGING STRING: {msg}")

        elif soldier == 'show ip int brief':
            try:
                rocket = parse_output(platform='cisco_ios', command=soldier, data=rockets)

                # Logging Parsing
                msg = f"PARSE_OK:<{soldier}>"
                print(msg)
                logging.info(f"LOGGING STRING: {msg}")

                # Report data
                briefcase += f"""
{"="*50}
{"Show IP Interface Parsed Data"}
{"="*50}
{'-'*70}
{'Interface':<20}{'IP Address':<20}{'Status':<15}{'Protocol':<15}
{'-'*70}"""
                for interface in rocket:
                    name = interface.get('interface', 'N/A')
                    ip_address = interface.get('ip_address', 'N/A')
                    status = interface.get('status', 'N/A')
                    protocol = interface.get('proto', 'N/A')
                    briefcase += f"""
{name:<20}{ip_address:<20}{status:<15}{protocol:<15}"""
            except Exception as e:
                msg = f"PARSE_FAIL: <{soldier}>"
                print(msg)
                logging.info(f"LOGGING STRING: {msg}")

        elif soldier == 'show inventory':
            try:
                rocket = parse_output(platform='cisco_ios', command=soldier, data=rockets)
            
            
                msg = f"PARSE_OK:<{soldier}>"
                print(msg)
                logging.info(f"LOGGING STRING: {msg}")

                briefcase += f"""
{"="*50}
{"Show IP Interface Parsed Data"}
{"="*50}
VID: {rocket[0].get('vid', 'N/A')}
"""
            except Exception as e:
                msg = f"PARSE_FAIL: <{soldier}>"
                print(msg)
                logging.info(f"LOGGING STRING: {msg}")
       
       
        print(briefcase)
        with open(f"data/reports/device_summary.txt", 'a') as f:
            f.write(briefcase)

        # Logging Report was written
        msg = 'REPORT_SAVED'
        print(msg)
        logging.info(f"LOGGING STRING: {msg}")
        













    teleporter.disconnect()
    print('device disconnected')

if __name__ == "__main__":
    main()