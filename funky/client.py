from message import *

class QuitClientMsg(Message):
	_fields = tuple()
	_defaults = tuple()
	_types = tuple()
	_msgtype = 0

class CmdClientMsg(Message):
	_fields = ('cmd',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 1 

class InitClientMsg(Message):
	_fields = ('rm', 'gm', 'nation', 'name', 'jver')
	_defaults = ('43' ,'', 'en', '', '1.8.0_101')
	_types = (TStr, TStr, TStr, TStr, TStr)
	_msgtype = 2

class LoginClientMsg(Message):
	_fields = ('enctyp', 'enckey', 'nam', 'pwd',
			'client_type', 'client_id', 'jver', 'osver',
			'client_ver', 'mac')
	_defaults = ('PLAIN' ,'', 'name', '',
			'Client', 'BSW', '1.8.0_101', 'sparc-1.0-SunOS',
			'-- Client $Revision: 1.183 $ (Client)', '')
	_types = (TStr, TStr, TStr, TStr,
			TStr, TStr, TStr, TStr,
			TStr, TStr)
	_msgtype = 20

class PingClientMsg(Message):
	_fields = ()
	_defaults = ()
	_types = ()
	_msgtype = 23

class RefreshClientMsg(Message):
	_fields = tuple()
	_defaults = tuple()
	_types = tuple()
	_msgtype = 33

class LangInfoClientMsg(Message):
	_fields = ('langs',)
	_defaults = (tuple(),)
	_types = (TStr2Array,)
	_msgtype = 44

class FunkenCardClientMsg(Message):
	_fields = ('card',)
	_defaults = (-1,)
	_types = (TInt,)
	_msgtype = 200

class PlayerWantedClientMsg(Message):
	_fields = ('player',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 988

class GameStartClientMsg(Message):
	_fields = ()
	_defaults = ()
	_types = ()
	_msgtype = 989

class RoomChangeClientMsg(Message):
	_fields = ('room',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 991

class ToolClientMsg(Message):
	_fields = ('tool',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 20000

class Tool2ClientMsg(Message):
	_fields = ('key', 'value')
	_defaults = ('', '')
	_types = (TStr, TStr)
	_msgtype = 20001

msgmap = dict(((x._msgtype, x) for x in (\
		QuitClientMsg,
		CmdClientMsg,
		InitClientMsg,
		LoginClientMsg,
		PingClientMsg,
		RefreshClientMsg,
		LangInfoClientMsg,
		FunkenCardClientMsg,
		PlayerWantedClientMsg,
		GameStartClientMsg,
		RoomChangeClientMsg,
		ToolClientMsg,
		Tool2ClientMsg,
		)))
