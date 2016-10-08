#!/usr/bin/python

import os

from kitty.model import *

## STEP 1 - the Template class.  Define a data model to show kitty what the
## protocol looks like.

http_get_1 = Template(
	name = 'HTTP_GET_V1', fields = [
		String('GET', name='method'),
		Delimiter(' ', name='space1'),
		String('/index.html', name='path'),
		Delimiter(' ', name ='space2'),
		String('HTTP/1.1', name='protocol name'),
		Delimiter('\r\n\r\n', name='eom'),
	]
)

## A more complex version of the above - not necessarily better.  The closer you
## get to a perfect representation of the protocol, the less room there is for
## generating weird cases.

http_get_2 = Template(
	name = 'HTTP_GET_V2', fields = [
		String('GET', name='method'),
		Delimiter(' ', name='space1'),
		String('/index.html', name='path'),
		Delimiter(' ', name ='space2'),
		String('HTTP', name='protocol name'),
		Delimiter('/', name='fws1'),
		Dword(1, name='major version', encoder=ENC_INT_DEC),
		Delimiter('.', name='dot1'),
		Dword(1, name='minor version', encoder=ENC_INT_DEC),
		Delimiter('\r\n\r\n', name='eom'),
	]
)


## 2 ways to get a non-fuzzable field
http_get_3 = Template(
	name = 'HTTP_GET_V2', fields = [
## Method 1. set fuzzable=False.  This lets us preserver the structure of the
## model
		String('GET', name='method', fuzzable=False),
		Delimiter(' ', name='space1', fuzzable=False),
		String('/index.html', name='path'),
		Delimiter(' ', name ='space2'),
		String('HTTP', name='protocol name'),
		Delimiter('/', name='fws1'),
		Dword(1, name='major version', encoder=ENC_INT_DEC),
		Delimiter('.', name='dot1'),
		Dword(1, name='minor version', encoder=ENC_INT_DEC),
## Method 2: Use Static: an immutable object.  Improves readability, especially
## if we have long chunks of data.
		Static('\r\n\r\n', name='eom'),
	]
)


## STEP ? - The Model class
## The model calss defines how the Templates are used

from kitty.model import GraphModel

class myModel(GraphModel):
	'''
	GraphModel is a Model built from a digraph where nodes are Templates
	(see above) and edges do callbacks.

	The last node (Template) in the chain is the one that gets mutated.

	e.g., if you're trying to fuzz something that requires setup, say the
	third part of a TCP 3 way handshake, you would need a graph that looked
	something like:
		SYN -> ACK
	The SYN is sent as normal, the edge callback handles the SYN-ACK
	response, and the last node in the chain, the ACK, gets fuzzed.

	''' 
	pass


## STEP 2 - The Target class

## There is already a built-in TCP target class:
# kitty.targets.tcp.TcpTarget
## but you can build your own as shown below:

## usage:
## 1. inherit from SevrerTarget
## 2. All overridden methods should call super except for:
##      _send_to_target
##   and
##      _receive_from_target

import socket
from kitty.targets.server import ServerTarget

class myTCPTarget(ServerTarget):
	def __init__(self, name, host, port, timeout=None, logger=None):
		'''
		:param name: name of the Target object
		:param host: hostname of target
		:param port: tcp port of target
		:param timeout: socket timeout
		:param logger: logger for this object (?)
		'''
		super(myTCPTarget, self).__init__(name, logger)
		self.host 	= host
		self.port 	= port
		self.timeout 	= timeout
		self.socket 	= None

		if (host is None) or (port is None):
			raise ValueError('host and port are required')

	def pre_test(self, test_num):
		'''
		prepare to do the test; create a socket;
		'''
		super(myTCPTarget, self).pre_test(test_num)
		if (self.socket is None):
			sock = self._get_socket()
			if self.timeout is not None:
				sock.settimeout(self.timeout)
			sock.connect((self.host, self.port))
			self.socket = sock
	
	def _get_socket(self):
		'''get a socket object'''
		return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def post_test(self, test_num):
		'''
		Called after a test is completed, perform cleanup etc.
		'''
