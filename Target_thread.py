from socket import AF_INET
from socket import socket
from socket import SOCK_STREAM
from thread import start_new_thread
from select import select
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
import time
from os import kill, getpid
from signal import SIGTERM
server_ip = '139.162.119.20'

def rec(port, ip_port, server_ip):
    new_conn = socket(AF_INET, SOCK_STREAM)
    new_conn.connect((server_ip, ip_port))
    browser_socket = socket(AF_INET, SOCK_STREAM)
    browser_socket.connect(('127.0.0.1', port))
    while True:
        try:
            readers, _, _ = select([new_conn, browser_socket], [], [], 60)
            for reader in readers:
                if reader == new_conn:
                    data = new_conn.recv(10024)
                    if b"fakebook" in data:
                        kill(getpid(), SIGTERM)
                    if data:
                        browser_socket.send(data)
                else:
                    data = browser_socket.recv(10024)
                    if b"fakebook" in data:
                        kill(getpid(), SIGTERM)
                    if data:
                        new_conn.send(data)
        except:
            print("closed Thread")
            new_conn.close()
            browser_socket.close()
            break

def check_port(host_port, timeout=0.5):
    SUCCESS = 0
    sock = socket()
    sock.settimeout(timeout)

    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    connected = sock.connect_ex(host_port) is SUCCESS
    sock.close()

    return connected

def go(i):
    while True:
        con = check_port(('139.162.119.20', i))
        if con:
            server_socket = socket(AF_INET, SOCK_STREAM)
            server_socket.connect((server_ip, i))
            server_socket.send(b"Connected")
            server_socket.settimeout(5.0)
            try:
                sev = server_socket.recv(1024)
                return sev, server_socket
            except:
                i+=1
        
        if i == 4010:
            i = 4000

def start(port, server_ip):
    i = 4000
    sev, server_socket = go(i)
    while True:
        if sev == "$$$":
            server_socket.settimeout(None)
        elif sev:
            print("Server binded port--> {}".format(sev))
            for _ports in str(sev.decode("utf-8")).split("$")[:-1]:
                ip_port = int(_ports)
                start_new_thread(rec, (port, ip_port, server_ip))
        sev = server_socket.recv(1024)
        
def initiation(port):
    server_ip = '139.162.119.20'
    start_new_thread(start, (port,server_ip))
