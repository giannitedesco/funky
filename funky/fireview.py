import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList
from funky.cards import cards

class FireBox(Gtk.Box):
	def __init__(self, plant_index, dcb):
		super(FireBox, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 0)
		self.plant_index = plant_index

		self.p = PlantList(((None, None),),
					show_text = True,
					selectable = False)
		self.d = Gtk.Button.new_with_label('Demolish')
		self.f = Gtk.ToggleButton.new_with_label('Fire')

		self.d.connect('clicked', lambda x:(dcb(self.plant_index)))

		self.p.set_margin(0)

		self.pack_start(self.p, False, True, 0)
		self.pack_start(self.d, False, True, 0)
		self.pack_start(self.f, False, True, 0)

	def get_mask(self):
		if self.f.props.active:
			return 7
		else:
			return 0


class FireView(Gtk.Box):
	def __init__(self, game):
		def fcb(*_):
			self.game.fire(*[x.get_mask() for x in self.p])

		def dcb(plant_index):
			self.game.demolish(plant_index)

		def plant_stock_cb(_, prs):
			if self.game.i_am < 0:
				return
			self.update_stock(prs[self.game.i_am])
		def plants_cb(_, plants):
			if self.game.i_am < 0:
				return
			self.update_plants(plants[self.game.i_am])

		super(FireView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)
		self.game = game

		name = Gtk.Label(xalign = 0)
		name.set_markup('<b>Fire Plants</b>')
		done = Gtk.Button.new_with_label('Fire Plants')
		done.connect('clicked', fcb)

		nhb = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)
		nhb.pack_start(name, True, True, 5)

		self.p = tuple([FireBox(i, dcb) for i in xrange(4)])

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
				spacing = 5)
		for x in self.p:
			hbox.pack_start(x, True, True, 0)

		self.pack_start(nhb, False, True, 5)
		self.pack_start(hbox, True, True, 5)
		self.pack_start(done, False, True, 5)

		self.game.connect('update_plants', plants_cb)
		self.game.connect('update_plant_stock', plant_stock_cb)

	def update_stock(self, stk):
		for i, (stock, cap) in enumerate(stk):
			stock = (stock >> 10) + (stock & 0x3ff)
			text = '%d/%d'%(stock, cap)
			self.p[i].p.update_text(0, text)
	def update_plants(self, plants):
		for i, p in enumerate(plants):
			self.p[i].p.update_item(0, cards[p], None)
