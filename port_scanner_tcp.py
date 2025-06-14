#!/usr/bin/env python3

#Libraries
import sys
import socket
import argparse
import signal
import threading
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

# Global variables
open_sockets = []
executor = None
stop_event = threading.Event() # Handler event to save exit status

def def_handler(signal, frame):
    
    print(colored(f"\n[-] Cerrando correctamente los procesos actuales...\n", 'yellow'))
    
    stop_event.set() # Evitar que todos los hilos sigan realizando el escaneo

    for socket in open_sockets:
        socket.close()
    
    print(colored(f"\n[!] Saliendo del programa...\n", 'red'))

    sys.exit(1)

# Manage CTRL + C
signal.signal(signal.SIGINT, def_handler)

# Get menu arguments
def get_arguments():
    argparser = argparse.ArgumentParser(description="Fast TCP Port Scanner")
    argparser.add_argument("-t", "--target", dest="target", required=True, help="Target to scan (Ex: 10.10.10.10)")
    argparser.add_argument("-p", "--port", dest="port", required=True, help="Port range to scan (Ex: 1-100 or 3030,8080,22 or 8080)")

    arguments = argparser.parse_args()

    return arguments.target, arguments.port

# Create sockets
def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    return s

def scan(host, port):
    if stop_event.is_set():
        return # Salir si se ha detenido el escaneo

    socket = create_socket()
    open_sockets.append(socket)
    
    try:
        socket.connect((host, port)) # Check connection for open port
        socket.sendall(b"HEAD / HTTP/1.0\r\n\r\n") # send info to receive headers of the namme and version service running, considering HTTP service
        response = socket.recv(1024) # receive headers of the name and version
        response = response.decode(errors='ignore').split('\n')[0] # Get the first line (version and service)

        if response:
            print(colored(f"\n[+] {port} -> {response}", 'green'))
        else:
            print(colored(f"\n[+] {port} - OPEN", 'green'))
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        socket.close()

# Manage scans with threads
def start_scan(host, ports):
    global executor

    executor = ThreadPoolExecutor(max_workers=50)
    executor.map(lambda port: scan(host, port), ports)
    executor.shutdown(wait=True)

# Get the port range to scan
def get_range(port_str):
    
    if '-' in port_str:
        start, end = map(int, port_str.split('-'))
        return range(start, end+1)
    elif ',' in port_str:
        return map(int, port_str.split(','))
    else:
        return (int(port_str),)

# main logic
def main():
    host, port_str = get_arguments()
    ports = get_range(port_str)

    start_scan(host, ports)

# Initial
if __name__ == '__main__':
    main()
