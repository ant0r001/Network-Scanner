# Colorful Advanced Network Scanner

This is a Python-based network scanning tool with a colorful and user-friendly graphical interface. It allows you to discover active hosts on your local network by sending ICMP echo requests (pings).

## Features

* **Intuitive Graphical User Interface (GUI):** Built with `tkinter` and `ttk` for a native look and feel.
* **Colorful Output:** Uses color cues to indicate the status of the scan and highlight live hosts.
* **Network Prefix Input:** Easily specify the network range you want to scan using CIDR notation (e.g., `192.168.1.0/24`).
* **Scan Progress:** A progress bar visually displays the progress of the network scan.
* **Real-time Status Updates:** A status label provides feedback on the current state of the scanner (Scanning, Complete, Cancelled, Error, Idle).
* **Live Host Listing:** Discovered active hosts (responding to ping) are listed in a scrollable text area, with live hosts highlighted in light green.
* **Scan Cancellation:** An option to stop the ongoing scan prematurely using a "Cancel Scan" button.
* **Themed Interface:** Utilizes `ttk.Style` for a more modern and customizable look (currently using the 'clam' theme).

## How to Use

1.  **Prerequisites:** Ensure you have Python 3 installed on your system. No additional libraries need to be installed as `tkinter`, `ipaddress`, `subprocess`, `threading`, `queue`, and `time` are part of the standard Python library.

2.  **Running the Scanner:**
    * Save the Python code (e.g., as `colorful_network_scanner_gui.py`).
    * Open your terminal or command prompt.
    * Navigate to the directory where you saved the file.
    * Run the script using the command: `python colorful_network_scanner_gui.py`

3.  **Using the GUI:**
    * **Enter Network Prefix:** In the "Scan Configuration" section, enter the network prefix you want to scan (e.g., `192.168.1.0/24`). If you are unsure about your network prefix, you can usually find it using system tools like `ipconfig` (Windows) or `ip a` / `ifconfig` (macOS/Linux). For a typical home network, the first three parts of your IP address followed by `/24` might work (e.g., if your IP is `192.168.1.100`, try `192.168.1.0/24`).
    * **Click "Scan Network":** Press the "Scan Network" button to start the scanning process.
    * **Observe Progress:** The "Scan Progress" section will show a progress bar and the current status of the scan.
    * **View Live Hosts:** As active hosts are found, their IP addresses will appear in the "Live Hosts" text area, with a light green background.
    * **Cancel Scan (Optional):** If you need to stop the scan before it completes, click the "Cancel Scan" button.
    * **Wait for Completion:** Once the scan is finished, the status label will indicate "Scan complete!" and show the number of live hosts found.

## Potential Enhancements (Future Development)

* **MAC Address Resolution:** Displaying the MAC address associated with each live IP address (this can be platform-dependent and may require elevated privileges).
* **Port Scanning:** Adding the ability to scan for open TCP/UDP ports on the discovered hosts.
* **Hostname Resolution:** Attempting to resolve hostnames for the live IP addresses.
* **More Styling Options:** Allowing users to customize the colors and theme of the GUI.
* **Saving Scan Results:** Providing an option to save the list of live hosts to a file.
* **More Advanced Ping Options:** Allowing customization of ping parameters (e.g., number of packets, timeout).

## Disclaimer

This tool is intended for educational purposes and for scanning networks you own or have explicit permission to scan. Network scanning can generate network traffic, and scanning networks without permission may be considered unethical or illegal. Use this software responsibly.
