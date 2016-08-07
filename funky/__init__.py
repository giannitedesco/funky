from message import Message
import client, server

def xorp(k, c):
	from itertools import izip, cycle
	k = bytearray(k)
	c = bytearray(c)
	p = ''.join(chr(a ^ b) for (a,b) in izip(c, cycle(k)))
	return p


__all__ = (
		'client',
		'server',
		'xorp',
		'Message',
	)
