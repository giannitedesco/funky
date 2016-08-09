import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from art import PlantPixbufs

class PlantList(Gtk.IconView):
	def __init__(self, indices = None,
				show_text = False,
				selectable = True):
		super(PlantList, self).__init__()

		s = Gtk.ListStore(Pixbuf, str, int)

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

	def get_selected(self):
		sel = self.get_selected_items()
		if not sel:
			return None
		path = sel[0]
		model = self.get_model()
		row = model[path]
		return (row[0], row[1], row[2])
	
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
				s.append((plant, None, i))
		else:
			for i, plant in enumerate(p):
				s.append((plant, None, i))

	def update_plant(self, idx, plant):
		if plant < 0:
			plant = 43
		s = self.get_model()
		p = PlantPixbufs()[plant]
		s.set_value(s.get_iter((idx,)), 0, p)

	def update_stock(self, idx, stock, cap):
		# for hybrid plants
		stock = (stock >> 10) + (stock & 0x3ff)
		s = self.get_model()
		text = '%d/%d'%(stock, cap)
		s.set_value(s.get_iter((idx,)), 1, text)
