import ip_blocker as ip
import tkinter as tk
from tkinter import messagebox

# Function to refresh blocked IPs list
def refresh_blocked_ips_list():
    listbox_blocked_ips.delete(0, tk.END)
    ip_add = ip.get_blocked_ips();
    for i in ip_add:
        listbox_blocked_ips.insert(tk.END, i)

# Function to handle double-click on an IP
def on_double_click(event):
    selected_index = listbox_blocked_ips.curselection()
    if not selected_index:
        return
    
    selected_ip = listbox_blocked_ips.get(selected_index)
    confirm = messagebox.askyesno("Unblock IP", f"Do you want to unblock the IP {selected_ip}?")
    if confirm:
         ip.unblock_ip(selected_ip)
         refresh_blocked_ips_list()

# Create the main application window
root = tk.Tk()
root.title("Blocked IPs Manager")

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Label for blocked IPs list
label_blocked_ips = tk.Label(main_frame, text="Blocked IPs", font=("Helvetica", 14, "bold"))
label_blocked_ips.pack(pady=10)

# Listbox for blocked IPs
listbox_blocked_ips = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=40, height=20, font=("Helvetica", 14))
listbox_blocked_ips.pack(pady=10, fill=tk.BOTH, expand=True)

# Bind double-click event to the listbox
listbox_blocked_ips.bind("<Double-1>", on_double_click)

refresh_blocked_ips_list()

root.mainloop()
  
    


