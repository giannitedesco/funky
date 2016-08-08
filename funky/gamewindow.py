import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList
from playerlist import PlayerList
from marketview import MarketView
from resourceview import ResourceView
from mapview import MapView
from funkgame import FunkGame

class GameWindow(Gtk.Box):
	def __init__(self):
		# Callbacks for buttons pushed in child windows
		# TODO: change to signals
		def bid_cb(_, index, price):
			self.game.bid(index, price)
		def pass_cb(_):
			self.game.bid(-1, -1)
		def buy_cb(_, k, o, m, ke):
			self.game.buy_rs(k, o, m, ke)
		def build_cb(_, city):
			self.game.build(0, city)
		def nobuild_cb(_, city):
			self.game.build(1, 0)

		# Callbacks for game events
		def ps_cb(_, p, s):
			return
		def money_cb(_, money):
			self.player_list.update_player_money(money)
		def players_cb(_, nr, names):
			self.player_list.update_player_names(nr, names)
		def plants_cb(_, plants):
			self.player_list.update_player_plants(plants)
		def nr_city_cb(_, nr_city):
			self.player_list.update_player_cities(nr_city)
		def market_cb(_, cards_left, market):
			self.market.update_market(cards_left, market)
		def map_cb(_, nr, dists):
			self.map_window.set_map(nr, dists)
		def stock_cb(_, stock):
			self.stock.update_stock(*stock)
		def cities_cb(_, cities):
			self.map_window.update_cities(cities)

		super(GameWindow, self).__init__(\
				orientation = Gtk.Orientation.HORIZONTAL,
				spacing = 6)

		self.game = FunkGame()
		self.game.connect('update_ps', ps_cb)
		self.game.connect('update_money', money_cb)
		self.game.connect('update_players', players_cb)
		self.game.connect('update_plants', plants_cb)
		self.game.connect('update_nr_city', nr_city_cb)
		self.game.connect('update_market', market_cb)
		self.game.connect('update_map', map_cb)
		self.game.connect('update_stock', stock_cb)
		self.game.connect('update_cities', cities_cb)

		self.player_list = PlayerList()
		self.stock = ResourceView()
		self.market = MarketView()
		self.map_window = MapView()

		self.stock.connect('buy', buy_cb)
		self.market.connect('bid', bid_cb)
		self.market.connect('pass', pass_cb)
		self.map_window.connect('build', build_cb)
		#self.map_window.connect('finish-building', nobuild_cb)

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		vbox.pack_start(self.player_list, True, True, 0)
		vbox.pack_start(self.stock, False, True, 0)
		vbox.pack_start(self.market, False, True, 0)

		uscr = Gtk.ScrolledWindow()
		uscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
		uscr.add(vbox)

		pscr = Gtk.ScrolledWindow()
		pscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		pscr.add(self.map_window)

		self.pack_start(uscr, False, True, 0)
		self.pack_start(pscr, True, True, 0)
