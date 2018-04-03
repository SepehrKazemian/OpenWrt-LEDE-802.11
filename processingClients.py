#!/usr/bin/python

import socket
from threading import Thread
import threading
from math import*
import _thread
import time
import concurrent.futures
import subprocess
import queue
from subprocess import Popen, PIPE
import sys
from multiprocessing import Process, Queue, dummy as multithreading
from multiprocessing.dummy import Pool as ThreadPool




class processingClients():
	def __init__(self):	
		address = ("192.168.8.167", 9999)
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind(address)
		server_socket.listen(5)
		self.macHash = {}
		self.readingCounter = 0
		(self.conn, address) = server_socket.accept()
		while True:	
			self.output = self.conn.recv(2048)
			self.readingCounter += 1
			print(self.output)
			self.readingData(self.output)

#	process = Popen("ncat -l -k 9990", stdout = PIPE, shell = True)
	def readingData(self, output):
		signalPower = []
		macAdd = []
#		print("????" + str(output))
#			line = processingClients.process.stdout.readline()
#			print(line)

		for i in range(2, 19):
			macAdd.append(str(output)[i])
		macAddStr = ''.join(str(e) for e in macAdd)

		if macAddStr not in self.macHash:
			self.macHash[macAddStr] = []

		for i in range(21, len(output)):
			if str(output)[i] != " ":
				signalPower.append(str(output)[i])
			else:
				break
		signalStr = ''.join(str(e) for e in signalPower)
		print(signalStr)

		self.macHash[macAddStr].append(signalStr)
		if len(self.macHash[macAddStr]) > 10:
			self.status(macAddStr)


		for key,value in self.macHash.items():
			if key == macAddStr:
				print(key, value)
		
#			thread = threading.Thread( target = self.status, args = (macAddStr,))
#			print("thread name is: " + str(thread))
#			thread.start()
			#thread.close()
			#thread.join()
#					pool.submit(self.status(macAddStr))
			#	pool.close()
			#	pool.join()

	def status(self, macAddStr):

		meanVal = 0
		variance = 0
		deviation = 0
		situation = ""

		for i in range(0, len(self.macHash[macAddStr])):
			meanVal += int(self.macHash[macAddStr][i])
		meanVal = meanVal/len(self.macHash[macAddStr])

		print(macAddStr + " mean is: " + str(meanVal))
		for i in range(0, len(self.macHash[macAddStr][i])):
			variance += pow(meanVal - int(self.macHash[macAddStr][i]), 2)

		variance = variance/len(self.macHash[macAddStr])
		print(macAddStr + " var is: " + str(variance))
		deviation = sqrt(variance)
		if deviation > 10:
			situation = macAddStr + " dynamic"
		else:
			situation = macAddStr + " staticc"
		print(situation)
		print(macAddStr + " " + str(deviation))
		self.conn.send(situation.encode())
		
	#		processingClients.conn.send(situation)
	#		proc =  Popen("echo "+ str(situation) + " | nc 192.168.8.1 6666", stdout = PIPE, shell = True)
		self.macHash.pop(macAddStr)




if __name__ == "__main__":
	processingClients()
