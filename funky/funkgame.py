import server, client
from gi.repository import GObject

class FunkGame(GObject.GObject):
	__gsignals__ = {
		# Emitted with a Message which should be sent to server
		'tx_msg':
			(GObject.SIGNAL_RUN_LAST, None, (object, )),

		# Emitted with any unhandled messages
		'rx_unhandled':
			(GObject.SIGNAL_RUN_LAST, None, (object, )),

		# Emitted for any chat messages
		'chat_msg':
			(GObject.SIGNAL_RUN_LAST, None, (str, )),

		# Emitted for any chat messages
		'log':
			(GObject.SIGNAL_RUN_LAST, None, (str, )),

		# Game status updates
		'update_ps':
			(GObject.SIGNAL_RUN_LAST, None, (int, int)),
		'update_money':
			(GObject.SIGNAL_RUN_LAST, None, (object, )),
		'update_players':
			(GObject.SIGNAL_RUN_LAST, None, (int, object)),
		'update_plants':
			(GObject.SIGNAL_RUN_LAST, None, (object,)),
		'update_nr_city':
			(GObject.SIGNAL_RUN_LAST, None, (object,)),
		'update_market':
			(GObject.SIGNAL_RUN_LAST, None, (int, object)),
		'update_map':
			(GObject.SIGNAL_RUN_LAST, None, (int, object)),
		'update_stock':
			(GObject.SIGNAL_RUN_LAST, None, (object,)),
		'update_cities':
			(GObject.SIGNAL_RUN_LAST, None, (object,)),
		'update_plant_stock':
			(GObject.SIGNAL_RUN_LAST, None, (object, )),
		'update_current_player':
			(GObject.SIGNAL_RUN_LAST, None, (int, int)),
		'update_city_active':
			(GObject.SIGNAL_RUN_LAST, None, (object, )),
		'update_bid':
			(GObject.SIGNAL_RUN_LAST, None, (int, int, int)),
	}

	def __init__(self):
		super(GObject.GObject, self).__init__()
		self.phase = -1
		self.stufe = -1
		self.round = -1

		self.nr_players = 0
		self.i_am_id = -1
		self.sequence = (-1, -1, -1, -1, -1, -1)
		self.players = (' ', ' ', ' ', ' ', ' ', ' ')
		self.money = (50, 50, 50, 50, 50, 50)
		self.plants = ((-1, -1, -1, -1),
				(-1, -1, -1, -1),
				(-1, -1, -1, -1),
				(-1, -1, -1, -1),
				(-1, -1, -1, -1),
				(-1, -1, -1, -1))
		self.nr_city = ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0))
		self.market = (-1, -1, -1, -1, -1, -1, -1, -1)
		self.cur_bid = (-1, 0, -1)
		self.cards_left = 0
		self.map_nr = -1
		self.stock = None
		self.dist = None
		self.cities = None
		self.plant_stock = None
		self.city_active = None
		self.current_player = -1
		self.i_am = -1

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

	def update_ps(self, phase, stufe):
		old_ps = (self.phase, self.stufe)
		self.phase = phase
		self.stufe = stufe
		if (self.phase, self.stufe) == old_ps:
			return
		self.emit('update_ps', self.phase, self.stufe)

	def update_money(self, money):
		if not money:
			return
		old_money = self.money
		self.money = money
		if self.money == old_money:
			return
		self.emit('update_money', self.money)

	def update_plant_stock(self, plant_stock):
		if not plant_stock:
			return
		old_plant_stock = self.plant_stock
		self.plant_stock = plant_stock
		if self.plant_stock == old_plant_stock:
			return
		self.emit('update_plant_stock', self.plant_stock)

	def update_players(self, nr, players):
		if not players:
			return
		old_players = (self.nr_players, self.players)
		self.players = players
		self.nr_players = nr
		if (self.nr_players, self.players) == old_players:
			return
		self.emit('update_players', self.nr_players, self.players)

	def update_market(self, nr, market):
		if not market:
			return
		old_market = (self.cards_left, self.market)
		self.market = market
		self.cards_left = nr
		if (self.cards_left, self.market) == old_market:
			return
		self.emit('update_market', self.cards_left, self.market)

	def update_plants(self, plants):
		if not plants:
			return
		old_plants = self.plants
		self.plants = plants
		if self.plants == old_plants:
			return
		self.emit('update_plants', self.plants)

	def update_nr_city(self, nr_city):
		if not nr_city:
			return
		old_nr_city = self.nr_city
		self.nr_city = nr_city
		if self.nr_city == old_nr_city:
			return
		self.emit('update_nr_city', self.nr_city)

	def update_map(self, nr, dist):
		if not dist:
			return
		old_dists = (self.map_nr, self.dist)
		self.dist = dist
		self.map_nr = nr
		if (self.map_nr, self.dist) == old_dists:
			return
		self.emit('update_map', self.map_nr, self.dist)

	def update_stock(self, stock):
		if not stock:
			return
		old_stock = self.stock
		self.stock = stock
		if self.stock == old_stock:
			return
		self.emit('update_stock', self.stock)

	def update_cities(self, cities):
		if not cities:
			return
		old_cities = self.cities
		self.cities = cities
		if self.cities == old_cities:
			return
		self.emit('update_cities', self.cities)

	def update_current_player(self, current_player):
		old_cp = self.current_player
		self.current_player = current_player
		if self.current_player == old_cp:
			return
		self.emit('update_current_player',
				self.current_player,
				self.i_am)

	def update_city_active(self, city_active):
		if not city_active:
			return
		old_city_active = self.city_active
		self.city_active = city_active
		if self.city_active == old_city_active:
			return
		self.emit('update_city_active', self.city_active)

	def update_bid(self, cur_bid):
		if not cur_bid:
			return
		old_bid = self.cur_bid
		self.cur_bid = cur_bid
		if self.cur_bid == old_bid:
			return
		self.emit('update_bid', *self.cur_bid)

	def dispatch(self, msg):
		def nop_cb(msg):
			return
		def ping_cb(msg):
			self.pong()
		def chat_cb(msg):
			self.chat(msg.cmd)

		def map_cb(msg):
			maps = ('usa.jpg', 'deut.jpg',
				'frankreich.jpg', 'italien.jpg', 'bw.jpg')
			self.update_map(msg.map, msg.dist)

		def player_cb(msg):
			self.round = msg.round
			self.update_ps(msg.phase, msg.stufe)

			if msg.sequence:
				self.sequence = msg.sequence

			self.i_am_id = int(msg.i_am_id)

			an = ('player%d'%x for x in xrange(1, 7))
			players = tuple(map(lambda x:getattr(msg, x), an))
			self.update_players(int(msg.nr_players), players)

			self.update_money(msg.money)

			self.i_am = msg.i_am_id
			self.update_current_player(msg.current_player)

		def score_cb(msg):
			self.update_plants(msg.plants)
			self.update_nr_city(msg.nr_city)

		def auction_cb(msg):
			phase = msg.phase_stufe & 0x3ff
			stufe = msg.phase_stufe >> 10
			self.update_ps(phase, stufe)

			self.update_money(msg.money)

			self.update_current_player(msg.current_player)

			self.update_market(msg.cards_left, msg.market)
			self.update_bid(msg.bid)

		def materials_cb(msg):
			self.update_ps(msg.phase, self.stufe)
			self.update_money(msg.money)
			self.update_stock(msg.stock)
			self.update_plant_stock(msg.materials)
			self.update_current_player(msg.current_player)

		def city_cb(msg):
			phase = msg.phase_stufe & 0x3ff
			stufe = msg.phase_stufe >> 10
			self.update_ps(phase, stufe)
			self.update_cities(msg.city)
			self.update_city_active(msg.city_active)
			self.update_nr_city(msg.nr_city)
			self.update_money(msg.money)
			self.update_current_player(msg.current_player)

		disp = {
			server.PingServerMsg: ping_cb,
			server.CmdServerMsg: chat_cb,
			server.FunkenMapServerMsg: map_cb,
			server.FunkenPlayerServerMsg: player_cb,
			server.FunkenScoreServerMsg: score_cb,
			server.FunkenAuctionServerMsg: auction_cb,
			server.FunkenMaterialsServerMsg: materials_cb,
			server.FunkenCityServerMsg: city_cb,
			server.FunkenUnusedServerMsg: nop_cb,
			server.FunkenAnimServerMsg: nop_cb,
		}

		# dispatch the message
		cb = disp.get(msg.__class__, None)
		if cb is None:
			self.rx_unhandled(msg)
			return

		cb(msg)

	def rx_msg(self, t, b):
		'Handles a message received from the server'
		# figure out the type of message
		c = server.msgmap.get(t, None)
		if c is None:
			self.log('UNKNOWN(%r), %r'%(t, b))
			return

		# parse the message from the bytes
		msg = c.frombytes(b)

		self.dispatch(msg)

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
			self.demolish(int(args))

		def rsmove_cb(cmd, args):
			frm, to, rs = args.split(None, 2)
			self.rs_move(int(frm), int(to), int(cb))

		def eval_cb(cmd, args):
			x = eval(args)
			self.dispatch(x)

		disp = {
			'pass': pass_cb,
			'bid': bid_cb,
			'rs': rs_cb,
			'build': build_cb,
			'nobuild': nobuild_cb,
			'fire': fire_cb,
			'demolish': demolish_cb,
			'rsmove': rsmove_cb,
			'eval': eval_cb,
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
		self.action(1, plant, 0, 0, 0)

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
