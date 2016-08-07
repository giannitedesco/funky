import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf

from os.path import join

base_dir = '/home/scara/Downloads/BrettspielWelt'

def load_plants(subdir):
	path = join(base_dir, subdir)
	fns = (
		'funkkart_03a.jpg', 'funkkart_04a.jpg',
		'funkkart_05a.jpg', 'funkkart_06a.jpg',
		'funkkart_07a.jpg', 'funkkart_08a.jpg',
		'funkkart_09a.jpg', 'funkkart_10a.jpg',
		'funkkart_11a.jpg', 'funkkart_12a.jpg',
		'funkkart_13a.jpg', 'funkkart_14a.jpg',
		'funkkart_15a.jpg', 'funkkart_16a.jpg',
		'funkkart_17a.jpg', 'funkkart_18a.jpg',
		'funkkart_19a.jpg', 'funkkart_20a.jpg',
		'funkkart_21a.jpg', 'funkkart_22a.jpg',
		'funkkart_23a.jpg', 'funkkart_24a.jpg',
		'funkkart_25a.jpg', 'funkkart_26a.jpg',
		'funkkart_27a.jpg', 'funkkart_28a.jpg',
		'funkkart_29a.jpg', 'funkkart_30a.jpg',
		'funkkart_31a.jpg', 'funkkart_32a.jpg',
		'funkkart_33a.jpg', 'funkkart_34a.jpg',
		'funkkart_35a.jpg', 'funkkart_36a.jpg',
		'funkkart_37a.jpg', 'funkkart_38a.jpg',
		'funkkart_39a.jpg', 'funkkart_40a.jpg',
		'funkkart_42a.jpg', 'funkkart_44a.jpg',
		'funkkart_46a.jpg', 'funkkart_50a.jpg',
		'stufe_3_a.jpg', 'blass.png', 'blocker.jpg'
	)

	out = []
	for fn in map(lambda x:join(path, x), fns):
		out.append(Pixbuf.new_from_file(fn))

	return tuple(out)

class PlantPixbufs(object):
	__map = None
	def __new__(cls, *args, **kwargs):
		if cls.__map is None:
			cls.__map = load_plants('funkenschlagPics/kw')
		return super(PlantPixbufs, cls).__new__(cls)
	def __getitem__(self, k):
		return self.__map[k]

