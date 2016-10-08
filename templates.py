#!/usr/bin/python

## Template definitions
## Message templates to be used by a kitty Model are defined here.

from kitty.model import *


http_get = Template(
	name = 'HTTP_GET_V2', fields = [
		String('GET', name='method', fuzzable=False),
		Delimiter(' ', name='space1', fuzzable=False),
		String('/index.html', name='path'),
		Delimiter(' ', name ='space2'),
		String('HTTP', name='protocol name'),
		Delimiter('/', name='fws1'),
		Dword(1, name='major version', encoder=ENC_INT_DEC),
		Delimiter('.', name='dot1'),
		Dword(1, name='minor version', encoder=ENC_INT_DEC),
		Static('\r\n\r\n', name='eom'),
	]
)
