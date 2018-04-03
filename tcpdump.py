#!/usr/bin/python

import threading, time
import subprocess
from subprocess import Popen, PIPE


class tcpdump():
    def runningCommand(self):
        interface = input("write your interface name: ")
        tcpdumpCommand = "tcpdump -vvs 0 -i " + str(interface) + " -en | tee /dev/tty | nc 127.0.0.1 8888"
        #should call pipe for the subprocess to read and write simultaneously
        proc = Popen(tcpdumpCommand, stdout = PIPE, shell = True)
        print("aaaa")
	
        while proc.poll() is None:
            #for every incoming line we should block and then read it
            line = proc.stdout.readline()
            print("helllllo")
            print(line)

if __name__ == '__main__':
    tcpdump().runningCommand()
