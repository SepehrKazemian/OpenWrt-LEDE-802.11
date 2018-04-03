#!/usr/bin/python

from threading import Thread
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

class stations():
	macHash = {}
	def findStations(self, command):
		#getting command and pass it to the Pipe
		process = Popen(command, stdout = PIPE, shell = True)
		
		while True:
			line = process.stdout.readline()
			#lineAscii = line.decode('ascii')
			if str(line) == r"b''":
				break
			#if (str(line)[2] != "\\"):
			yield str(line)
			
			
	def macStations(self, command):
		macCollector = []
		threads = []
		macAddSave = ''
#		pool = multithreading.Pool(1)
#		thread1 = Thread( target = self.recieve, args = ("6666",))
#		thread1.start()                                                           

		while True:
			time.sleep(0.5)
			result = self.findStations(command)
			for line in result:
				macAdd = []
				signal = []
				print(line)
				proc = Popen("echo " + str(line) + " | nc 127.0.0.1 9990", stdout = PIPE, shell = True)
#		thread1 = Thread( target = self.recieve, args = ("6666",))
#				thread2 = Thread( target = self.send, args = ("9997",line,))
#				proc = Popen("echo " + str(line) + " | nc 192.168.8.167 9999", stdout = PIPE, shell = True)
#			thread1.start()
#			thread2.start()


	def recieve(self, portNum):
#		print(str(line))
		proc = Popen("ncat -l -k -p " +portNum, stdout = PIPE, shell = True)
		while True:
			output = proc.stdout.readline()
			if str(output) != r"b''":
				print(output)
						
#
			#***Save the Mac Address***#

#				for i in range(2, 19):
#					macAdd.append(line[i])
#				macAddStr = ''.join(str(e) for e in macAdd)
#				print(macAddStr)
#
#				if macAddStr not in stations.macHash:
#					stations.macHash[macAddStr] = []
#					print(macAddStr)
#					thread = Thread( target = self.status(macAddStr))
#					threads.append(thread)
#					thread.start()
					#thread.close()
#					print("thread name is: " + str(thread))
#					thread.join()
#					pool.submit(self.status(macAddStr))
				#	pool.close()
				#	pool.join()





		#***Save the signal power related to that Mac Address***#			

#				if "signal:" in line:				
					#for i in range(15, len(line)):                          
				#		if line[i] != "\\" :                            
			#				signal.append(line[i])     
		#				else:
	#						break
#					signalStr = ''.join(str(e) for e in signal)
					#print(signalStr)
				#	if len(stations.macHash[macAddSave]) >= 10:
			#			del stations.macHash[macAddSave][0]
		#			stations.macHash[macAddSave].append(signalStr)
	#		for key,value in stations.macHash.items():
#				print(key, value)



if __name__ == '__main__':
	stations().macStations("tcpdump -i mon0")
