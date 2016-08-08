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
				s.append((plant, 'Card %d'%i, i))
		else:
			for i, plant in enumerate(p):
				s.append((plant, 'Card %d'%i, i))
