#!/usr/bin/python

#we want to find the number of users and clients that are in our range

import threading, time
import subprocess
from subprocess import Popen, PIPE


class processing():

	def __init__(self):
		
    
	#since we can operate in different channels, we have to specify which channels we want to operate in
	channels = ['ch1','ch6', 'ch11']
	struct = {}
	# we are making a Hash Map for saving the data
	for i in channels:
		struct[i] = {}
		struct[i]['APs'] = {}
		struct[i]['clients'] = {}
		struct[i]['OW'] = {}
    
    
	def runningCommand(self):
		#we are defining the interface name and then we ran the tcpdump command
		interface = input("write your interface name: ")
		tcpdumpCommand = "tcpdump -vvs 0 -i " + str(interface) + " -en"
		
		#should call pipe for the subprocess to read and write simultaneously
		proc = Popen(tcpdumpCommand, stdout = PIPE, shell = True)
    
		while proc.poll() is None:
			#for every incoming line we should block and then read it
			line = proc.stdout.readline()
			self.parsingOutput(line)

	def parsingOutput(self, line):
        #pattern:
        #14:03:56.122536 13163491749us tsft 12.0 Mb/s 2462 MHz
        #11g -55dBm signal -63dBm signal antenna 0 0us 
        #BSSID:50:0f:80:27:0e:45 DA:ff:ff:ff:ff:ff:ff 
        #SA:50:0f:80:27:0e:45 Beacon (AHSRestrict) 
        #[12.0* 18.0 24.0 36.0 48.0 54.0 Mbit] ESS CH: 11, PRIVACY

		time = []
		SA = []
		BSSID = []
		DA = []
		signal = []
		i = 0
        #line here is binary string which is started with "b'"
        #we should convert it to string
		lineAsc = line.decode('ascii')
		frequency = []
		channelName = ''
		channelStr = ''
    
#		print(lineAsc)

		#getting the time
		for x in range(0,15):
#			print(lineAsc[x])
			time.append(str(lineAsc[x]))
            
		timeStr = ''.join(str(e) for e in time)
#		print(timeStr)
#		print(line)


		#getting the BSSID
		for x in range(16, len(lineAsc)): 
			if (lineAsc[x] == 'B') and (lineAsc[x+1] == 'S') and (lineAsc[x+2]== 'S') and (lineAsc[x+3] == 'I') and (lineAsc[x+4] == 'D') and (lineAsc[x+5] == ':'):
				for i in range (x + 6, x + 23):
					BSSID.append(lineAsc[i])
				BSSIDStr = ''.join(str(e) for e in BSSID)
#				print("BSSID:"+BSSIDStr)
				break

		#getting the Destination Address
		for x in range(16, len(lineAsc)):
			if (lineAsc[x] == 'D') and (lineAsc[x+1] == 'A') and (lineAsc[x+2] == ':'):
				for i in range (x + 3, x + 20):
					DA.append(lineAsc[i])
				DAStr = ''.join(str(e) for e in DA)
#				print("DA:"+DAStr)
				break
            
		#getting the Source Address
		for x in range(16, len(lineAsc)):
			if (lineAsc[x] == 'S') and (lineAsc[x+1] == 'A') and (lineAsc[x+2] == ':'):
				for i in range (x + 3, x + 20):
					SA.append(lineAsc[i])
				SAStr = ''.join(str(e) for e in SA)
#				print("SA:"+SAStr)
				break
       

		#getting the Signal of the data
		for x in range(16, len(lineAsc)):
			if (lineAsc[x] == 's') and (lineAsc[x+1] == 'i') and (lineAsc[x+2] == 'g') and (lineAsc[x+3] =='n') and (lineAsc[x+4] == 'a') and (lineAsc[x+5] == 'l') and (lineAsc[x+6] == ' ') and (lineAsc[x+7] == 'a') and (lineAsc[x+8] == 'n'):
				for i in range (x - 7, x - 1):
					signal.append(lineAsc[i])
				signalStr = ''.join(str(e) for e in signal)
#				print("Signal Antenna:"+signalStr)
				break
        
		#getting the frequency that we are getting the packets at
		for x in range(16, len(lineAsc)):
			if (lineAsc[x] == 'M') and (lineAsc[x+1] == 'H') and (lineAsc[x+2] == 'z') and (lineAsc[x-1] == ' ') and (lineAsc[x+3] == ' '):
				for i in range (x - 5, x - 1):
					frequency.append(lineAsc[i])
				frequencyStr = ''.join(str(e) for e in frequency)
#				print("frequency is:" + frequencyStr)
				break

		#the frequencyStr should be in one of these channels
		#for the sake of simplicity we ignore the packets that are from other channels and we can hear them
		try:
			if frequencyStr == '2462':
				channelStr = 'ch11'

			elif frequencyStr == '2437':
				channelStr = 'ch6'

			elif frequencyStr == '2412':
				channelStr = 'ch1'


			#printing the APs addresses
			for key,value in processing.struct[channelStr]['APs'].items():
				print(key)
#			print("aAAAAAAAAAAAAAAAAAAAAAAAAAA")
			
			#printing the Clients' addresses
			for key,value in processing.struct[channelStr]['clients'].items():
				print(key)
#			print(processing.struct[channelStr]['APs'])

			#incomplete:
			#using beacons as an update of the APs to be sure that they are still existing
			#next step we should check it out in our Hash Table
			if 'Beacon' in lineAsc:
				if SAStr in processing.struct[channelStr]['APs']:
					processing.struct[channelStr]['APs'][SAStr] = {}
					processing.struct[channelStr]['APs'][SAStr] = {'update': 1, 'signalAntenna': signalStr, 'lastTimeSeen': timeStr}
				else:
					processing.struct[channelStr]['APs'][SAStr] = {'update': 1, 'signalAntenna': signalStr, 'lastTimeSeen': timeStr}
                    
            
			#incomplete:
			#using probe responces as an update of the clients to be sure that they are still existing
			#next step we should check it out in our Hash Table
			if 'Probe Response' in lineAsc:
				if DAStr in processing.struct[channelStr]['clients']:
					processing.struct[channelStr]['clients'][DAStr] = {} 
					processing.struct[channelStr]['clients'][DAStr] = {'update': 1, 'signalAntenna': signalStr, 'lastTimeSeen': timeStr}
				else: 
					processing.struct[channelStr]['clients'][DAStr] = {'update': 1, 'signalAntenna': signalStr, 'lastTimeSeen': timeStr}
		except UnboundLocalError:
			print("packet from other frequencies")




if __name__ == '__main__':
	processing().runningCommand()
