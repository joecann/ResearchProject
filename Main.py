from config import RunSnort 
import ip_blocker
import start_up
from tkinter import messagebox

if start_up.check_for_start_shell('Snort_Windows1.0.lnk') == False:
    start_up.add_start_shell('C:\Snort_Windows1.0\Main.py','Snort_Windows1.0.lnk')
    
if ip_blocker.is_admin():
    RunSnort()
else: 
    messagebox.showerror("Authentication Error", "User must have administrative privileges!")