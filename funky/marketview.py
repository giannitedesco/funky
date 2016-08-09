import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList

class MarketView(Gtk.Box):
	__gsignals__ = {
		'bid':
			(GObject.SIGNAL_RUN_LAST, None, (int, int)),
		'pass':
			(GObject.SIGNAL_RUN_LAST, None, ()),
	}
	def __init__(self):
		def bid_cb(idx, price):
			sel = self.plants.get_selected()
			if not sel:
				return
			img, txt, idx = sel
			price = self.c.get_value_as_int()
			self.emit('bid', idx, price)
		def pass_cb():
			self.emit('pass')
		super(MarketView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)

		self.title = Gtk.Label(xalign = 0)
		self.title.set_markup('<b>Power Plant Auction</b>')

		hbox.pack_start(self.title, True, True, 5)
		self.pack_start(hbox, True, True, 5)

		self.plants = PlantList(indices = (-1 for x in xrange(8)))
		self.plants.set_columns(4)
		self.pack_start(self.plants, True, True, 5)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)
		self.c = Gtk.SpinButton()
		self.c.set_range(0, 10000)
		self.c.set_numeric(True)
		self.c.set_value(1)
		self.c.set_increments(1, 1)
		b = Gtk.Button.new_with_label("bid")
		p = Gtk.Button.new_with_label("pass")
		hbox.pack_start(self.c, True, True, 5)
		hbox.pack_start(b, True, True, 5)
		hbox.pack_start(p, True, True, 5)

		self.c.connect('activate', bid_cb)
		b.connect('clicked', bid_cb)
		p.connect('clicked', pass_cb)

		self.pack_start(hbox, False, True, 5)

	def update_market(self, cards_left, market):
		t = '<b>Power Plant Auction: %u plants left</b>'%cards_left
		self.title.set_markup(t)
		self.plants.update(market)

	def update_bid(self, plant, bid, player):
		if plant < 0 or player is None:
			# clear bid
			return
		print plant, bid, player
