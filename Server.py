# -*- coding: utf-8 -*-
import socket
import select
# from thread import start_new_thread
from threading import Thread
import sys
import ast
import os
import time

dir_list = os.getcwd().split("/")
country = dir_list[-2:]
file = open("info.json", 'r')
data = file.read()
file.close()
info_dict = ast.literal_eval(data)

def check_port(choice, info_dict, country, timeout=0.5):
    SUCCESS = 0

    start = info_dict[country[0]][country[1]][choice][0]
    end = info_dict[country[0]][country[1]][choice][1]

    for i in range(start, end):
        host_port = ('', i)
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            test_sock.bind(('',i))
            print("Browser Port: {}".format(i))
            break
        except:
            test_sock.close()
    return test_sock


connection = check_port("Browser", info_dict, country)
connection.listen(2000)

outgoing_connection = check_port("range", info_dict, country)
outgoing_connection.listen(1)

while True:
    target_conn, addr = outgoing_connection.accept()
    reply = target_conn.recv(1024)
    if reply:
        print(reply)
	    target_conn.send(b'$$$')
    if reply == 'Connected':
        info_dict[country[0]][country[1]]['Connection_Status'] = "True"
        file = open("/home/tentacool/info.json", 'w')
        file.write(str(info_dict))
        file.close()
        break

def free_port(range_):
    c = os.popen('netstat -lntu').read().split("\n")
    count = 2
    len_ = len(c)
    port_list = []
    while count < len_:
        t = c[count].split()
	try:
	    port_list.append(int(t[3].split(":")[-1]))
	except:
		pass
    count += 1
    print("port_list: {}".format(port_list))
    for p in range(range_[0], range_[1]):
        if p not in port_list:
	    try:
	    	recieve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    	recieve.bind(('', int(p)))
            print("port {}".format(p))
            break
	    except:
		    pass
    return (recieve,p)


def go(conn, target_conn, addr, range_):
    try:
	    recieve, po = free_port(range_)
	    recieve.listen(2000)
	    p_port = str(po)+"$"
	    target_conn.send(p_port.encode('utf-8'))
	    recc, add = recieve.accept()
	    start = time.time()
	    check = True
	    while check:
            try:
                readers, _, _ = select.select([conn, recc], [], [], 60)
                for reader in readers:
                if reader is conn:
                    data = conn.recv(8129)
                    if data:
                    recc.sendall(data)
                    start = time.time()
                else:
                    data = recc.recv(8129)
                    if data:
                    conn.send(data)
                    start = time.time()
                if time.time() - start > 60:
                    check = False
                    break
            except:
                recc.close()
                conn.close()
                check = False
	    try:
            recc.close()
            conn.close()
	    except:
		    pass
	    recieve.close()
    except:
	    target_conn.close()
addr_list = []

while True:
    conn, addr = connection.accept()
    print("Browser addr connection IP:Port--> {}".format(addr))
    if addr not in addr_list:
        range_ = info_dict[country[0]][country[1]]['Port Range']
        print("range: {}".format(range_))
        Thread(target=go, args=(conn, target_conn,addr, range_)).start()
    addr_list.append(addr)
    addr_list = list(set(addr_list))
    print(len(addr_list))
