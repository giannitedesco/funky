import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList
from reslist import ResourceList

from cards import PlantType

class FireBox(Gtk.Box):
	def __init__(self, plant_index, dcb):
		super(FireBox, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 0)
		self.plant_index = plant_index

		self.p = PlantList(((None, None),),
					show_text = True,
					selectable = False)
		self.p.set_margin(0)

		self.d = Gtk.Button.new_with_label('Demolish')
		self.f = Gtk.ToggleButton.new_with_label('Fire')

		self.d.connect('clicked', lambda x:(dcb(self.plant_index)))

		self.r = ResourceList((), selectable = True)
		self.r.set_columns(3)
		self.r.set_margin(0)

		self.pack_start(self.p, False, True, 0)
		self.pack_start(self.d, False, True, 0)
		self.pack_start(self.f, False, True, 0)
		self.pack_start(self.r, False, True, 0)

		self.plant = 0

	def get_mask(self):
		if self.f.props.active and self.plant:
			return (1 << self.plant.resources) - 1
		else:
			return 0


class FireView(Gtk.Box):
	def __init__(self, game):
		def fcb(*_):
			self.game.fire(*[x.get_mask() for x in self.p])

		def dcb(plant_index):
			self.game.demolish(plant_index)

		def update_cb(game, p):
			self.update_plants(p.plants)
			self.update_stock(p.stock)

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

		self.game.connect('update_self', update_cb)

	def update_stock(self, stk):
		for i, (stock, cap) in enumerate(stk):
			stock = (stock >> 10) + (stock & 0x3ff)
			text = '%d/%d'%(stock, cap)
			self.p[i].p.update_text(0, text)

			if not self.p[i].plant:
				self.p[i].r.set_resources(())
				return

			rtmap = {
				PlantType.green: (),
				PlantType.coal: (0,),
				PlantType.oil: (1,),
				PlantType.hybrid: (1,0), # flipped?
				PlantType.trash: (2,),
				PlantType.nuclear: (3,),
			}

			rc = (stock & 0x3ff, stock >> 10)
			out = list()
			for ci, x in enumerate(rtmap[self.p[i].plant.type]):
				out += [x for _ in xrange(rc[ci])]
			#print rc, self.p[i].plant.type, out

			self.p[i].r.set_resources(out)

	def update_plants(self, plants):
		for i, p in enumerate(plants):
			self.p[i].plant = p
			self.p[i].p.update_item(0, p, None)
