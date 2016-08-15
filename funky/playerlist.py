import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk

from plantlist import PlantList
from funky.cards import cards

colors = (
	Gdk.RGBA(0.22265625, 0.234375, 0.6484375),
	Gdk.RGBA(0.58984375, 0.20703125, 0.54296875),
	Gdk.RGBA(0.71484375, 0.70703125, 0.23828125),
	Gdk.RGBA(0.6171875, 0.171875, 0.19921875),
	Gdk.RGBA(0.34765625, 0.48046875, 0.42578125),
	Gdk.RGBA(0.60546875, 0.4609375, 0.2265625),
)

class PlayerRow(Gtk.ListBoxRow):
	def __init__(self, p, prev = None):
		super(PlayerRow, self).__init__()

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		self.add(vbox)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)

		self.rb = Gtk.RadioButton.new_from_widget(prev)
		self.rb.set_sensitive(False)

		self.col = Gtk.ColorButton.new_with_rgba(colors[p.seat_nr])
		self.col.set_sensitive(False)
		self.col.props.title = 'hi'

		self.name = Gtk.Label(xalign = 0)

		self.m = Gtk.Label()

		self.cities = Gtk.Label()

		hbox.pack_start(self.rb, False, False, 0)
		hbox.pack_start(self.col, False, False, 0)
		hbox.pack_start(self.name, True, True, 5)
		hbox.pack_start(self.cities, False, True, 5)
		hbox.pack_start(self.m, False, True, 5)
		vbox.pack_start(hbox, True, True, 5)

		self.plants = PlantList(selectable = False, show_text = True)
		vbox.pack_start(self.plants, True, True, 0)

		self.show_money = True
		self.update_name(p.name)
		self.update_cities(p.nr_cities, p.capacity)
		self.update_money(p.money)
		self.update_plants(p.plants)
		self.update_stock(p.stock)

		self.seat_nr = p.seat_nr

	def update_name(self, name):
		self.name.set_markup('<b>%s</b>'%name)
	def update_money(self, money):
		self.money = money
		if self.show_money:
			self.m.set_markup('<b>%d</b>'%self.money)
		else:
			self.m.set_markup('<b>??</b>')
	def set_show_money(self, show_money):
		self.show_money = show_money
		self.update_money(self.money)
	def update_cities(self, cities, cap):
		self.cities.set_markup('<b>%d/%d</b>'%(cap, cities))
	def update_plants(self, plants):
		self.plants.set_plants(((x, None) for x in plants))
	def update_stock(self, stk):
		for i, (stock,cap) in enumerate(stk):
			stock = (stock >> 10) + (stock & 0x3ff)
			text = '%d/%d'%(stock, cap)
			self.plants.update_text(i, text)

class PlayerList(Gtk.ListBox):
	def get_row_for_seat_nr(self, index):
		if self.rf:
			index = self.rf[index]
		return self.get_row_at_index(index)
	def __init__(self, game):
		def update_cb(game, p):
			r = self.get_row_for_seat_nr(p.seat_nr)
			r.update_money(p.money)
			r.update_name(p.name)
			r.update_cities(p.nr_cities, p.capacity)
			r.update_plants(p.plants)
			r.update_stock(p.stock)

		def join_cb(game, p):
			r = PlayerRow(p, prev = self.prev)
			self.prev = r.rb
			self.insert(r, -1)
			self.show_all()

		def leave_cb(game, p):
			r = self.get_row_for_seat_nr(p.seat_nr)
			self.remove(r)

		def current_player_cb(game, cp, iam):
			if cp < 0:
				self.null.set_active(True)
				return

			r = self.get_row_for_seat_nr(cp)
			r.rb.set_active(True)

		def seq_cb(game, seq):
			self.mf = dict(enumerate(seq[:self.game.nr_players]))
			self.rf = dict(map(lambda x:reversed(x),
				enumerate(seq[:self.game.nr_players])))
			self.invalidate_sort()

		def i_am_cb(game, i_am):
			for idx in xrange(self.game.nr_players):
				r = self.get_row_for_seat_nr(idx)
				r.set_show_money(idx == i_am)

		def sort_cb(a, b):
			if not self.rf:
				return cmp(a.seat_nr, b.seat_nr)
			return cmp(self.rf[a.seat_nr], self.rf[b.seat_nr])

		super(PlayerList, self).__init__()
		self.game = game

		self.set_can_focus(False)
		self.set_selection_mode(Gtk.SelectionMode.NONE)
		self.null = Gtk.RadioButton()
		self.prev = self.null
		self.mf = None
		self.rf = None

		self.game.connect('update_current_player', current_player_cb)
		self.game.connect('player_join', join_cb)
		self.game.connect('player_update', update_cb)
		self.game.connect('player_leave', leave_cb)
		self.game.connect('update_player_sequence', seq_cb)
		self.game.connect('update_i_am', i_am_cb)

		self.set_sort_func(sort_cb)
