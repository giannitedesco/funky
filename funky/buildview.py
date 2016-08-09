import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class BuildView(Gtk.Box):
	__gsignals__ = {
		'finished-building':
			(GObject.SIGNAL_RUN_LAST, None, ()),
	}
	def __init__(self):
		def dcb(*_):
			self.emit('finished-building')

		super(BuildView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)

		name = Gtk.Label(xalign = 0)
		name.set_markup('<b>Build Cities</b>')
		done = Gtk.Button.new_with_label("Done")
		done.connect('clicked', dcb)
		self.pack_start(name, False, True, 5)
		self.pack_start(Gtk.Label('TODO: preview'), True, True, 5)
		self.pack_start(done, False, True, 5)

