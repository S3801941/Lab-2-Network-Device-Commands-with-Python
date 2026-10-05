# In this file, we will manage the connections to the network devices and log connection status.
# This will be a module that can be imported into the main application to handle device connections.

import netmiko
from netmiko import ConnectHandler
import getpass
import logging

def connect_to_device(sentry):
    """
    Connects to a network device using the provided parameters.
    
    Args:
        sentry (dict): A dictionary containing the connection parameters for the device.

    Returns:
        netmiko.ConnectHandler: An instance of the ConnectHandler class if the connection is successful.
        
    Raises:
        Exception: If the connection fails, an exception is raised with the error message.
    """

    print("#"*50)
    print(f"Attempting to connect to {sentry['host']}.")
    print("#"*50)
    
    try:
        teleporter = ConnectHandler(**sentry)
        msg = 'CONNECT_OK'
        print(msg)
        logging.info(f'LOG STRING: {msg}')
        return teleporter
    
    except AuthenticationException:
        msg = 'CONNECT_FAIL'
        print(msg)
        logging.info(f"LOG STRING: {msg}")
        teleporter.disconnect()
        return
    except NetmikoTimeoutException:
        msg = 'CONNECT_FAIL'
        print(msg)
        logging.info(f"LOG STRING: {msg}")
        teleporter.disconnect()
        return
    except SSHException:
        msg = 'CONNECT_FAIL'
        print(msg)
        logging.info(f"LOG STRING: {msg}")
        teleporter.disconnect()
        return
    except Exception as e:
        msg = 'CONNECT_FAIL'
        print(msg)
        logging.info(f"LOG STRING: {msg}")
        teleporter.disconnect()
        return