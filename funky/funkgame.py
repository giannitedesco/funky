import server, client
from gi.repository import GObject

class FunkGame(GObject.GObject):
	__gsignals__ = {
		# Emitted with a Message which should be sent to server
		'tx_msg': (GObject.SIGNAL_RUN_LAST, None, (object, )),

		# Emitted with any unhandled messages
		'rx_unhandled': (GObject.SIGNAL_RUN_LAST, None, (object, )),

		# Emitted for any chat messages
		'chat_msg': (GObject.SIGNAL_RUN_LAST, None, (str, )),

		# Emitted for any chat messages
		'log': (GObject.SIGNAL_RUN_LAST, None, (str, )),
	}

	def __init__(self):
		super(GObject.GObject, self).__init__()

	def tx(self, msg):
		'Emits a message to transmit to server'
		self.emit('tx_msg', msg)

	def chat(self, s):
		'Emits a chat message'
		self.emit('chat_msg', s)

	def log(self, s):
		'Emits a log message'
		self.emit('log', s)

	def rx_unhandled(self, msg):
		self.emit('rx_unhandled', msg)

	def pong(self):
		x = client.PingClientMsg()
		self.tx(x)

	def rx_msg(self, t, b):
		'Handles a message received from the server'
		def ping_cb(msg):
			self.pong()
		def chat_cb(msg):
			self.chat(msg.cmd)

		disp = {
			server.PingServerMsg: ping_cb,
			server.CmdServerMsg: chat_cb,
		}

		# figure out the type of message
		c = server.msgmap.get(t, None)
		if c is None:
			self.log('UNKNOWN(%r), %r'%(t, b))
			return

		# parse the message from the bytes
		msg = c.frombytes(b)

		# dispatch the message
		cb = disp.get(c, None)
		if cb is None:
			self.rx_unhandled(msg)
			return

		cb(msg)

	def cl_cmd(self, cmd):
		'Receive a string typed in to server window'
		if len(cmd) >=2 and cmd[:2] == '//':
			self.game_cmd(cmd[2:])
		else:
			self.sys_cmd(cmd)

	def sys_cmd(self, cmd):
		'Send a command message'
		x = client.CmdClientMsg(cmd = cmd)
		self.tx(x)

	def game_cmd(self, cmd):
		'Send a Funken game command'

		def pass_cb(cmd, args):
			self.bid(-1, -1)

		def bid_cb(cmd, args):
			k, p = args.split(None, 2)
			self.bid(int(k), int(p))

		def rs_cb(cmd, args):
			k, o, m, ke = args.split(None, 3)
			self.buy_rs(int(k), int(o), int(m), int(ke))

		def build_cb(cmd, args):
			self.build(0, int(args))

		def nobuild_cb(cmd, args):
			self.build(1, 0)

		def fire_cb(cmd, args):
			a, b, c, d = args.split(None, 3)
			self.fire(int(a), int(b), int(c), int(d))

		def demolish_cb(cmd, args):
			self.demolish(0, int(args))

		def rsmove_cb(cmd, args):
			frm, to, rs = args.split(None, 2)
			self.rs_move(int(frm), int(to), int(cb))

		disp = {
			'pass': pass_cb,
			'bid': bid_cb,
			'rs': rs_cb,
			'build': build_cb,
			'nobuild': nobuild_cb,
			'fire': fire_cb,
			'demolish': demolish_cb,
			'rsmove': rsmove_cb,
		}
		try:
			cmd, args = cmd.split(None, 1)
		except ValueError:
			cmd = cmd
			args = None
		cb = disp.get(cmd, None)
		if cb is None:
			self.chat('Unknwon game command: %s'%cmd)
		else:
			cb(cmd, args)

	def demolish(self, plant):
		self.action(0, plant, 0, 0, 0)

	def fire(self, a, b, c, d):
		self.action(0, a, b, c, d)

	def buy_rs(self, coal, oil, trash, nuke):
		self.action(0, coal, oil, trash, nuke)

	def rs_move(self, frm, to, rs):
		self.action(2, frm, to, rs, 0)

	def build(self, act, s):
		self.action(act, s, 0, 0, 0)

	def bid(self, k, p):
		if k < 0:
			k = 0x3f
		if p < 0:
			p = 0x3f
		code = (p << 6) | k
		x = client.FunkenClientMsg(code = code)
		self.tx(x)

	def action(self, act, k, p, p1, p2):
		code = (act << 28)
		code |= k
		code |= p << 6
		code |= p1 << 12
		code |= p2 << 18
		x = client.FunkenClientMsg(code = code)
		self.tx(x)
