import socket, sys
from thread import *



try:
	listening_port = int(raw_input("Enter listening port"))
except KeyboardInterrupt:
	print("\n interrpt")

max_conn = 5
buffer_size = 8192

def proxy_server(webserver, port, conn, data, addr):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		webserver = socket.gethostbyname( webserver )
		print(webserver)
		s.connect((webserver, port))
		s.sendall(data)
		while 1:
			reply = s.recv(buffer_size)
			print(len(reply))
			if (len(reply) > 0):
				conn.send(reply)
				dar = float(len(reply))
				dar = float(dar / 1024)
				dar = "%.3s" % (str(dar))
				dar = "%s KB" % (dar)
				print("[*] request Done: %s => %s <=" % (str(addr[0]), str(dar)))
			else:
				s.close()
				conn.close()
	except socket.error, (value, message):
		s.close()
		conn.close()
		sys.exit(1)

def conn_string(conn, data, addr):
	try:
		print("data --> {}".format(data))
		first_line = data.split('\n')[0]
		url = first_line.split(' ')[1]
		print(url)
		http_pos = url.find("://")
		if (http_pos==-1):
			temp = url
		else:
			temp = url[(http_pos+3):]
		port_pos = temp.find(":")

		webserver_pos = temp.find("/")
		if webserver_pos == -1:
			webserver_pos = len(temp)
		webserver = ""
		port = -1
		if (port_pos==-1 or webserver_pos < port_pos):
			port = 80
			webserver = temp[:webserver_pos]
		else:
			port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
			webserver = temp[:port_pos]
		print("data : {}| port: {}| webserver: {}| addr: {}| conn: {} ".format(data, port, webserver, addr, conn))
		proxy_server(webserver, port, conn, data, addr)
	except Exception, e:
		pass


def start():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('0.0.0.0', listening_port))
		s.listen(max_conn)
		print("server started at [%d]\n" % (listening_port))
	except Exception, e:
		print("unable to initialize")
		sys.exit()

	while 1:
		try:
			conn, addr = s.accept()
			data = conn.recv(buffer_size)
			start_new_thread(conn_string, (conn, data, addr))

		except Exception as e:
			s.close()
			print("user requested to close")
			sys.exit(1)
	s.close()


start()
