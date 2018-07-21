#!/usr/bin/python

import threading, time
import subprocess
from subprocess import Popen, PIPE
import os


class tshark():
	def __init__(self):
		self.totalLength = 0
		self.time = -10
		self.timeArr = []

	def runningCommand(self):
#		interface = input("write your interface name: ")
		tsharkCommand = 'ssh root@192.168.1.1 "tcpdump -i mon1 -s 0 -U -w -" | sudo tshark -q -n -i - -Tfields -e radiotap.datarate -e radiotap.length -e frame.len -e wlan.ra -e wlan.ta -e wlan_mgt.ds.current_channel -e wlan_radio.signal_dbm -e frame.time -e frame.interface_id -E separator=/'
#		tsharkCommand = 'sudo tshark -Pq -n -i wlx8416f918fc7e -Tfields -e radiotap.datarate -e radiotap.length -e frame.len -e wlan.ra -e wlan.ta -e wlan_mgt.ds.current_channel -e wlan_radio.signal_dbm -e frame.time -e frame.interface_id -E separator=/'
		#should call pipe for the subprocess to read and write simultaneously
		proc = Popen(tsharkCommand, stdout = PIPE, shell = True)
	
		while proc.poll() is None:
			#for every incoming line we should block and then read it
			line = proc.stdout.readline()
#			print(line.decode("ascii"))
			self.analyze(line.decode("ascii"))
	
	def analyze(self, line):
		transmitterAdd = ""
		destinationAdd = ""
		tmpArr = []
		dataRate = 0
		length = 0
		ra = ""
		ta = ""
		channel = 0
		rssi = ""
		chanUtil = 0
		time = ""
		#pointer is the number of the char that we are reading
		pointer = 0
		radiotapHeader = 0
		#in each part we have different information and each part is add by "\"
		part = 0
		seconds = 0
		counter = 0

		while part <= 7:
			x = pointer
			for i in range(x, len(line)):
				if line[i] == "\\":
					pointer += 1
					break
				else:
					tmpArr.append(line[i])
					pointer += 1
			if len(tmpArr) != 0:
				tmp = ''.join(str(x) for x in tmpArr)
			else:
				tmp = "-999" #it is impossible for the fields to be this number

			if part == 0:
				dataRate = float(tmp)
			elif part == 1:
				radiotapHeader = int(tmp)
			elif part == 2:
				length = (int(tmp) - radiotapHeader) * 8 #36 is radiotap header size
			elif part == 3:
				ra = tmp
			elif part == 4:
				ta = tmp
			elif part == 5:
				channel = int(tmp)
			elif part == 6:
				rssi = tmp
#			elif part == 7:
#				chanUtil = int(tmp) #channel utilization is out of 255
			elif part == 7:
				time = tmp


			#print(dataRate)
			tmpArr = []
			#print(pointer)
			part += 1
#		print(dataRate)
#		print(length)
#		print(ra, ta, channel, rssi, chanUtil)
#		print(time[19: 31:])
		seconds = float(time[19: 31:])
#		print(int(seconds))
		
#		if ta == "50:0f:80:27:0e:46" and chanUtil != -999:
#			print("it is chanUtil: " + str(float(chanUtil/255)))


		if self.time == int(seconds):
			if dataRate != -999 and length != -999:
				self.totalLength += ((float(length))/float(dataRate))
#				print(self.totalLength)
		elif self.time + 1 == int(seconds):
			couter = 0
			if dataRate != -999 and length != -999:
				if len(self.timeArr) < 5:
					self.timeArr.append(self.totalLength)
				else:
					for i in range(len(self.timeArr)):
						counter += self.timeArr[i]
					counter = counter / 1000000
					print(counter)
					del self.timeArr[0]
					self.timeArr.append(self.totalLength)
				self.totalLength = 0
				self.time = int(seconds)
				self.totalLength += ((float(length))/float(dataRate))
		else:
			if dataRate != -999 and length != -999:
				self.time = int(seconds)
				self.totalLength += ((float(length))/float(dataRate))
'''		
		transmitterAdd += line[len(line)-18::]
		destinationAdd += line[len(line)- 36: len(line)-18:]
#			print(line)
#			print(transmitterAdd)
#			print(destinationAdd)

		for i in range(len(line) - 36):
			if line[i] != " ":
				dataRateArr.append(line[i])
			else:
				break
	
		dataRate = ''.join(str(x) for x in dataRateArr)

		counter = 0		
		for i in range(len(line) - 36):
			if line[i] == " " and counter == 0:
				counter += 1
			elif line[i] != " " and counter == 1:
				packLengthArr.append(line[i])
		
			elif line[i] == " " and counter == 1:
				break

		packLength = ''.join(str(x) for x in packLengthArr)
#			print(dataRate)
#			print(packLength)
		if ("e4:95:6e:42:21:f2" in transmitterAdd and "40:b8:37:a2:a2:9a" in destinationAdd) or ("40:b8:37:a2:a2:9a" in transmitterAdd and "e4:95:6e:42:21:f2" in destinationAdd):
#				print("intooam")
			self.totalLength += ((float(packLength) - 26)/float(dataRate))
		
		print(self.totalLength)
'''



			

if __name__ == '__main__':
	tshObj = tshark()
	tshObj.runningCommand()