## Call super to prep the report
		super(myTCPTarget, self).post_test(test_num)
		if self.socket is not None:
			self.socket.close()
			self.socket = None
	
	def _send_to_target(self, data):
		self.socket.send(data)
	
	def _receive_from_target(self):
		return self.socket.recv(10000)


## STEP 3 - the Controller class
## Starts and Preps the victim process for fuzzing.  Basic monitoring - Reports crashes
## "makes sure the victim is ready and reports a failure if it's not"


from kitty.controllers.base import BaseController

class LocalProcessController(BaseController):
	'''
	LocalProcessController is a process controller that was opened using
	subprocess.Popen.  This process will be created for each test and killed
	at the end of the test.
	'''

	def __init__(self, name, process_path, process_args, logger=None):
		'''
		:param name: name of the controller object
		:param process_path: path to the target executable
		:param process_args: arguments to pass to the process
		:param logger: logger for this object (?)
		'''
		super(ClientProcessController, self).__init__(name,logger)
		assert(process_path)
		assert(os.path.exists(process_path))
		self._process_path = process_path
		self._process_name = os.path.basename(process_path)
		self._process_args = process_args
		self._process = None
	
	def pre_test(self, test_num):
		'''start the victim'''
		if self._process:
			self._stop_process()
		cmd = [self._process_path] + self._process_args
# start the process
		self._process = Popen(cmd, stdout=PIPE, stderr=PIPE)
# Add process info to the report
		self.report.add('process_name'. self._process_name)
		self.report.add('process_path'. self._process_path)
		self.report.add('process_args'. self._process_args)
		self.report.add('process_id'. self._process_id)

	def post_test(self):
		'''called when the test is done'''
		self._stop_process()
# Make sure the process was started by us
		assert(self._process)
# Add process info to the report
		self.report.add('stdout', self._process.stdout.read())
		self.report.add('stderr', self._process.stderr.read())
		self.logger.debug('return code: %d', self._process.returncode)
		self.report.add('return_code', self._process.returncode)
		self.report.add('failed', self._process.returncode != 0) # obviously...
		self._process = None
		super(ClientProcessController, self).post_test()
	
	def teardown(self):
		'''
		Called at the end of the fuzzing session, overide with victime
		teardown.
		'''
		self._stop_process()
		self._process = None
		super(ClientProcessController, self).teardown()
	
	def _stop_process(self):
		if self._is_victim_alive():
			self._process.terminate()
			time.sleep(0.5)
			if self._is_victim_alive():
				raise Exception('Failed to kill process')
	
	def _is_victim_alive(self):
		return self._process and (self._process.poll() is None)



## STEP ? - Monitor

class myMonitor():
	pass



## STEP ? - Interface - provides a user interface to check the fuzzer status.
## The docs reccommend a web UI...

from kitty.fuzzers.server import ServerFuzzer
from kitty.controllers import EmptyController
from kitty.interfaces.web import WebInterface

def main():
	
	template = http_get_3
	
	controller = EmptyController(name='Empty Controller (testing)')

	target = myTCPTarget(name='myTarget', host='localhost', port=7657)
	target.set_controller(controller)

	model = GraphModel(name='mysimpleHTTPModel')
	model.connect(template)

	interface = WebInterface(host='localhost', port=8081)

## The fuzzer is the top-level object.  ties the model to the target and the monitor
## and controller.  Docs say it doesn't need to be subclassed.
	fuzzer = ServerFuzzer(name='myServerFuzzer')

	
	fuzzer.set_interface(interface)
	fuzzer.set_model(model)
	fuzzer.set_target(target)

	fuzzer.start()
	print "Fuzzer done."
	raw_imput('press enter to exit')
	fuzzer.stop()

if __name__ == '__main__':
	main()
