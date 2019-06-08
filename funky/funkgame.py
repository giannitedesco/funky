from . import server, client
from gi.repository import GObject

from .cards import cards

RL = GObject.SIGNAL_RUN_LAST

class GameSeat(GObject.GObject):
    __gsignals__ = {
        'join': (RL, None, ()),
        'leave': (RL, None, ()),
        'update': (RL, None, ()),
    }
    def __init__(self, snr):
        super(GameSeat, self).__init__()
        setter = super(GameSeat, self).__setattr__
        setter('seat_nr', snr)
        setter('in_game', False)
        self.clear()

    def clear(self):
        setter = super(GameSeat, self).__setattr__
        sig = self.in_game
        setter('name', '')
        setter('money', 50)
        setter('nr_cities', 0)
        setter('capacity', 0)
        setter('plants', (None, None, None, None))
        setter('stock', ((0,0), (0,0), (0,0), (0,0)))
        setter('in_game', False)
        if sig:
            self.emit('leave')

    def __setattr__(self, k, v):
        old = getattr(self, k)
        if v == old:
            return
        #print self.seat_nr, k, repr(old), '->', repr(v)
        super(GameSeat, self).__setattr__(k, v)
        if not self.in_game:
            self.emit('join')
            super(GameSeat, self).__setattr__('in_game', True)
        self.emit('update')

