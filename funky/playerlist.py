import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from plantlist import PlantList

from collections import namedtuple

Player = namedtuple('Player', ('name', 'money', 'cities', 'plants'))

class PlayerRow(Gtk.ListBoxRow):
	def __init__(self, u):
		super(PlayerRow, self).__init__()

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		self.add(vbox)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)

		self.name = Gtk.Label(xalign = 0)

		self.money = Gtk.Label()

		self.cities = Gtk.Label()

		hbox.pack_start(self.name, True, True, 5)
		hbox.pack_start(self.cities, False, True, 5)
		hbox.pack_start(self.money, False, True, 5)
		vbox.pack_start(hbox, True, True, 5)

		self.plants = PlantList(selectable = False, show_text = True)
		vbox.pack_start(self.plants, True, True, 0)

		self.update(u)
	
	def update(self, u):
		self.update_name(u.name)
		self.update_cities(u.cities)
		self.update_money(u.money)
		self.update_plants(u.plants)

	def update_name(self, name):
		self.name.set_markup('<b>%s</b>'%name)
	def update_money(self, money):
		self.money.set_markup('<b>%d elektro</b>'%money)
	def update_cities(self, cities):
		self.cities.set_markup('<b>%d cities</b>'%cities)
	def update_plants(self, plants):
		self.plants.update(plants)
	def update_stock(self, stock):
		for i, s in enumerate(stock):
			self.plants.update_stock(i, *s)

class PlayerList(Gtk.ListBox):
	def __init__(self):
		super(PlayerList, self).__init__()
		self.set_can_focus(False)
		#self.set_sensitive(False)
		self.set_selection_mode(Gtk.SelectionMode.NONE)

	def update_plant_stock(self, prs):
		for i, pr in enumerate(prs):
			if not pr or pr == (-1, -1, -1, -1):
				continue
			r = self.get_row_at_index(i)
			if r is None:
				continue
			r.update_stock(pr)

	def update_player_names(self, nr, names):
		for i, n in enumerate(names[:nr]):
			if not n or n == ' ':
				n = '**'
			r = self.get_row_at_index(i)
			if r is None:
				u = Player(n, 50, 0, (-1, -1, -1, -1))
				r = PlayerRow(u)
				self.insert(PlayerRow(u), i)
			else:
				r.update_name(n)
		self.show_all()

	def update_player_plants(self, plants):
		for (i, p) in enumerate(plants):
			r = self.get_row_at_index(i)
			if r is None:
				if p == (-1, -1, -1, -1):
					continue
				u = Player('**', 50, 0, p)
				r = PlayerRow(u)
				self.insert(PlayerRow(u), i)
			else:
				r.update_plants(p)
		self.show_all()

	def update_player_money(self, money):
		for (i, m) in enumerate(money):
			r = self.get_row_at_index(i)
			if r is None:
				if m == 50:
					continue
				u = Player('**', m, 0, (-1, -1, -1, -1))
				r = PlayerRow(u)
				self.insert(PlayerRow(u), i)
			else:
				r.update_money(m)
		self.show_all()

	def update_player_cities(self, cities):
		for (i, (_, c)) in enumerate(cities):
			r = self.get_row_at_index(i)
			if r is None:
				if (_, c) == (0, 0):
					continue
				u = Player('**', 50, c, (-1, -1, -1, -1))
				r = PlayerRow(u)
				self.insert(PlayerRow(u), i)
			else:
				r.update_cities(c)
		self.show_all()
