import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList
from funky.cards import cards

class MarketView(Gtk.Box):
	def __init__(self, game):
		def bid_cb(*_):
			sel = self.plants.get_selected()
			if not sel:
				return
			card, text = sel
			price = self.c.get_value_as_int()
			self.game.bid(card.idx, price)
		def pass_cb(_):
			self.game.bid(-1, -1)

		def sel_cb(_):
			sel = self.plants.get_selected()
			if not sel:
				self.cur.update_item(0, None, None)
				self.c.set_range(0, 10000)
				return
			card, text = sel
			self.cur.update_item(0, card, None)
			self.c.set_range(card.price, 10000)
			self.c.set_value(card.price)

		def market_cb(_, cards_left, market):
			self.update_market(cards_left, market)
		def cur_bid_cb(_, card, bid, player):
			if player < 0:
				p = None
			else:
				p = self.game.players[player]
			self.update_bid(card, bid, p)

		super(MarketView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)

		self.game = game

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)

		self.title = Gtk.Label(xalign = 0)
		self.title.set_markup('<b>Power Plant Auction</b>')

		hbox.pack_start(self.title, True, True, 5)
		self.pack_start(hbox, True, True, 5)

		self.plants = PlantList(((None, None) for x in xrange(8)))
		self.plants.set_columns(4)
		self.plants.connect('selection-changed', sel_cb)
		self.pack_start(self.plants, True, True, 5)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)
		self.cur = PlantList(((None, None),), selectable = False)
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

		self.game.connect('update_market', market_cb)
		self.game.connect('update_bid', cur_bid_cb)

	def update_market(self, cards_left, market):
		t = '<b>Power Plant Auction: %u plants left</b>'%cards_left
		self.title.set_markup(t)
		m = ((cards[i], None) for i in market)
		self.plants.set_plants(m)

	def update_bid(self, plant, bid, player):
		if plant < 0 or player is None:
			self.p.set_markup('<b>Player</b>')
			self.c.set_value(1)
			self.cur.update_item(0, None, None)
			return
		self.p.set_markup('<b>Player: %s</b>'%player)
		self.c.set_value(bid)
		self.cur.update_item(0, cards[plant], None)
