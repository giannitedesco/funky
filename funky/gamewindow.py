import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList
from playerlist import PlayerList
from marketview import MarketView
from resourceview import ResourceView
from mapview import MapView

class GameWindow(Gtk.Box):
	__gsignals__ = {
		'bid':
			(GObject.SIGNAL_RUN_LAST, None, (int, int)),
		'pass':
			(GObject.SIGNAL_RUN_LAST, None, ()),
		'buy':
			(GObject.SIGNAL_RUN_LAST, None, (int, int, int, int)),
	}
	def __init__(self):
		def bid_cb(index, price):
			self.emit('bid', index, price)
		def pass_cb():
			self.emit('pass')
		def buy_cb(k, o, m, ke):
			self.emit('buy', k, o, m, ke)
		super(GameWindow, self).__init__(\
				orientation = Gtk.Orientation.HORIZONTAL,
				spacing = 6)

		self.player_list = PlayerList()
		self.stock = ResourceView(buy_cb)
		self.market = MarketView(bid_cb, pass_cb)
		self.map_window = MapView()

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		vbox.pack_start(self.player_list, True, True, 0)
		vbox.pack_start(self.stock, True, True, 0)
		vbox.pack_start(self.market, False, True, 0)

		uscr = Gtk.ScrolledWindow()
		uscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
		uscr.add(vbox)

		pscr = Gtk.ScrolledWindow()
		pscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		pscr.add(self.map_window)

		self.pack_start(uscr, False, True, 0)
		self.pack_start(pscr, True, True, 0)

	def update_player_names(self, nr, names):
		self.player_list.update_player_names(nr, names)

	def update_player_plants(self, plants):
		self.player_list.update_player_plants(plants)

	def update_player_money(self, money):
		self.player_list.update_player_money(money)

	def update_player_cities(self, cities):
		self.player_list.update_player_cities(cities)

	def update_market(self, cards_left, market):
		self.market.update_market(cards_left, market)

	def update_map(self, nr, dist):
		self.map_window.set_map(nr, dist)

	def update_stock(self, stock):
		if not stock:
			print 'uh'
			return
		self.stock.update_stock(*stock)
