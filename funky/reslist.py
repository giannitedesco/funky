import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from art import ResourcePixbufs

class ResourceList(Gtk.IconView):
	def __init__(self, resources = (),
				selectable = True):
		super(ResourceList, self).__init__()

		s = Gtk.ListStore(int, Pixbuf)

		self.set_model(s)
		self.set_pixbuf_column(1)

		self.set_spacing(0)
		self.set_row_spacing(0)
		self.set_column_spacing(0)
		self.set_item_padding(0)
		self.set_item_width(10)

		if not selectable:
			self.set_selection_mode(Gtk.SelectionMode.NONE)

		self.set_resources(resources)

	def __row(self, rs):
		pix = ResourcePixbufs()
		img = pix[rs]
		return (rs, img)

	def set_resources(self, resources = ()):
		if not resources:
			return

		s = self.get_model()

		s.clear()
		for rs in resources:
			s.append(self.__row(rs))

	def get_selected(self):
		sel = self.get_selected_items()
		if not sel:
			return None
		path = sel[0]
		model = self.get_model()
		row = model[path]
		return (row[0], row[1])
	
	def update_item(self, idx, rs):
		s = self.get_model()
		it = s.get_iter((idx,))
		r = self.__row(rs)
		s.set(it, 0, r[0], 1, r[1])
