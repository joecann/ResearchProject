import subprocess
import socket
import time
from tkinter import messagebox
import re
import ip_blocker as ip 
import datetime
import os
import sys

shortcut_name = 'Snort_Windows.exe'
class RunSnort():
    def __init__(self) -> None:
        self.run()
        
    def getIP(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))        
            ip_address = s.getsockname()[0]
            return ip_address
        except Exception as e:
            print(f"Error fetching IP address: {e}")
            return None
        
    def get_snort_interface_index(self):
        try:
            result = subprocess.run(['C:\\Snort_Windows1.0\\Snort\\bin\\snort', '-W'], 
                                    capture_output=True, text=True)
            # Split the output into lines
            lines = result.stdout.strip().split('\n')
            # Skip the header line if present (if 'Interface' is in the first line)
            if 'Interface' in lines[0]:
                lines = lines[1:]
            #returns interface index
            for line in lines:
                if line.startswith('Index') or line.startswith('-----'):
                    continue  # Skip header lines
                parts = line.split()
                if len(parts) >= 3: 
                    index = parts[0]
                    ip = parts[2]
                    if ip == self.getIP():
                        return index

        except Exception as e:
            print(f"Error running snort -W: {e}")
            return []

    def monitor_snort_log(self,log_file_path):
        rules =[]
        with open("C:\Snort_Windows1.0\\rules.txt","r") as file:
                file.readline()
                for f in file:
                    rules.append(f)
        try:
            with open(log_file_path, 'r') as file:
                # Move the file pointer to the end of the file
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(1)  # Wait for new data to be written
                        continue
                    if any(tp in line for tp in rules):
                        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                        ip_addresses = re.findall(ip_pattern, line)
                        if ip_addresses:
                            first_ip = ip_addresses[0] 
                        #because of the speed of alert it may take time for the alerts to catch up with the firewall
                        if first_ip not in ip.get_blocked_ips():                   
                            alert = messagebox.askyesno(title="Alert", message= f"Would you like to block {first_ip}")
                            if alert: #yes == true
                                ip.block_ip(first_ip)
                    #else:
                     #   print(line)

        except Exception as e:
            print(f"An error occurred: {e}")

    def run(self):  
        index = self.get_snort_interface_index()
        #create new log folder with date stamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_folder = f"C:\\Snort_Windows1.0\\Snort\\log\\log_{timestamp}" 
        os.makedirs(log_folder, exist_ok=True)
        #run command
        cmd_command = f"C:\\Snort_Windows1.0\\Snort\\bin\\snort.exe -c C:\\Snort_Windows1.0\\Snort\\etc\\snort.conf -i {index} -A fast -l {log_folder}"
        result = subprocess.run(cmd_command, shell=True, capture_output=True, text=True)
        time.sleep(10)#allows time for the alert file to be created. Stops no file found error
        self.monitor_snort_log(f"C:\\Snort_Windows1.0\\Snort\\log\\{log_folder}\\alert.ids")
        return result
