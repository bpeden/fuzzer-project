#!/usr/bin/python

## Template definitions
## Message templates to be used by a kitty Model are defined here.

## Templates can be verified with the "kitty-template-tester" tool that is
## automatically installed when you use "pip install kitty".
## Note: this only checks syntax to check if it's a valid model, not that the
## model is correct.

from kitty.model import *

http_apache_crash = Template(
	name = 'HTTP_APACHE_CRASH', fields = [
		String('\x16\x03\x03'),
		Static('\r\n\r\n', name='eom')]
	)

http_nginx_win_crash_1 = Template(
	name = 'HTTP_NGINX_CRASH_1', fields =[
		Static('GET '),
		String('/%c0./%c0./%c0.%c0./%c0.%c0./%c0.%c0./%20'),
		Static('HTTP/1.1'),
		Static('\r\n\r\n', name='eom')
		]
	)

http_nginx_win_crash_2 = Template(
	name = 'HTTP_NGINX_CRASH_2', fields =[
		Static('GET '),
		String('/%c0./%c0./%c0.%c0./%c0.%c0./%20'),
		Static('HTTP/1.1'),
		Static('\r\n\r\n', name='eom')
		]
	)

http_nginx_win_crash_3 = Template(
	name = 'HTTP_NGINX_CRASH_3', fields =[
		Static('GET '),
		String('/%c0./%c0./%c0.%c0./%20'),
		Static('HTTP/1.1'),
		Static('\r\n\r\n', name='eom')
		]
	)

http_lighttpd_crash = Template(
	name = 'HTTP_LIGHTTPD_CRASH', fields =[
		String('GET / HTTP/1.1\r\nHost: pwn.ed\r\nConnection: TE,,Keep-Alive\r\n\r\n')
		]
	)



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
		Static('\n'),
		
		# Can we generate a random domain here??
		String("Referrer:", fuzzable=False),
		Delimiter(' '),
		String("www."),
		String("host"),
		String(".com"),		
		Static('\n'),

		String("User-Agent:", fuzzable=False),
		Delimiter(' '),
		String("Mozilla Firesocks"),
		Static('\n'),

		# Can we get the domain of the host here?
		String("Host:", fuzzable=False),
		Delimiter(' '),
		String("host.com"),
		Static('\n'),		

		String("Accept:", fuzzable=False),
		Delimiter(' '),
		String("text/plain"),
		Static('\n'),

		String("Accept-Encoding:", fuzzable=False),
		Delimiter(' '),
		String("gzip"),
		Delimiter(','),
		String("deflate"),
		Static('\n'),

		String("Accept-Language:", fuzzable=False),
		Delimiter(' '),
		String("en-US"),
		Static('\n'),		

		# Can we put in a date here?
		String("If-Modified-Since:", fuzzable=False),
		Delimiter(' '),
		String("Sat, 29 Oct 1994 19:43:31 GMT"),
		Static('\n'),

		String("Cookie:", fuzzable=False),
		Delimiter(' '),
		String("Gee I Sure Love A Good Cookie!"),
		Static('\n'),

		String("Range:", fuzzable=False),
		Delimiter(' '),
		String("Bytes="),
		Dword(0),
		Delimiter('-'),
		Dword(1024),
		Static('\n'),

		String("If-Range:", fuzzable=False),
		Delimiter(' '),
		Sha1('method'),
		Static('\n'),

		# Used for PUSH requests!
		#String("Content-Type:", fuzzable=False),
		#Delimiter(' '),
		#String("application/x-www-form-urlencoded"),
		#Static('\n'),		

		String("Content-Length:", fuzzable=False),
		Delimiter(' '),
		Dword(348),
		Static('\n'),

		# This will give us too many drops
		#String("Authorization:", fuzzable=False),
		#Delimiter(' '),
		#String("authenticate_me!")
		#Static('\n'),

		String("Connection:", fuzzable=False),
		Delimiter(' '),
		String("keep-alive"),
		Static('\n'),
		

		Static('\r\n\r\n', name='eom'),
	]
)

http_post = Template(
	name = 'HTTP_POST',
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
