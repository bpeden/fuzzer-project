#!/usr/bin/python

## Template definitions
## Message templates to be used by a kitty Model are defined here.

## Templates can be verified with the "kitty-template-tester" tool that is
## automatically installed when you use "pip install kitty".
## Note: this only checks syntax to check if it's a valid model, not that the
## model is correct.

from kitty.model import *

http_get = Template(
	name = 'HTTP_GET', fields = [
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

http_post_basic = Template(
	name = 'HTTP_POST_Basic',
	fields = [
		Static('POST', name='method'),
		Delimiter(' ', name='space1'),
		String('/index.html', name='path'),
		Delimiter(' ', name='space2'),
		String('HTTP', name='protocol name'),
		Delimiter('/', name='fws1'),
		Dword(1, name='major version', encoder=ENC_INT_DEC),
		Delimiter('.', name='dot1'),
		Dword(1, name='minor version', encoder=ENC_INT_DEC),
		Static('\r\n\r\n', name='eom'),
		String('data')
	]
)
