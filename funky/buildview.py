import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class BuildView(Gtk.Box):
	def __init__(self, game):
		def dcb(*_):
			self.game.finish_building()

		super(BuildView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)

		self.game = game

		name = Gtk.Label(xalign = 0)
		name.set_markup('<b>Build Cities</b>')
		done = Gtk.Button.new_with_label("Done")
		done.connect('clicked', dcb)
		self.pack_start(name, False, True, 5)
		self.pack_start(Gtk.Label('TODO: preview'), True, True, 5)
		self.pack_start(done, False, True, 5)
