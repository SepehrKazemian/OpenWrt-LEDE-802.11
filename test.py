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
import os

class processingClients():
	def __init__(self):
		print("hello")	
		arr = []
		a = "10.0.0.1"
		b = "10.0.0.2"
		arr.append(a)
		arr.append(b)
#		time.sleep(50)
		script="""
		IF_DSL=wlan0
		TC=$(which tc)
		IPT=$(which iptables)
		#******REMOVING SHAPERS RUlES******#
		$IPT -t mangle --flush
		$TC qdisc del dev $IF_DSL root 2> /dev/null > /dev/null
		$IPT -t mangle -D POSTROUTING -o $IF_DSL -j shape-in 2> /dev/null > /dev/null
		$IPT -t mangle -F shape-in 2> /dev/null > /dev/null
		$IPT -t mangle -F shape-in 2> /dev/null > /dev/null
	
		#******START TO MAKE SHAPING RULES*****#
		IPTMOD="$IPT -t mangle -A POSTROUTING -o
		"""
		script3 = """ 
			"""
		for i in range(0, 4):
			script3 += """ echo this is """ + str(i)
			script3 += """
				"""
		print("hello")
		script2 = """ echo """ + str(len(arr)) + """
		echo 3 """ + script3
		
		os.system("bash -c '{0}'".format(script2))

#	while True: 

if __name__ == "__main__":
	processingClients()
