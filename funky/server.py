from message import *

class QuitServerMsg(Message):
	_fields = tuple()
	_defaults = tuple()
	_types = tuple()
	_msgtype = 0

class CmdServerMsg(Message):
	_fields = ('cmd',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 1 

class TellServerMsg(Message):
	_fields = ('response', 'from', 'ort')
	_defaults = ('', '', '')
	_types = (TStr, TStr, TStr)
	_msgtype = 2

class Spam6ServerMsg(Message):
	_fields = ('x', 'y', 'z')
	_defaults = ('', -1, '')
	_types = (TStr, TInt, TStr)
	_msgtype = 6

class Spam8ServerMsg(Message):
	_fields = ('x', 'y')
	_defaults = (-1, -1)
	_types = (TInt, TInt)
	_msgtype = 8

class SoundServerMsg(Message):
	_fields = ('snr','sndpack')
	_defaults = (-1, '')
	_types = (TInt, TStr,)
	_msgtype = 19

class PingServerMsg(Message):
	_fields = ()
	_defaults = ()
	_types = ()
	_msgtype = 23

class PongServerMsg(Message):
	_fields = ()
	_defaults = ()
	_types = ()
	_msgtype = 24

class RefreshServerMsg(Message):
	_fields = tuple()
	_defaults = tuple()
	_types = tuple()
	_msgtype = 33

class LangInfoServerMsg(Message):
	_fields = ('langs',)
	_defaults = (tuple(),)
	_types = (TStr2Array,)
	_msgtype = 44

class FunkenBoardServerMsg(Message):
	_fields = ('target', 'dist', 'card',)
	_defaults = ('', tuple(), -1)
	_types = (TStr, TInt2Array, TInt)
	_msgtype = 200

class FunkenPlayerServerMsg(Message):
	_fields = ('target', 'player1', 'player2', 'player3',
			'player4', 'player5', 'player6', 'running',
			'round', 'phase', 'current_player', 'nr_players',
			'i_am_id', 'stufe', 'sequence', 'money',
			'bid', 'ok')
	_defaults = ('', '', '', '',
			'', '', '', False,
			-1, -1, -1, -1,
			-1, -1, tuple(), tuple(),
			tuple(), tuple())

	_types = (TStr, TStr, TStr, TStr,
			TStr, TStr, TStr, TBool,
			TInt, TInt, TInt, TInt,
			TInt, TInt, TIntArray, TIntArray,
			TIntArray, TBoolArray)
	_msgtype = 201

class FunkenAuctionServerMsg(Message):
	_fields = ('target', 'cards_left', 'market', 'provider',
			'in_play', 'bid', 'act_provider', 'new',
			'old', 'money', 'phase_stufe')
	_defaults = ('', -1, tuple(), tuple(),
			tuple(), tuple(), -1, -1,
			-1, -1, -1)
	_types = (TStr,TInt,TIntVector,TIntVector,
			TIntVector, TIntArray, TInt, TInt,
			TInt, TIntArray, TInt)
	_msgtype = 202

class FunkenCityServerMsg(Message):
	_fields = ('target', 'city', 'city_active', 'nr_city',
			'money', 'build_cost', 'phase_stufe', 'currentPlayer')
	_defaults = ('', tuple(), tuple(), tuple(),
			tuple(), tuple(), -1, -1)
	_types = (TStr,TInt2Array,TBoolArray,TInt2Array,
			TIntArray, TIntArray, TInt, TInt)
	_msgtype = 203

class FunkenMaterialsServerMsg(Message):
	_fields = ('target', 'stock', 'fires', 'materials',
			'money', 'newRs', 'revenue', 'phase',
			'currentPlayer')
	_defaults = ('', tuple(), tuple(), tuple(),
			tuple(), tuple(), tuple(), -1,
			-1)
	_types = (TStr,TIntArray,TIntArray,TInt3Array,
			TIntArray, TIntArray, TIntArray, TInt,
			TInt,)
	_msgtype = 204

class FunkenScoreServerMsg(Message):
	_fields = ('target', 'plants', 'nr_city', 'rs_weg')
	_defaults = ('', tuple(), tuple(), tuple())
	_types = (TStr,TInt2Array,TInt2Array,TIntArray)
	_msgtype = 205

class FunkenUnusedServerMsg(Message):
	_fields = ('target', )
	_defaults = ('', )
	_types = (TStr,)
	_msgtype = 206

class FunkenExchangeServerMsg(Message):
	_fields = ('target', 'message', 'exchange')
	_defaults = ('', tuple(), tuple())
	_types = (TStr,TIntArray,TIntArray)
	_msgtype = 207

class FunkenAnimServerMsg(Message):
	_fields = ('target', 'message',)
	_defaults = ('', tuple())
	_types = (TStr,TIntArray)
	_msgtype = 208

class PlayerWantedServerMsg(Message):
	_fields = ('player',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 988

class GameStartServerMsg(Message):
	_fields = ('tree',)
	_defaults = ('' ,)
	_types = (TStr,)
	_msgtype = 989

class RoomChangeServerMsg(Message):
	_fields = ('room',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 991

class ToolServerMsg(Message):
	_fields = ('tool',)
	_defaults = ('',)
	_types = (TStr,)
	_msgtype = 20000

class Tool2ServerMsg(Message):
	_fields = ('key', 'value')
	_defaults = ('', '')
	_types = (TStr, TStr)
	_msgtype = 20001

class YellServerMsg(Message):
	_fields = ('yel0', 'yel1', 'yel2', 'yel3', 'yel4',)
	_defaults = ('', '', '', '', '', '')
	_types = (TStr, TStr, TStr, TStr, TStr)
	_msgtype = 10070

msgmap = dict(((x._msgtype, x) for x in (\
		QuitServerMsg,
		CmdServerMsg,
		TellServerMsg,
		Spam6ServerMsg,
		Spam6ServerMsg,
		Spam8ServerMsg,
		SoundServerMsg,
		PingServerMsg,
		PongServerMsg,
		RefreshServerMsg,
		LangInfoServerMsg,
		FunkenBoardServerMsg,
		FunkenPlayerServerMsg,
		FunkenAuctionServerMsg,
		FunkenCityServerMsg,
		FunkenMaterialsServerMsg,
		FunkenScoreServerMsg,
		FunkenUnusedServerMsg,
		FunkenExchangeServerMsg,
		FunkenExchangeServerMsg,
		FunkenAnimServerMsg,
		GameStartServerMsg,
		RoomChangeServerMsg,
		ToolServerMsg,
		Tool2ServerMsg,
		YellServerMsg,
		)))
