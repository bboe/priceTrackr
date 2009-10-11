#!/usr/bin/python

# Copyright 2006 Bryce Boe

import sys,threading,Queue,os,signal
from functions import openUrl
from functions import parse

class Process(threading.Thread):
	def __init__(self,ids,results,update):
		threading.Thread.__init__(self)
		self.ids = ids
		self.results = results
		self.update = update
	def run(self):
		while True:
		 	if self.ids.empty():
		 		break
		 	try:
		 		id = self.ids.get(True,1)
		 	except Queue.Empty:
		 		continue
		 	self.results.put(parse(id,self.update))
	
def main():
	# SET DEFAULTS
	UPDATE = False
	NUMTHREADS = 1

	# Process arguments
	for arg in sys.argv[1:]:
		if arg == '-u':
			UPDATE = True
		elif arg[:2] == '-n':
			try:
				NUMTHREADS = int(arg[2:])
			except ValueError:
				sys.stderr.write('Invalid number of threads\n')
				sys.exit(1)
		else:
			sys.stderr.write('Invalid parameter: '+arg+'\n')
			sys.exit(1)

	# Setup queues
	ids = Queue.Queue(0)
	for line in sys.stdin:
			ids.put(line[:-1])
	n = ids.qsize()
	results = Queue.Queue(n)
	
	# Verify we need all the threads
	NUMTHREADS = min(n,NUMTHREADS)

	#Watcher()
	
	myThreads = []
	for x in xrange(NUMTHREADS):
		myThreads.append(Process(ids,results,UPDATE))
		myThreads[x].start()
		
	for x in xrange(n):
		try:
			for part in results.get():
				sys.stdout.write(str(part)+ "\t")
		except KeyboardInterrupt:
			sys.exit(1)
			
		try:
			sys.stdout.write('\n')
			sys.stdout.flush()
		except IOError:
			sys.exit(1)
	
if __name__ == '__main__':
	main()
