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
		def bid_cb(*_):
			sel = self.plants.get_selected()
			if not sel:
				return
			img, txt, idx = sel
			price = self.c.get_value_as_int()
			self.emit('bid', idx, price)
		def sel_cb(_):
			sel = self.plants.get_selected()
			if not sel:
				self.cur.update_plant(0, -1)
				return
			img, txt, idx = sel
			self.cur.update_plant(0, idx)

			# TODO: know start price
			#self.c.set_value()

		def pass_cb(_):
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
		self.plants.connect('selection-changed', sel_cb)
		self.pack_start(self.plants, True, True, 5)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)
		self.cur = PlantList(indices = [-1])
		hbox.pack_start(self.cur, False, True, 5)

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 0)
		self.p = Gtk.Label()
		self.c = Gtk.SpinButton()
		self.c.set_range(0, 10000)
		self.c.set_numeric(True)
		self.c.set_increments(1, 1)
		b = Gtk.Button.new_with_label("bid")
		p = Gtk.Button.new_with_label("pass")
		vbox.pack_start(self.p, False, True, 2)
		vbox.pack_start(self.c, False, True, 2)
		vbox.pack_start(b, False, True, 2)
		vbox.pack_start(p, False, True, 2)

		self.c.connect('activate', bid_cb)
		b.connect('clicked', bid_cb)
		p.connect('clicked', pass_cb)

		hbox.pack_start(vbox, True, True, 5)
		self.pack_start(hbox, False, True, 5)

		self.update_bid(-1, 0, -1)

	def update_market(self, cards_left, market):
		t = '<b>Power Plant Auction: %u plants left</b>'%cards_left
		self.title.set_markup(t)
		self.plants.update(market)

	def update_bid(self, plant, bid, player):
		if plant < 0 or player is None:
			self.p.set_markup('<b>Player</b>')
			self.c.set_value(1)
			self.cur.update_plant(0, -1)
			return
		self.p.set_markup('<b>Player: %s</b>'%player)
		self.c.set_value(bid)
		self.cur.update_plant(0, plant)
