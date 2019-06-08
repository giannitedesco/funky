import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from .plantlist import PlantList
from .playerlist import PlayerList
from .marketview import MarketView
from .resourceview import ResourceView
from .buildview import BuildView
from .mapview import MapView
from .fireview import FireView
from .funkgame import FunkGame

class GameWindow(Gtk.Box):
    def __init__(self):
        # Callbacks for game events
        def ps_cb(_, p, s):
            n = ('auction',
                'auction',
                'rs',
                'build',
                'fire',
                None,
                None,
                None,
                None,
                None,
                'fire',
                None)
            self.stack.set_visible_child_name(n[p])

        super(GameWindow, self).__init__(\
                orientation = Gtk.Orientation.HORIZONTAL,
                spacing = 6)

        # Game object
        self.game = FunkGame()
        self.game.connect('update_ps', ps_cb)

        # Child windows
        self.player_list = PlayerList(self.game)
        self.map_win = MapView(self.game)
        self.rs = ResourceView(self.game)
        self.market = MarketView(self.game)
        self.build_win = BuildView(self.game)
        self.fire_win = FireView(self.game)

        self.stack = stack = Gtk.Stack()
        stack.set_transition_type(\
                Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(250)

        stack.add_titled(self.market,
                'auction',
                'Auction Power Plants')
        stack.child_set_property(self.market,
                    'icon-name',
                    'gnome-power-manager-symbolic')

        stack.add_titled(self.rs,
                'rs',
                'Resources')
        stack.child_set_property(self.rs,
                    'icon-name',
                    'preferences-color-symbolic')

        stack.add_titled(self.build_win,
                'build',
                'Build Connections')
        stack.child_set_property(self.build_win,
                    'icon-name',
                    'preferences-system-sharing-symbolic')

        stack.add_titled(self.fire_win,
                'fire',
                'Fire Plants')
        stack.child_set_property(self.fire_win,
                    'icon-name',
                    'goa-panel-symbolic')

        ss = Gtk.StackSwitcher()
        ss.set_stack(stack)
        ss.set_halign(Gtk.Align.CENTER)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                    spacing = 5)
        vbox.pack_start(self.player_list, True, True, 0)
        vbox.pack_start(ss, False, True, 0)
        vbox.pack_start(stack, False, True, 0)

        uscr = Gtk.ScrolledWindow()
        uscr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        uscr.add(vbox)

        pscr = Gtk.ScrolledWindow()
        pscr.set_policy(Gtk.PolicyType.AUTOMATIC,
                Gtk.PolicyType.AUTOMATIC)
        pscr.add(self.map_win)

        self.pack_start(uscr, False, True, 0)
        self.pack_start(pscr, True, True, 0)
