import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class ResourceRow(Gtk.ListBoxRow):
	def __init__(self, name, count):
		super(ResourceRow, self).__init__()

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 5)

		self.name = Gtk.Label(xalign = 0)
		self.name.set_markup('<b>%s</b>'%name)


		self.c = Gtk.SpinButton()
		self.c.set_numeric(True)
		self.c.set_increments(1, 1)
		self.c.set_editable(False)
		self.c.set_can_focus(False)

		self.p = Gtk.SpinButton()
		self.p.set_numeric(True)
		self.p.set_increments(1, 1)
		self.p.set_can_focus(False)
		self.p.set_value(0)

		hbox.pack_start(self.name, True, True, 5)
		hbox.pack_start(self.c, False, True, 5)
		hbox.pack_start(self.p, False, True, 5)
		self.add(hbox)

		self.set_can_focus(False)

		self.update_count(count)

	def update_count(self, count):
		self.c.set_range(count, count)
		self.c.set_value(count)
		self.p.set_range(0, count)
	def __int__(self):
		return self.p.get_value_as_int()

class ButtonRow(Gtk.ListBoxRow):
	def __init__(self, buy_cb):
		def cb_shim(*_):
			buy_cb(*self.totals)
		super(ButtonRow, self).__init__()

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 5)

		self.name = Gtk.Label(xalign = 0)
		self.name.set_markup('<b>Purchase</b>')

		self.d = Gtk.Label()#xalign = 0)
		self.update_totals(0, 0, 0, 0)

		b = Gtk.Button.new_with_label('buy')
		b.connect('clicked', cb_shim)

		hbox.pack_start(self.name, True, True, 0)
		hbox.pack_start(self.d, False, True, 0)
		hbox.pack_start(b, False, True, 0)
		self.add(hbox)

		self.set_can_focus(False)

	def update_totals(self, k, o, m, ke):
		self.totals = (k, o, m, ke)
		self.d.set_markup('%d coal, %d oil, %d trash, %d nuclear'%\
				(k, o, m, ke))

class ResourceView(Gtk.ListBox):
	__gsignals__ = {
		'buy':
			(GObject.SIGNAL_RUN_LAST, None, (int, int, int, int)),
	}
	def __init__(self):
		def buy_cb(k, o, m, ke):
			self.emit('buy', k, o, m, ke)
		def cb(*_):
			self.buttons.update_totals(*map(int, (self.coal,
								self.oil,
								self.trash,
								self.nuclear)))
		super(ResourceView, self).__init__()
		self.set_can_focus(False)
		self.set_selection_mode(Gtk.SelectionMode.NONE)

		name_row = Gtk.ListBoxRow()
		name = Gtk.Label(xalign = 0)
		name.set_markup('<b>Resources Market</b>')
		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 5)
		hbox.pack_start(name, True, True, 5)
		name_row.add(hbox)

		self.coal = ResourceRow('Coal', 0)
		self.oil = ResourceRow('Oil', 0)
		self.trash = ResourceRow('Trash', 0)
		self.nuclear = ResourceRow('Nuclear', 0)
		self.buttons = ButtonRow(buy_cb)

		self.coal.p.connect('changed', cb)
		self.oil.p.connect('changed', cb)
		self.trash.p.connect('changed', cb)
		self.nuclear.p.connect('changed', cb)

		self.insert(name_row, -1)
		self.insert(self.coal, -1)
		self.insert(self.oil, -1)
		self.insert(self.trash, -1)
		self.insert(self.nuclear, -1)
		self.insert(self.buttons, -1)

	def update_stock(self, k, o, m, ke):
		self.coal.update_count(k)
		self.oil.update_count(o)
		self.trash.update_count(m)
		self.nuclear.update_count(ke)
