#!/usr/bin/python

import threading, time
import subprocess
from subprocess import Popen, PIPE


class tshark():
	def __init__(self):
		self.totalLength = 0

	def runningCommand(self):
#		interface = input("write your interface name: ")
		tsharkCommand = "sudo tshark -P -q -n -i wlp2s0 -Tfields -e radiotap.datarate -e frame.len -e wlan.ra -e wlan.ta -E separator=/s"
		#should call pipe for the subprocess to read and write simultaneously
		proc = Popen(tsharkCommand, stdout = PIPE, shell = True)
	
		while proc.poll() is None:
			#for every incoming line we should block and then read it
			line = proc.stdout.readline()
#			print(line)
			self.analyze(line)
	
	def analyze(self, line):
		if len(line) > 36:
			transmitterAdd = ""
			destinationAdd = ""
			packLengthArr = []
			dataRateArr = []
			line = line.decode("ascii")
	#		print(line[1:10])
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




			

if __name__ == '__main__':
	tshObj = tshark()
	tshObj.runningCommand()
