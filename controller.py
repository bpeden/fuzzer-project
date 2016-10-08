#!/usr/bin/python

## Controller definition
## Starts and Preps the victim process for fuzzing.  Basic monitoring - Reports crashes

import os

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
