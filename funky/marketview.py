import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from plantlist import PlantList

class MarketRow(Gtk.ListBoxRow):
	def __init__(self, bid_cb, pass_cb):
		def bid_shim(*args):
			sel = self.plants.get_selected()
			if not sel:
				return
			img, txt, idx = sel
			bid_cb(idx, self.c.get_value_as_int())
		def pass_shim(*args):
			pass_cb()
		super(MarketRow, self).__init__()

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		self.add(vbox)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)

		self.name = Gtk.Label(xalign = 0)
		self.name.set_markup('<b>Market</b>')

		hbox.pack_start(self.name, True, True, 5)
		vbox.pack_start(hbox, True, True, 5)

		self.plants = PlantList(indices = (-1 for x in xrange(8)))
		self.plants.set_columns(4)
		vbox.pack_start(self.plants, True, True, 5)

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

		self.c.connect('activate', bid_shim)
		b.connect('clicked', bid_shim)
		p.connect('clicked', pass_shim)

		vbox.pack_start(hbox, False, True, 5)
		self.set_can_focus(False)

	def update_plants(self, plants):
		self.plants.update(plants)

class MarketView(Gtk.ListBox):
	def __init__(self, bid_cb, pass_cb):
		super(MarketView, self).__init__()
		self.set_can_focus(False)
		self.set_selection_mode(Gtk.SelectionMode.NONE)

		self.market = MarketRow(bid_cb, pass_cb)
		self.insert(self.market, -1)

	def update_market(self, cards_left, market):
		self.market.plants.update(market)
