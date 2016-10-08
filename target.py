#!/usr/bin/python

## Target definition

## Alternatively, use the pre-defined:
# kitty.targets.tcp.TcpTarget

## usage:
## 1. inherit from SevrerTarget
## 2. All overridden methods should call super except for:
##      _send_to_target
##   and
##      _receive_from_target

import socket
from kitty.targets.server import ServerTarget

class myTCPTarget(ServerTarget):
	'''
	An ipv4 TCP server target.
	'''
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
