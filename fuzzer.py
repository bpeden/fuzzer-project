#!/usr/bin/python

from kitty.fuzzers.server import ServerFuzzer
from kitty.controllers import EmptyController
from kitty.interfaces.web import WebInterface
from kitty.model import GraphModel

from templates import http_get
from target import myTCPTarget

def main():
	
	template = http_get
	
	controller = EmptyController(name='Empty Controller (testing)')

	target = myTCPTarget(name='myTarget', host='localhost', port=80)
	target.set_controller(controller)

	model = GraphModel(name='mysimpleHTTPModel')
	model.connect(template)

	interface = WebInterface(host='localhost', port=8081)

	## The fuzzer is the top-level object.  Ties the model to the target and the monitor
	## and controller.  Docs say it doesn't need to be subclassed.
	fuzzer = ServerFuzzer(name='myServerFuzzer')

	fuzzer.set_interface(interface)
	fuzzer.set_model(model)
	fuzzer.set_target(target)

	fuzzer.start()
	print "Fuzzer done."
	raw_input('press enter to exit')
	fuzzer.stop()

if __name__ == '__main__':
	main()
