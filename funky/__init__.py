from message import Message
from serverwindow import ServerWindow
import client, server

def xorp(k, c):
	from itertools import izip, cycle
	k = bytearray(k)
	c = bytearray(c)
	p = ''.join(chr(a ^ b) for (a,b) in izip(c, cycle(k)))
	return p

def encrypt_login(x):
	key = '$Revision: 1.183 $'
	x = client.LoginClientMsg(
		enctyp = 'XORP',
		enckey = key,
		nam = xorp(key, x.nam),
		pwd = xorp(key, x.pwd),
		client_type = xorp(key, x.client_type),
		client_id = xorp(key, x.client_id),
		jver = xorp(key, x.jver),
		osver = xorp(key, x.osver),
		client_ver = xorp(key, x.client_ver),
		mac = xorp(key, x.mac),
	)

	return x

__all__ = (
		'client',
		'encrypt_login',
		'server',
		'xorp',
		'Message',
		'ServerWindow',
	)
