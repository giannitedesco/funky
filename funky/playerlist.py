import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from plantlist import PlantList

from collections import namedtuple

Player = namedtuple('Player', ('name', 'money', 'cap', 'cities', 'plants'))

class PlayerRow(Gtk.ListBoxRow):
	def __init__(self, u, prev = None):
		super(PlayerRow, self).__init__()

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
					spacing = 5)
		self.add(vbox)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)

		self.rb = Gtk.RadioButton.new_from_widget(prev)
		self.rb.set_sensitive(False)

		self.name = Gtk.Label(xalign = 0)

		self.money = Gtk.Label()

		self.cities = Gtk.Label()

		hbox.pack_start(self.rb, False, False, 5)
		hbox.pack_start(self.name, True, True, 5)
		hbox.pack_start(self.cities, False, True, 5)
		hbox.pack_start(self.money, False, True, 5)
		vbox.pack_start(hbox, True, True, 5)

		self.plants = PlantList(selectable = False, show_text = True)
		vbox.pack_start(self.plants, True, True, 0)

		self.update(u)

	def update(self, u):
		self.update_name(u.name)
		self.update_cities(u.cities, u.cap)
		self.update_money(u.money)
		self.update_plants(u.plants)

	def update_name(self, name):
		self.name.set_markup('<b>%s</b>'%name)
	def update_money(self, money):
		self.money.set_markup('<b>%d elektro</b>'%money)
	def update_cities(self, cities, cap):
		self.cities.set_markup('<b>%d/%d cities</b>'%(cap, cities))
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
		self.null = Gtk.RadioButton()
		self.prev = self.null

	def update_current_player(self, idx):
		r = self.get_row_at_index(idx)
		if r is None:
			self.null.set_active(True)
		else:
			r.rb.set_active(True)

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
				u = Player(n, 50, 0, 0, (-1, -1, -1, -1))
				r = PlayerRow(u, prev = self.prev)
				self.prev = r.rb
				self.insert(r, i)
			else:
				r.update_name(n)
		self.show_all()

	def update_player_plants(self, plants):
		for (i, p) in enumerate(plants):
			r = self.get_row_at_index(i)
			if r is None:
				if p == (-1, -1, -1, -1):
					continue
				raise Exception
			else:
				r.update_plants(p)
		self.show_all()

	def update_player_money(self, money):
		for (i, m) in enumerate(money):
			r = self.get_row_at_index(i)
			if r is None:
				if m == 50:
					continue
				raise Exception
			else:
				r.update_money(m)
		self.show_all()

	def update_player_cities(self, cities):
		for (i, (n, c)) in enumerate(cities):
			r = self.get_row_at_index(i)
			if r is None:
				if (n, c) == (0, 0):
					continue
				raise Exception
			else:
				r.update_cities(n, c)
		self.show_all()
