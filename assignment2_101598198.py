"""
Author: Rohan Davis
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

# TODO: Import the required modules (Step ii)
# socket, threading, sqlite3, os, platform, datetime

import socket
import threading
import sqlite3
import os
import platform
import datetime


# TODO: Print Python version and OS name (Step iii)

print("Python Version:", platform.python_version())
print("Operating System:", os.name)


# TODO: Create the common_ports dictionary (Step iv)
# Add a 1-line comment above it explaining what it stores

# Stores common ports and their services
common_ports = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS"
}

# TODO: Create the NetworkTool parent class (Step v)
# - Constructor: takes target, stores as private self.__target
# - @property getter for target
# - @target.setter with empty string validation
# - Destructor: prints "NetworkTool instance destroyed"

class NetworkTool:
    def __init__(self, target):
        self.__target = target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if value == "":
            print("Error: Target cannot be empty")
        else:
            self.__target = value

    def __del__(self):
        print("NetworkTool instance destroyed")


# Q3: What is the benefit of using @property and @target.setter?
# TODO: Your 2-4 sentence answer here... (Part 2, Q3)

# Using @property and @target.setter allows controlled access to the private __target variable. 
# It ensures that validation can be applied when setting the value, such as preventing an empty target. 
# It also improves data security and encapsulation compared to directly accessing the variable.


# Q1: How does PortScanner reuse code from NetworkTool?
# TODO: Your 2-4 sentence answer here... (Part 2, Q1)

# The PortScanner class reuses code from the NetworkTool class through inheritance. This allows it to access its attributes and methods without rewriting them. 
# For example, a PortScanner inherits the target property and its getter/setter, so it can store and validate the target IP address. 
# It also reduces code duplication and keeps the design organized by separating common functionality into the parent class.

# TODO: Create the PortScanner child class that inherits from NetworkTool (Step vi)
# - Constructor: call super().__init__(target), initialize self.scan_results = [], self.lock = threading.Lock()
# - Destructor: print "PortScanner instance destroyed", call super().__del__()

class PortScanner(NetworkTool):

    def __init__(self, target):
        super().__init__(target)
        self.scan_results = []
        self.lock = threading.Lock()

    def __del__(self):
        print("PortScanner instance destroyed")
        super().__del__()
#
# - scan_port(self, port):
#     Q4: What would happen without try-except here?
#     TODO: Your 2-4 sentence answer here... (Part 2, Q4)

# Without the try-except block, the program would crash if an error occurs while scanning a port, such as when the target is unreachable. 
# This would stop the entire scanning process instead of continuing with other ports. 
# Exception handling ensures the program remains stable and continues scanning even if some ports cause errors.
#
#     - try-except with socket operations
#     - Create socket, set timeout, connect_ex
#     - Determine Open/Closed status
#     - Look up service name from common_ports (use "Unknown" if not found)
#     - Acquire lock, append (port, status, service_name) tuple, release lock
#     - Close socket in finally block
#     - Catch socket.error, print error message
#
# - get_open_ports(self):
#     - Use list comprehension to return only "Open" results
#
#     Q2: Why do we use threading instead of scanning one port at a time?
#     TODO: Your 2-4 sentence answer here... (Part 2, Q2)

# Threading allows multiple ports to be scanned at the same time, which significantly improves performance. 
# Using threads makes the scan much faster by running many port checks in parallel.
# If we scanned ports one at a time, scanning up to 1024 ports would take a long time because each connection waits before moving to the next. 



#
# - scan_range(self, start_port, end_port):
#     - Create threads list
#     - Create Thread for each port targeting scan_port
#     - Start all threads (one loop)
#     - Join all threads (separate loop)


# TODO: Create save_results(target, results) function (Step vii)
# - Connect to scan_history.db
# - CREATE TABLE IF NOT EXISTS scans (id, target, port, status, service, scan_date)
# - INSERT each result with datetime.datetime.now()
# - Commit, close
# - Wrap in try-except for sqlite3.Error

def scan_port(self, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((self.target, port))

        status = "Open" if result == 0 else "Closed"
        service = common_ports.get(port, "Unknown")

        self.lock.acquire()
        self.scan_results.append((port, status, service))
        self.lock.release()

    except socket.error as e:
        print(f"Error scanning port {port}: {e}")

    finally:
        sock.close()

# TODO: Create load_past_scans() function (Step viii)
# - Connect to scan_history.db
# - SELECT all from scans
# - Print each row in readable format
# - Handle missing table/db: print "No past scans found."
# - Close connection

def get_open_ports(self):
    return [r for r in self.scan_results if r[1] == "Open"]



# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    pass


    # TODO: Get user input with try-except (Step ix)
    # - Target IP (default "127.0.0.1" if empty)
    # - Start port (1-1024)
    # - End port (1-1024, >= start port)
    # - Catch ValueError: "Invalid input. Please enter a valid integer."
    # - Range check: "Port must be between 1 and 1024."

def scan_range(self, start, end):
    threads = []

    for port in range(start, end + 1):
        t = threading.Thread(target=self.scan_port, args=(port,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()    

   

    # TODO: After valid input (Step x)
    # - Create PortScanner object
    # - Print "Scanning {target} from port {start} to {end}..."
    # - Call scan_range()
    # - Call get_open_ports() and print results
    # - Print total open ports found
    # - Call save_results()
    # - Ask "Would you like to see past scan history? (yes/no): "
    # - If "yes", call load_past_scans()

def save_results(target, results):
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            port INTEGER,
            status TEXT,
            service TEXT,
            scan_date TEXT
        )
        """)

        for r in results:
            cursor.execute("INSERT INTO scans VALUES (NULL, ?, ?, ?, ?, ?)",
                           (target, r[0], r[1], r[2], str(datetime.datetime.now())))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(e)

def load_past_scans():
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM scans")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        conn.close()

    except:
        print("No past scans found.")      



try:
    target = input("Enter target IP (default 127.0.0.1): ") or "127.0.0.1"
    start = int(input("Start port: "))
    end = int(input("End port: "))

    if start < 1 or end > 1024:
            print("Port must be between 1 and 1024")
    else:
            scanner = PortScanner(target)

            print(f"Scanning {target} from port {start} to {end}...")

            scanner.scan_range(start, end)

            results = scanner.get_open_ports()

            for r in results:
                print(f"Port {r[0]}: {r[1]} ({r[2]})")

            print(f"Total open ports: {len(results)}")

            save_results(target, results)

            if input("View past scans? (yes/no): ") == "yes":
                load_past_scans()

except ValueError:
        print("Invalid input. Please enter numbers only.")          


# Q5: New Feature Proposal
# TODO: Your 2-3 sentence description here... (Part 2, Q5)
# Diagram: See diagram_101598198.png in the repository root


# I would add a feature that filters and displays only specific types of ports, such as only "Open" ports, using a list comprehension. 
# This would make it easier for users to quickly analyze results without manually checking all scanned ports. 
# The feature would use a list comprehension to extract only matching results from the scan_results list.
# Diagram: See diagram_101598198.png in the repository root