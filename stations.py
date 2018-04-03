#!/usr/bin/python

import socket
from threading import Thread
from math import*
import _thread
import time
import concurrent.futures
import subprocess
import queue
from subprocess import Popen, PIPE, STDOUT
import sys
from multiprocessing import Process, Queue, dummy as multithreading
from multiprocessing.dummy import Pool as ThreadPool
import os

class stations():

	def __init__(self):
		self.macHash = {}
		self.usersMac = []
	
	def findStations(self, command):
		#getting command and pass it to the Pipe
		process = Popen(command, stdout = PIPE, shell = True)
		
		while True:
			line = process.stdout.readline()
			#lineAscii = line.decode('ascii')
			if str(line) == r"b''":
				break
			if (str(line)[2] != "\\"):
				yield line
#				proc = Popen("echo " + str(line) + " | nc 192.168.8.167 9990", stdout = PIPE, shell = True)
#				print(line)
			
			
	def macStations(self, command):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(("192.168.8.167", 9999))
		macCollector = []
		threads = []
		macAddSave = ''
#		pool = multithreading.Pool(1)
		thread1 = Thread( target = self.recieve, args = (client_socket,))
		thread2 = Thread( target = self.tcTable)
		thread1.start()
		thread2.start()

		while True:
#			time.sleep(0.5)
			result = self.findStations(command)
#			proc = Popen(" nc 192.168.8.167 9990", stdout = PIPE, stdin = PIPE, stderr = STDOUT, shell = True)

			for line in result:
				macAdd = []
				signal = []
				print(line)
				client_socket.send(line)
#				situation = client_socket.recv(2048)
#				print("situation is: " + str(situation))
#				send_msg = proc.communicate(input = line)[0]
#				print("hello")
#				proc = Popen("echo " + str(line) + " | nc 192.168.8.167 9990", stdout = PIPE, shell = True)
#				proc.stdout.close()
#		thread1 = Thread( target = self.recieve, args = ("6666",))
#				thread2 = Thread( target = self.send, args = ("9997",line,))
#				proc = Popen("echo " + str(line) + " | nc 192.168.8.167 9999", stdout = PIPE, shell = True)
#			thread1.start()
#			thread2.start()


	def recieve(self, client_socket):
		wordSituation = []
		while True:
			situation = client_socket.recv(2048)
			decodeSituation = situation.decode()
			print(decodeSituation)
			if  ("staticc" in decodeSituation) or ("dynamic" in decodeSituation):
				numberOfInfo = floor(len(decodeSituation) / 25)
				print(numberOfInfo)
				self.printWord(decodeSituation, 0, numberOfInfo)
						
	
	def printWord(self, word, startPoint, numberOfInfo):
		wordArr = []
		macAddress = []
		isBool = 0
		for i in range(startPoint, startPoint+24):
			wordArr.append(word[i])
		wordStr = ''.join(str(e) for e in wordArr)

		for i in range(0,17):
			macAddress.append(wordStr[i])
		macAddressStr = ''.join(str(e) for e in macAddress)

		if macAddressStr not in self.macHash:
			self.macHash[macAddressStr] = {}
			self.updateRate = 1
			self.macHash[macAddressStr]['situation'] = ''
			outputIP = subprocess.Popen(['cat /tmp/dhcp.leases | cut -f 2,3,4 -s -d" " | grep -i ' + macAddressStr +' | cut -f 2 -s -d" "'], stdout=subprocess.PIPE, shell = True)
			IP, err = outputIP.communicate()
			IP = IP.decode().replace('\n', '')
			self.macHash[macAddressStr]['IP'] = str(IP)
			print(IP)


		if "static" in wordStr:
			if self.macHash[macAddressStr]['situation'] == 'dynamic':
				self.updateRate = 1
			self.macHash[macAddressStr]['situation'] = 'static'
		else:
			if self.macHash[macAddressStr]['situation'] == 'static':
				self.updateRate = 1
			self.macHash[macAddressStr]['situation'] = 'dynamic'

		self.macHash[macAddressStr]['lastCalled'] = [str(time.time())]

		if macAddressStr not in self.usersMac:
			self.usersMac.append(macAddressStr)

		print(self.macHash)
		print(self.usersMac)
			
		print(wordStr)
		startPoint += 25
		if (startPoint < 25 * numberOfInfo):
			self.printWord(word, startPoint, numberOfInfo)

	
	def tcTable(self):

			while True:			
				time.sleep(10)

				IPScript = """
				"""
				setClassScript = """
				"""
				for i in range(0, len(self.usersMac)):
					IPScript += """$IPTMOD -s """ + self.macHash[self.usersMac[i]]['IP'] + """ -j CLASSIFY --set-class 1:""" + str((i+1)*10)
					IPScript += """
							"""
					setClassScript += """tc class add dev $IF_DSL parent 1:1 classid 1:""" + str((i+1)*10) + """ htb rate $bwForAll"""
					setClassScript +="""
							"""
				
				script = """
				IPT=$(which iptables)
				IF_DSL=wlan0
				IPTMOD="iptables -t mangle -A POSTROUTING -o $IF_DSL"
				NomUsers=""" + str(len(self.usersMac)) + """
				bwForAll=""" + str(30000/len(self.usersMac)) + """kbit
				TC=$(which tc)
	
			#******REMOVING SHAPERS RUlES******#
	
				
				iptables -t mangle --flush
				tc qdisc del dev $IF_DSL root 2> /dev/null > /dev/null
				iptables -t mangle -D POSTROUTING -o $IF_DSL -j shape-in 2> /dev/null > /dev/null
				iptables -t mangle -F shape-in 2> /dev/null > /dev/null
				iptables -t mangle -F shape-in 2> /dev/null > /dev/null
	
			#******START TO MAKE SHAPING RULES*****#
			
				IPTMOD="iptables -t mangle -A POSTROUTING -o $IF_DSL"
				insmod sch_htb
	
				tc qdisc add dev $IF_DSL root	handle 1: htb default 100
				tc class add dev $IF_DSL parent 1:  classid 1:1  htb rate 30000kbit
				""" + setClassScript +  IPScript
				
				print(str(script))
				os.system("bash -c '{0}'".format(script))
				
				

				
#				print("situation is: " + str(situation))
#		print(str(line))
#		proc = Popen("ncat -l -k -p " +portNum, stdout = PIPE, shell = True)
#		while True:
#			output = proc.stdout.readline()
#			if str(output) != r"b''":
#				print(output)
						
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
	initial = stations()
	initial.macStations("iwinfo wlan0 assoclist")
