import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango

class CmdEntry(Gtk.Entry):
	__gsignals__ = {
		'send': (GObject.SIGNAL_RUN_LAST, None, (str, )),
	}
	def send(self, s):
		self.emit('send', s)

	def __activate(self, _):
		s = self.get_text()
		self.set_text('')
		if len(s):
			self.send(s)

	def __init__(self):
		super(CmdEntry, self).__init__()
		self.connect('activate', self.__activate)

class ServerWindow(Gtk.Box):
	__gsignals__ = {
		'server_cmd': (GObject.SIGNAL_RUN_LAST, None, (str, )),
	}
	def __setup_tags(self, buf):
		tag = buf.create_tag('font')
		tag.set_property('font', 'Lucida Console 8')

		tag = buf.create_tag('bold')
		tag.set_property('weight', Pango.Weight.BOLD)

		for x in ['red', 'blue', 'green',
				'cyan', 'magenta', 'yellow',
				'purple', 'black',
				'dark blue', 'dark green']:
			tag = buf.create_tag(x)
			tag.set_property('foreground', x)
			tag.set_property('foreground-set', True)

	def __cb(self, _, s):
		self.emit('server_cmd', s)

	def __init__(self):
		super(ServerWindow, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 6)

		self.entry = CmdEntry()
		self.entry.connect('send', self.__cb)

		self.text = Gtk.TextView()
		self.text.set_editable(False)
		self.text.set_cursor_visible(False)
		self.text.set_wrap_mode(Gtk.WrapMode.WORD)
		self.__setup_tags(self.text.get_buffer())
		scr = Gtk.ScrolledWindow()
		scr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scr.add(self.text)

		scr.set_can_focus(False)
		self.text.set_can_focus(False)

		self.pack_start(scr, True, True, 0)
		self.pack_start(self.entry, False, True, 0)

	def msg(self, msg, tags = []):
		tags.append('font')
		buf = self.text.get_buffer()
		i = buf.get_iter_at_offset(buf.get_char_count())
		buf.place_cursor(i)
		buf.insert_with_tags_by_name(i, msg, *tags)
		i = buf.get_iter_at_offset(buf.get_char_count())
		buf.place_cursor(i)

		if not '\n' in msg:
			return

		mark = buf.create_mark(None, i, left_gravity = True)
		self.text.scroll_to_mark(mark, 0.0, False, 0.0, 0.0)

	def log(self, s):
		self.msg('<<< ' + s + '\n')

	def chat_msg(self, s):
		self.msg('<<< ' + s + '\n', ['bold'])

	def rx_msg(self, msg):
		self.msg('<<< ' + str(msg) + '\n', ['dark green'])

	def tx_msg(self, msg):
		self.msg('>>> ' + str(msg) + '\n', ['purple'])
		return

