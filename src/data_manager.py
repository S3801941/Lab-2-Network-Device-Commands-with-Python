# This file will be used to send commands to the network devices and log the output of those commands.
# It will then save the raw output to a file and parse the output using the ntc_templates library to extract relevant information.
# It will then log the parsed output and save it to a file as a report for further analysis.
# All of these steps will be logged to a log file for auditing and troubleshooting purposes.
# These steps will show up in the log file as, [CMD_RUN], [PARSE_OK: <command>] or [PARSE_FAIL: <command>], [REPORT_SAVED].
# The report will be saved as data/reports/device_summary.txt and the raw output will be saved as data/raw/command_output_<timestamp>.txt.




def send_command(teleporter, soldiers):
    """
    Sends a list of commands to the connected network device and logs the output.
    
    Args:
        teleporter (netmiko.ConnectHandler): An instance of the ConnectHandler class representing the device connection.
        soldiers (list): A list of commands to be sent to the device.
    """
    import netmiko
    from netmiko import ConnectHandler
    import getpass
    import datetime
    from pprint import pprint
    from ntc_templates.parse import parse_output
    import logging

    for soldier in soldiers:
        print("#"*50)
        print(f"Sending command: {soldier}")
        print("#"*50)
        
        try:
            rockets = teleporter.send_command(soldier)
            msg = f'CMD_RUN: {soldier}'
            print(msg)
            logging.info(msg)
            explosion = repr(rockets)

            print("#"*50)
            print(f"Raw output for command: {soldier}")
            print("#"*50)
            print(explosion)

            # Save raw output to a file
            mission_timer = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_output_file = f"data/raw/{soldier}_output_{mission_timer}.txt"
            with open(raw_output_file, 'a') as f:
                f.write(f"="*50 + "\n")
                f.write(f"Raw output for command: {soldier}\n")
                f.write(f"="*50 + "\n")
                f.write(explosion + "\n\n")
            
            # Parse the output using ntc_templates
            if soldier == 'show version':
                try:
                    rocket = parse_output(platform='cisco_ios',command=soldier, data= rockets)
                    msg = f'PARSE_OK: {soldier}'
                    print(msg)
                    logging.info(msg)
                
                    # Save parsed output to a report file
                    briefcase = f"data/reports/device_summary.txt"
              
                    with open(briefcase, 'a') as f:
                        f.write(f"Command: {soldier}\n")
                        pprint(rockets, stream=f)
                        f.write("\n\n")
                
                msg = 'REPORT_SAVED'
                print(msg)
                logging.info(msg)
            else:
                msg = f'PARSE_FAIL: {soldier}'
                print(msg)
                logging.info(msg)

        except Exception as e:
            msg = f'ERROR_RUNNING_COMMAND: {soldier} - {str(e)}'
            print(msg)
            logging.error(msg)
