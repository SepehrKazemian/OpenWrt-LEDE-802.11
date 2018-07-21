import os, sys
import threading, time
import subprocess
from subprocess import Popen, PIPE

class abb():
	'''
	def threads(self):
		print("aaaa")
		thread = threading.Thread( target = abb.capturing)
		thread2 = threading.Thread(target = abb.func1)
		print("thread name is: " + str(thread))
		thread.start()
		thread2.start()


	def capturing():
		interface = input("write your interface name: ")
		tcpdumpCommand = "tcpdump -vvs 0 -i wlx8416f918fc7e -en"
		
		#should call pipe for the subprocess to read and write simultaneously
		proc = Popen(tcpdumpCommand, stdout = PIPE, shell = True)
		    
		while proc.poll() is None:
			print("aa")
			#for every incoming line we should block and then read it
			line = proc.stdout.readline()
			print(line)
	'''
	def func1(self):
		i = 1
		while True:
			time.sleep(0.0001)
			proc = Popen("sudo iwconfig wlx8416f918fc7e channel " + str(i), stdout = PIPE, shell = True)
			if i == 1:
				i = 6
			elif i == 6:
				i = 11
			elif i == 11:
				i = 1

	def func2():
		while True:
			print(2)


if __name__ == "__main__":
	abb().func1()
	
