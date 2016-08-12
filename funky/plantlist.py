import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from art import PlantPixbufs

class PlantList(Gtk.IconView):
	def __init__(self, plants = (),
				show_text = False,
				selectable = True):
		super(PlantList, self).__init__()

		s = Gtk.ListStore(object, Pixbuf, str)

		self.set_model(s)
		self.set_pixbuf_column(1)
		if show_text:
			self.set_text_column(2)

		self.set_spacing(2)
		self.set_row_spacing(2)
		self.set_column_spacing(2)
		self.set_item_padding(2)
		self.set_item_width(40)

		if not selectable:
			self.set_selection_mode(Gtk.SelectionMode.NONE)

		self.set_plants(plants)

	def __row(self, card, text):
		pix = PlantPixbufs()
		if card:
			img = pix[card.idx]
		else:
			img = pix[43]
		return (card, img, text)

	def set_plants(self, plants = ()):
		if not plants:
			return

		s = self.get_model()

		s.clear()
		for (card, text) in plants:
			s.append(self.__row(card, text))

	def get_selected(self):
		sel = self.get_selected_items()
		if not sel:
			return None
		path = sel[0]
		model = self.get_model()
		row = model[path]
		return (row[0], row[2])
	
	def update_item(self, idx, card, text):
		s = self.get_model()
		it = s.get_iter((idx,))
		r = self.__row(card, text)
		s.set(it, 0, r[0], 1, r[1], 2, r[2])

	def update_text(self, idx, text):
		s = self.get_model()
		it = s.get_iter((idx,))
		s.set_value(it, 2, text)
