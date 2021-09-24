#  coding: utf-8 
import socketserver
from os import path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

	def handle(self):
		rlist = self.request.recv(1024).decode().strip().split()
		if not rlist:
			self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			return
		if rlist[0] != "GET":
			self.request.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode())
			return
		if '../' in rlist[1][1:]:
			self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			return
		file_path = "./www/" + rlist[1][1:]
		if path.isfile(file_path):
			f = open(file_path,"r")
			self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/" + rlist[1][1:].split('.')[-1].strip() + "\r\n\r\n" + "\n".join(f.readlines())).encode())
			f.close()
		elif path.isdir(file_path):
			if file_path[-1] != '/':
				f = open("./www/index.html","r")
				self.request.sendall(("HTTP/1.1 301 Moved Permanently Location: " + 'http://localhost:8080/www/' + file_path + "/" + "\r\nContent-Type: text/html\r\n\r\n" + "\n".join(f.readlines())).encode())
				f.close()
			else:
				f = open("./www/index.html","r")
				self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + "\n".join(f.readlines())).encode())
				f.close()
		else:
			self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
