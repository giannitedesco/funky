import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gtk, Gdk, GObject

import cairo
from math import sqrt

from art import load_map, load_houses

def surf(p):
	return Gdk.cairo_surface_create_from_pixbuf(p, 1, None)

cxy = (
	(
		(896, 614), (64, 36), (34, 104), (176, 160), (340, 112),
		(404, 214), (394, 268), (568, 230), (36, 314), (104, 404),
		(150, 454), (192, 350), (262, 250), (260, 430), (372, 374),
		(552, 88), (636, 68), (622, 128), (718, 216), (682, 298),
		(802, 282), (806, 358), (588, 292), (550, 378), (680, 384),
		(564, 444), (572, 512), (682, 510), (746, 426), (810, 196),
		(920, 178), (892, 248), (1064, 178), (1022, 220), (996, 262),
		(942, 294), (980, 338), (928, 372), (810, 424), (876, 444),
		(872, 498), (832, 562)
	),

	(
		(479, 930), (300, 25), (341, 93), (337, 195), (245, 153),
		(259, 258), (190, 195), (338, 358), (401, 137),(455, 200),
		(503, 113), (656, 194), (604, 334), (688, 359),(485, 366),
		(197, 343), (152, 405), (95, 453), (45, 434), (165, 483),
		(298, 498), (58, 512), (499, 469), (656, 542), (544, 500),
		(440, 540), (337, 597), (350, 703), (440, 743), (248, 642),
		(199, 665), (111, 562), (34, 585), (66, 706), (136, 782),
		(241, 761), (266, 845), (173, 928), (266, 972), (398, 874),
		(505, 808), (626, 863),
	),

	(
		(348, 175), (407, 202), (458, 209), (426, 252), (400, 317),
		(329, 368), (352, 487), (459, 491), (385, 42), (468, 64),
		(410, 128), (529, 188), (645, 187), (725, 244), (644, 257),
		(709, 321), (646, 375), (573, 358), (577, 480), (690, 477),
		(628, 555), (531, 539), (530, 641), (609, 673), (711, 670),
		(640, 730), (571, 712), (483, 687), (454, 770), (415, 719),
		(364, 673), (274, 728), (189, 684), (244, 576), (215, 459),
		(182, 375), (27, 267), (181, 292), (253, 355), (297, 295),
		(242, 212), (279, 153)
	),

	(
		(94, 1016), (327, 25), (324, 148), (428, 92), (509, 93),
		(426, 148), (520, 149), (532, 196), (603, 200), (588, 242),
		(627, 286), (614, 313), (712, 325), (686, 376), (676, 164),
		(333, 212), (447, 191), (432, 230), (341, 270), (454, 267),
		(526, 300), (445, 317), (530, 370), (511, 424), (508, 513),
		(408, 474), (443, 422), (377, 352), (327, 298), (315, 547),
		(452, 610), (456, 745), (321, 713), (324, 764), (495, 839),
		(521, 918), (433, 905), (306, 926), (204, 984), (188, 944),
		(99, 842), (103, 976)
	),

	(
		(849, 253), (623, 102), (647, 320), (508, 305), (419, 262),
		(372, 205), (320, 145), (260, 168), (290, 350), (227, 415),
		(363, 408), (250, 486), (176, 562), (130, 638), (87, 518),
		(127, 753), (303, 796), (395, 763), (397, 874), (225, 913),
		(85, 905), (34, 964), (496, 914), (589, 920), (625, 847),
		(667, 729), (507, 743), (709, 597), (849, 605), (506, 573),
		(436, 493), (507, 463), (503, 385), (637, 473), (754, 376)
	),
)

def draw(self, cr):
	if not self.surf:
		return

	cr.set_source_surface(self.surf)
	cr.rectangle(0, 0, self.surf.get_width(), self.surf.get_height())
	cr.fill()

	#cr.set_source_rgba(1.0, 0.0, 0.0, 0.3)
	#cr.set_line_width(2)
	#for (x, y) in self.cxy:
	#	cr.arc(x, y, 24, 0, 2*3.141)
	#	cr.stroke()

	for ce in self.cities:
		h, idx = (ce[:3], ce[3])
		x,y = self.cxy[idx]
		if idx in self.clouds:
			t = self.houses[7]
			cr.save()
			cr.translate(x - 38, y - 30)
			cr.set_source_surface(t)
			cr.rectangle(0, 0, t.get_width(), t.get_height())
			cr.fill()
			cr.restore()
			continue
		for i, o in enumerate(h):
			if o < 0 or o >= 6:
				break

			t = self.houses[o]
			xx = x - 11 + (0, -10, 10)[i]
			yy = y - 18 - (10, -10, -10)[i]
			cr.save()
			cr.translate(xx, yy)
			cr.set_source_surface(t)
			cr.rectangle(0, 0, t.get_width(), t.get_height())
			cr.fill()
			cr.restore()

def click(self, evt):
	if evt.button != 1:
		return
	if not self.cxy:
		return

	for (i, (x,y)) in enumerate(self.cxy):
		xd = x - evt.x
		yd = y - evt.y
		d = sqrt(xd * xd + yd * yd)
		if d < 25:
			self.game.build(0, i)
			break

class MapView(Gtk.DrawingArea):
	def __init__(self, game):
		def map_cb(_, nr, dists):
			self.set_map(nr, dists)
		def cities_cb(_, cities):
			self.update_cities(cities)
		def city_active_cb(_, city_active):
			self.update_city_active(city_active)

		super(MapView, self).__init__()
		self.game = game
		self.cities = None
		self.houses = None

		self.clear_map()
		self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK
				|Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect('draw', draw)
		self.connect('button-release-event', click)
		self.set_can_focus(False)

		self.game.connect('update_map', map_cb)
		self.game.connect('update_cities', cities_cb)
		self.game.connect('update_city_active', city_active_cb)

	def clear_map(self):
		self.surf = None
		return

	def set_map(self, nr, dist):
		if not dist or nr < 0:
			self.clear_map()
			return

		if not self.houses:
			self.houses = tuple(map(surf, load_houses()))

		p = load_map(nr)
		self.surf = surf(p)
		self.cxy = cxy[nr]

	def update_cities(self, cities):
		self.cities = cities
		self.queue_draw()

	def update_city_active(self, city_active):
		g = (i for (i,x) in
			filter(lambda (i,x):not x, enumerate(city_active)))
		self.clouds = frozenset(g)
		self.queue_draw()