class FunkGame(GObject.GObject):
    __gsignals__ = {
        # Emitted with a Message which should be sent to server
        'tx_msg': (RL, None, (object, )),

        # Emitted with any unhandled messages
        'rx_unhandled': (RL, None, (object, )),

        # Emitted for any chat messages
        'chat_msg': (RL, None, (str, )),

        # Emitted for any chat messages
        'log': (RL, None, (str, )),

        # Game status updates
        'update_ps': (RL, None, (int, int)),
        'update_market':(RL, None, (int, object)),
        'update_map': (RL, None, (int, object)),
        'update_stock': (RL, None, (object,)),
        'update_cities': (RL, None, (object,)),
        'update_current_player': (RL, None, (int, int)),
        'update_player_sequence': (RL, None, (object,)),
        'update_i_am': (RL, None, (int,)),
        'update_city_active': (RL, None, (object, )),
        'update_bid': (RL, None, (int, int, int)),

        'player_join': (RL, None, (object,)),
        'player_update': (RL, None, (object,)),
        'player_leave': (RL, None, (object,)),

        'update_self': (RL, None, (object,)),
    }

    def __init__(self):
        super(GObject.GObject, self).__init__()

        def pjoin_cb(p):
            self.emit('player_join', p)
        def pupdate_cb(p):
            self.emit('player_update', p)
            if self.i_am >= 0 and p.seat_nr == self.i_am:
                self.emit('update_self', p)
        def pleave_cb(p):
            self.emit('player_leave', p)

        self.seats = tuple(GameSeat(snr) for snr in range(6))
        for p in self.seats:
            p.connect('join', pjoin_cb)
            p.connect('update', pupdate_cb)
            p.connect('leave', pleave_cb)

        self.phase = -1
        self.stufe = -1
        self.round = -1

        self.nr_players = 0
        self.current_player = -1
        self.i_am = -1
        self.sequence = (-1, -1, -1, -1, -1, -1)

        self.market = (-1, -1, -1, -1, -1, -1, -1, -1)
        self.cur_bid = (-1, 0, -1)
        self.cards_left = 0

        self.map_nr = -1
        self.dist = None
        self.cities = None
        self.city_active = None

        self.stock = None

    def tx(self, msg):
        'Emits a message to transmit to server'
        self.emit('tx_msg', msg)

    def chat(self, s):
        'Emits a chat message'
        self.emit('chat_msg', s)

    def log(self, s):
        'Emits a log message'
        self.emit('log', s)

    def rx_unhandled(self, msg):
        self.emit('rx_unhandled', msg)

    def pong(self):
        x = client.PingClientMsg()
        self.tx(x)

    def update_ps(self, phase, stufe):
        old_ps = (self.phase, self.stufe)
        self.phase = phase
        self.stufe = stufe
        if (self.phase, self.stufe) == old_ps:
            return
        self.emit('update_ps', self.phase, self.stufe)

    def update_players(self, nr, players):
        for s in reversed(self.seats[nr:]):
            s.clear()
        for n,s in zip(players[:nr], self.seats[:nr]):
            s.name = n
        self.nr_players = nr

    def update_money(self, money):
        for m, s in zip(money, self.seats):
            if not s.in_game:
                continue
            s.money = m

    def update_plant_stock(self, plant_stock):
        for stk, s in zip(plant_stock, self.seats):
            if not s.in_game:
                continue
            s.stock = stk

    def update_nr_city(self, nr_city):
        for c, s in zip(nr_city, self.seats):
            if not s.in_game:
                continue
            nr, cap = c
            s.nr_cities = nr
            s.capacity = cap

    def update_plants(self, plants):
        for p, s in zip(plants, self.seats):
            if not s.in_game:
                continue
            def c(idx):
                if idx < 0:
                    return None
                return cards[idx]
            s.plants = tuple(c(x) for x in p)

    def update_market(self, nr, market):
        old_market = (self.cards_left, self.market)
        self.market = market
        self.cards_left = nr
        if (self.cards_left, self.market) == old_market:
            return
        self.emit('update_market', self.cards_left, self.market)

    def update_map(self, nr, dist):
        old_dists = (self.map_nr, self.dist)
        self.dist = dist
        self.map_nr = nr
        if (self.map_nr, self.dist) == old_dists:
            return
        self.emit('update_map', self.map_nr, self.dist)

    def update_stock(self, stock):
        old_stock = self.stock
        self.stock = stock
        if self.stock == old_stock:
            return
        self.emit('update_stock', self.stock)

    def update_cities(self, cities):
        old_cities = self.cities
        self.cities = cities
        if self.cities == old_cities:
            return
        self.emit('update_cities', self.cities)

    def update_current_player(self, current_player):
        old_cp = self.current_player
        self.current_player = current_player
        if self.current_player == old_cp:
            return
        self.emit('update_current_player',
                self.current_player,
                self.i_am)

    def update_sequence(self, sequence):
        old_seq = self.sequence
        self.sequence = sequence
        if self.sequence == old_seq:
            return
        self.emit('update_player_sequence', self.sequence)

    def update_i_am(self, i_am):
        old_me = int(self.i_am)
        self.i_am = i_am
        if self.i_am == old_me:
            return
        self.emit('update_i_am', self.i_am)

    def update_city_active(self, city_active):
        old_city_active = self.city_active
        self.city_active = city_active
        if self.city_active == old_city_active:
            return
        self.emit('update_city_active', self.city_active)

    def update_bid(self, cur_bid):
        old_bid = self.cur_bid
        self.cur_bid = cur_bid
        if self.cur_bid == old_bid:
            return
        self.emit('update_bid', *self.cur_bid)

    def dispatch(self, msg):
        def nop_cb(msg):
            return
        def ping_cb(msg):
            self.pong()
        def chat_cb(msg):
            self.chat(msg.cmd)

        def map_cb(msg):
            maps = ('usa.jpg', 'deut.jpg',
                'frankreich.jpg', 'italien.jpg', 'bw.jpg')
            self.update_map(msg.map, msg.dist)

        def player_cb(msg):
            self.round = msg.round
            self.update_ps(msg.phase, msg.stufe)

            self.update_i_am(msg.i_am_id)

            an = ('player%d'%x for x in range(1, 7))
            players = tuple([getattr(msg, x) for x in an])
            self.update_players(int(msg.nr_players), players)

            self.update_money(msg.money)

            self.update_sequence(msg.sequence)

            self.update_current_player(msg.current_player)

        def score_cb(msg):
            self.update_plants(msg.plants)
            self.update_nr_city(msg.nr_city)

        def auction_cb(msg):
            phase = msg.phase_stufe & 0x3ff
            stufe = msg.phase_stufe >> 10
            self.update_ps(phase, stufe)

            self.update_money(msg.money)

            self.update_current_player(msg.current_player)

            self.update_market(msg.cards_left, msg.market)
            self.update_bid(msg.bid)

        def materials_cb(msg):
            self.update_ps(msg.phase, self.stufe)
            self.update_money(msg.money)
            self.update_stock(msg.stock)
            self.update_plant_stock(msg.materials)
            self.update_current_player(msg.current_player)

        def city_cb(msg):
            phase = msg.phase_stufe & 0x3ff
            stufe = msg.phase_stufe >> 10
            self.update_ps(phase, stufe)
            self.update_cities(msg.city)
            self.update_city_active(msg.city_active)
            self.update_nr_city(msg.nr_city)
            self.update_money(msg.money)
            self.update_current_player(msg.current_player)

        disp = {
            server.PingServerMsg: ping_cb,
            server.CmdServerMsg: chat_cb,
            server.FunkenMapServerMsg: map_cb,
            server.FunkenPlayerServerMsg: player_cb,
            server.FunkenScoreServerMsg: score_cb,
            server.FunkenAuctionServerMsg: auction_cb,
            server.FunkenMaterialsServerMsg: materials_cb,
            server.FunkenCityServerMsg: city_cb,
            server.FunkenUnusedServerMsg: nop_cb,
            server.FunkenAnimServerMsg: nop_cb,
        }

        # dispatch the message
        cb = disp.get(msg.__class__, None)
        if cb is None:
            self.rx_unhandled(msg)
            return

        cb(msg)

    def rx_msg(self, t, b):
        'Handles a message received from the server'
        # figure out the type of message
        c = server.msgmap.get(t, None)
        if c is None:
            self.log('UNKNOWN(%r), %r'%(t, b))
            return

        # parse the message from the bytes
        msg = c.frombytes(b)

        self.dispatch(msg)

    def cl_cmd(self, cmd):
        'Receive a string typed in to server window'
        if len(cmd) >=2 and cmd[:2] == '//':
            self.game_cmd(cmd[2:])
        else:
            self.sys_cmd(cmd)

    def sys_cmd(self, cmd):
        'Send a command message'
        x = client.CmdClientMsg(cmd = cmd)
        self.tx(x)

    def game_cmd(self, cmd):
        'Send a Funken game command'

        def pass_cb(cmd, args):
            self.bid(-1, -1)

        def bid_cb(cmd, args):
            k, p = args.split(None, 2)
            self.bid(int(k), int(p))

        def rs_cb(cmd, args):
            k, o, m, ke = args.split(None, 3)
            self.buy_rs(int(k), int(o), int(m), int(ke))

        def build_cb(cmd, args):
            self.build(int(args))

        def nobuild_cb(cmd, args):
            self.finish_building()

        def fire_cb(cmd, args):
            a, b, c, d = args.split(None, 3)
            self.fire(int(a), int(b), int(c), int(d))

        def demolish_cb(cmd, args):
            self.demolish(int(args))

        def rsmove_cb(cmd, args):
            frm, to, rs = args.split(None, 2)
            self.rs_move(int(frm), int(to), int(rs))

        def eval_cb(cmd, args):
            x = eval(args)
            self.dispatch(x)

        disp = {
            'pass': pass_cb,
            'bid': bid_cb,
            'rs': rs_cb,
            'build': build_cb,
            'nobuild': nobuild_cb,
            'fire': fire_cb,
            'demolish': demolish_cb,
            'rsmove': rsmove_cb,
            'eval': eval_cb,
        }
        try:
            cmd, args = cmd.split(None, 1)
        except ValueError:
            cmd = cmd
            args = None
        cb = disp.get(cmd, None)
        if cb is None:
            self.chat('Unknwon game command: %s'%cmd)
        else:
            cb(cmd, args)

    def demolish(self, plant):
        self.action(1, plant, 0, 0, 0)

    def fire(self, a, b, c, d):
        self.action(0, a, b, c, d)

    def buy_rs(self, coal, oil, trash, nuke):
        self.action(0, coal, oil, trash, nuke)

    def rs_move(self, frm, to, rs):
        self.action(2, frm, to, rs, 0)

    def build(self, s):
        self.action(0, s, 0, 0, 0)

    def finish_building(self):
        self.action(1, 0, 0, 0, 0)

    def bid(self, k, p):
        if k < 0:
            k = 0x3f
        if p < 0:
            p = 0x3f
        code = (p << 6) | k
        x = client.FunkenClientMsg(code = code)
        self.tx(x)

    def action(self, act, k, p, p1, p2):
        code = (act << 28)
        code |= k
        code |= p << 6
        code |= p1 << 12
        code |= p2 << 18
        x = client.FunkenClientMsg(code = code)
        self.tx(x)
