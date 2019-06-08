import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Gdk, GObject
from gi.repository.GdkPixbuf import Pixbuf

from .art import ResourcePixbufs

atom = Gdk.Atom.intern('funk-rs', False)
RL = GObject.SIGNAL_RUN_LAST

class ResourceList(Gtk.IconView):
    __gsignals__ = {
        'rs-move': (RL, None, (int,int,int)),
    }
    def __init__(self, ident, resources = (),
                selectable = True):

        def d_send(self, dctx, data, info, time):
            sel = self.get_selected_items()
            if not sel:
                return None
            rsidx = sel[0][0]
            data.set(atom, 8, '%d,%d,\0'%(self.ident, rsidx))
            self.to_delete = rsidx
        def d_recv(self, dctx, x,y, data,info, time):
            src, rtype, _ = data.get_data().split(',', 2)
            self.emit('rs-move', int(src), self.ident, int(rtype))

        super(ResourceList, self).__init__()

        self.ident = ident

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

        act = Gdk.DragAction.COPY

        t = Gtk.TargetEntry()
        t.target = 'funk-rs'
        t.flags = Gtk.TargetFlags.SAME_APP | Gtk.TargetFlags.OTHER_WIDGET
        t.info = 666
        tgt = (t,)
        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, tgt, act)
        self.drag_dest_set(Gtk.DestDefaults.ALL, tgt, act)
        #self.drag_dest_set_target_list(tgt)
        #self.drag_source_set_target_list(tgt)

        self.connect('drag-data-get', d_send)
        self.connect('drag-data-received', d_recv)

        self.set_resources(resources)
        self.set_size_request(16 * 3, 16 * 2)

    def __row(self, rs):
        pix = ResourcePixbufs()
        img = pix[rs]
        return (rs, img)

    def set_resources(self, resources = ()):
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
