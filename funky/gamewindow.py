import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Gio
from gi.repository.GdkPixbuf import Pixbuf

from art import PlantPixbufs

from collections import namedtuple

class PlantList(Gtk.IconView):
	def __init__(self, indices = None,
				show_text = False,
				selectable = True):
		super(PlantList, self).__init__()

		s = Gtk.ListStore(Pixbuf, str)

		self.set_model(s)
		self.set_pixbuf_column(0)
		if show_text:
			self.set_text_column(1)

		self.set_spacing(2)
		self.set_row_spacing(2)
		self.set_column_spacing(2)
		self.set_item_padding(2)
		self.set_item_width(40)

		if not selectable:
			self.set_selection_mode(Gtk.SelectionMode.NONE)

		self.update(indices)
	
	def update(self, indices = None):
		if not indices:
			return

		p = PlantPixbufs()
		s = self.get_model()

		s.clear()
		if indices:
			for i in indices:
				if i < 0:
					i = 43
				plant = p[i]
				s.append((plant, 'Card %d'%i))
		else:
			for i, plant in enumerate(p):
				s.append((plant, 'Card %d'%i))

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

		self.plants = PlantList(selectable = False)
		vbox.pack_start(self.plants, True, True, 0)

		self.update(u)
		self.u = u
	
	def update(self, u):
		self.update_name(u.name)
		self.update_cities(u.cities)
		self.update_money(u.money)
		self.update_plants(u.plants)

	def update_name(self, name):
		self.name.set_markup('<b>%s</b>'%name)
	def update_money(self, money):
		self.cities.set_markup('<b>%d elektro</b>'%money)
	def update_cities(self, cities):
		self.money.set_markup('<b>%d cities</b>'%cities)
	def update_plants(self, plants):
		self.plants.update(plants)

Player = namedtuple('Player', ('name', 'money', 'cities', 'plants'))

class PlayerList(Gtk.ListBox):
	def __init__(self):
		super(PlayerList, self).__init__()
		self.set_can_focus(False)
		#self.set_sensitive(False)
		self.set_selection_mode(Gtk.SelectionMode.NONE)

class GameWindow(Gtk.Box):
	def __init__(self):
		super(GameWindow, self).__init__(\
				orientation = Gtk.Orientation.HORIZONTAL,
				spacing = 6)

		self.player_list = PlayerList()
		uscr = Gtk.ScrolledWindow()
		uscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
		uscr.add(self.player_list)
		uscr.show_all()

		self.plant_list = PlantList()
		pscr = Gtk.ScrolledWindow()
		pscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		pscr.add(self.plant_list)

		self.pack_start(uscr, False, True, 0)
		self.pack_start(pscr, True, True, 0)

	def update_player_names(self, nr, names):
		for i, n in enumerate(names[:nr]):
			if not n or n == ' ':
				n = '**'
			r = self.player_list.get_row_at_index(i)
			if r is None:
				u = Player(n, 50, 0, (-1, -1, -1, -1))
				r = PlayerRow(u)
				self.player_list.insert(PlayerRow(u), i)
			else:
				r.update_name(n)

	def update_player_plants(self, plants):
		for (i, p) in enumerate(plants):
			r = self.player_list.get_row_at_index(i)
			if r is None:
				if p == (-1, -1, -1, -1):
					continue
				u = Player('**', 50, 0, p)
				r = PlayerRow(u)
				self.player_list.insert(PlayerRow(u), i)
			else:
				r.update_plants(p)

	def update_player_money(self, money):
		for (i, m) in enumerate(money):
			r = self.player_list.get_row_at_index(i)
			if r is None:
				if m == 50:
					continue
				u = Player('**', m, 0, (-1, -1, -1, -1))
				r = PlayerRow(u)
				self.player_list.insert(PlayerRow(u), i)
			else:
				r.update_money(m)

	def update_player_cities(self, cities):
		for (i, (_, c)) in enumerate(cities):
			r = self.player_list.get_row_at_index(i)
			if r is None:
				if (_, c) == (0, 0):
					continue
				u = Player('**', 50, c, (-1, -1, -1, -1))
				r = PlayerRow(u)
				self.player_list.insert(PlayerRow(u), i)
			else:
				r.update_cities(c)
