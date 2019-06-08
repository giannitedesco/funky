from .funkgame import FunkGame
from .message import Message
from .serverwindow import ServerWindow
from .gamewindow import GameWindow
from . import client, server
from hashlib import sha1

def xorp(k, c):
    from itertools import cycle
    p = ''.join(chr(ord(a) ^ ord(b)) for (a,b) in zip(c, cycle(k)))
    return p

def encrypt_login(params):
    key = '$Revision: 1.184 $'

    pt = f'{params.nam} {params.pwd}'.encode('utf-8')
    hd = sha1(pt).hexdigest()
    agb = hd #f'AGB:hd'

    enc = client.LoginClientMsg(
        enctyp = 'XORP',
        enckey = key,
        nam = xorp(key, params.nam),
        pwd = xorp(key, agb),
        client_type = xorp(key, params.client_type),
        client_id = xorp(key, params.client_id),
        jver = xorp(key, params.jver),
        osver = xorp(key, params.osver),
        client_ver = xorp(key, params.client_ver),
        mac = xorp(key, params.mac),
    )

    return enc

__all__ = (
        'client',
        'encrypt_login',
        'server',
        'xorp',
        'FunkGame',
        'GameWindow',
        'Message',
        'ServerWindow',
    )
