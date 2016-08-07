import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList
from playerlist import PlayerList
from marketview import MarketView

class GameWindow(Gtk.Box):
	__gsignals__ = {
		'bid':
			(GObject.SIGNAL_RUN_LAST, None, (int, int)),
		'pass':
			(GObject.SIGNAL_RUN_LAST, None, ()),
	}
	def __init__(self):
		def bid_cb(index, price):
			self.emit('bid', index, price)
		def pass_cb():
			self.emit('pass')
		super(GameWindow, self).__init__(\
				orientation = Gtk.Orientation.HORIZONTAL,
				spacing = 6)

		self.player_list = PlayerList()
		self.market = MarketView(bid_cb, pass_cb)
		self.map_window = PlantList()

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		vbox.pack_start(self.player_list, True, True, 0)
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
