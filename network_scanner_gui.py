import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ipaddress
import subprocess
import platform
import threading
import queue
import time

def ping(host, result_queue, stop_flag):
    """Pings a host and puts the result (host, is_alive) in the queue."""
    is_alive = False
    try:
        if stop_flag.is_set():
            return
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(timeout=1)
        is_alive = process.returncode == 0
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        print(f"Error pinging {host}: {e}")
    result_queue.put((host, is_alive))

def scan_network(network_prefix, progress_var, result_text, status_label, stop_flag):
    """Scans a network range for live hosts and updates the GUI."""
    result_text.delete(1.0, tk.END)  # Clear previous results
    live_hosts_count = 0
    status_label.config(text="Status: Scanning...")
    cancel_button['state'] = tk.NORMAL # Enable cancel button
    scan_button['state'] = tk.DISABLED # Disable scan button
    status_label.config(foreground="darkgreen") # Indicate scanning

    try:
        net = ipaddress.ip_network(network_prefix, strict=False)
        total_hosts = net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses
        progress_var.set(0)
        progress_bar['maximum'] = total_hosts

        result_queue = queue.Queue()
        threads = []
        host_count = 0

        for ip in net.hosts():
            if stop_flag.is_set():
                break
            host_count += 1
            ip_str = str(ip)
            thread = threading.Thread(target=ping, args=(ip_str, result_queue, stop_flag))
            threads.append(thread)
            thread.start()
            time.sleep(0.01) # Add a small delay

        for thread in threads:
            thread.join()
            if not result_queue.empty():
                host, is_alive = result_queue.get()
                if is_alive:
                    live_hosts_count += 1
                    result_text.insert(tk.END, f"IP: {host}\n", "live") # Tag live hosts
            progress_var.set(host_count)

        if not stop_flag.is_set():
            status_label.config(text=f"Status: Scan complete! Found {live_hosts_count} live hosts.")
            status_label.config(foreground="blue") # Indicate completion
        else:
            status_label.config(text="Status: Scan cancelled.")
            status_label.config(foreground="orange") # Indicate cancellation

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid network prefix: {e}")
        status_label.config(text="Status: Error")
        status_label.config(foreground="red") # Indicate error
    finally:
        scan_button['state'] = tk.NORMAL # Re-enable scan button
        cancel_button['state'] = tk.DISABLED # Disable cancel button

def start_scan():
    """Starts the network scan in a separate thread."""
    network_prefix = network_entry.get()
    if network_prefix:
        stop_flag.clear() # Reset the stop flag
        threading.Thread(target=scan_network, args=(network_prefix, progress_var, result_text, status_label, stop_flag)).start()
    else:
        messagebox.showerror("Error", "Please enter a network prefix.")

def cancel_scan():
    """Sets the stop flag to signal the scan to stop."""
    stop_flag.set()
    status_label.config(text="Status: Cancelling...")
    status_label.config(foreground="orange")

# --- GUI Setup ---
window = tk.Tk()
window.title("Colorful Advanced Network Scanner")

# --- Style Configuration ---
style = ttk.Style()

# Configure the overall theme (you can experiment with different themes)
style.theme_use('clam') # Try 'clam', 'alt', 'default', 'classic'

# Configure LabelFrame colors
style.configure("TLabelframe", background="#f0f0f0", bordercolor="gray")
style.configure("TLabelframe.Label", background="#f0f0f0", foreground="black")

# Configure Button colors
style.configure("TButton", padding=6, relief="raised")
style.configure("Scan.TButton", foreground="darkgreen", font=('Arial', 10, 'bold'))
style.configure("Cancel.TButton", foreground="darkred", font=('Arial', 10))

# Configure Progressbar color
style.configure("TProgressbar", troughcolor="#d9d9d9", background="lightblue")

stop_flag = threading.Event()

# Input Frame
input_frame = ttk.LabelFrame(window, text="Scan Configuration")
input_frame.pack(padx=10, pady=10, fill=tk.X)

network_label = ttk.Label(input_frame, text="Network Prefix (e.g., 192.168.1.0/24):")
network_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
network_entry = ttk.Entry(input_frame)
network_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
input_frame.columnconfigure(1, weight=1) # Make entry expand

scan_button = ttk.Button(input_frame, text="Scan Network", command=start_scan, style="Scan.TButton")
scan_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

cancel_button = ttk.Button(input_frame, text="Cancel Scan", command=cancel_scan, state=tk.DISABLED, style="Cancel.TButton")
cancel_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Progress Frame
progress_frame = ttk.LabelFrame(window, text="Scan Progress")
progress_frame.pack(padx=10, pady=5, fill=tk.X)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, mode='determinate')
progress_bar.pack(padx=5, pady=5, fill=tk.X)

status_label = ttk.Label(progress_frame, text="Status: Idle", foreground="gray")
status_label.pack(padx=5, pady=5, anchor=tk.W)

# Results Frame
results_frame = ttk.LabelFrame(window, text="Live Hosts")
results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

result_text = scrolledtext.ScrolledText(results_frame, width=40, height=10)
result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Configure the ScrolledText widget tag for live hosts AFTER it's created
result_text_bg = "#e0ffe0" # Light green
result_text.tag_configure("live", background=result_text_bg)

window.mainloop()