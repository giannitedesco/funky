from struct import pack, unpack
from operator import itemgetter

class Sentinel(object):
	pass

class Message(tuple):
	__slots__ = ()
	_initialized = False
	def __new__(_cls, *args, **kwargs):
		if not _cls._initialized:
			for i, x in enumerate(_cls._fields):
				setattr(_cls, x, property(itemgetter(i)))
			_cls._initialized = True

		a = tuple(map(lambda x: kwargs.pop(x, Sentinel()), _cls._fields))
		if kwargs:
			raise Exception('Unknown fields: %s'%\
					', '.join(kwargs.keys()))
		def setdef(a, d, t):
			if isinstance(a, Sentinel):
				return t(d)
			else:
				return t(a)

		ax = map(lambda (x,y,z):setdef(x,y,z),
			zip(a, _cls._defaults, _cls._types))
		ret = tuple.__new__(_cls, ax)
		return ret

	def get_bytes(self):
		msg = ''.join(map(lambda x:x.get_bytes(), self))
		l = len(msg) + 5
		hdr = ''.join((chr((l >> 16) & 0xff),
				chr((l >> 8) & 0xff),
				chr(l & 0xff),
				chr((self._msgtype >> 8) & 0xff),
				chr(self._msgtype & 0xff)))
		return hdr + msg

	def __repr__(self):
		s = map(lambda (k,v):'%s=%r'%(k,v), zip(self._fields, self))
		return self.__class__.__name__ + '(%s)'%', '.join(s)

	def __str__(self):
		return self.__repr__()

	@classmethod
	def frombytes(_cls, b):
		args = dict()
		#print _cls, '%r'%b
		for n, t, d in zip(_cls._fields, _cls._types, _cls._defaults):
			#print _cls, t, n
			(val, sz) = t.frombytes(b, d)
			args[n] = val
			b = b[sz:]
		return _cls(**args)

class TInt(int):
	def get_bytes(self):
		return pack('>Bi', 1, self)

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)
		tv, v = unpack('>Bi', b[:5])
		assert(tv == 1)
		return (_cls(v), 5)

class TBool(int):
	def get_bytes(self):
		return pack('>Bi', 1, self)

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)
		tv, v = unpack('>BB', b[:2])
		assert(tv == 2)
		return (_cls(v), 2)

class TIntArray(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		(tv, nr) = unpack('>BH', b[:3])
		assert(tv == 5)
		ofs = 3
		out = list()
		for i in xrange(nr / 4):
			s = TInt(unpack('>i', b[ofs:ofs+4])[0])
			out.append(s)
			ofs += 4

		return (_cls(out), ofs)

class TIntVector(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		(tv, nr) = unpack('>BH', b[:3])
		assert(tv == 8)
		ofs = 3
		out = list()
		for i in xrange(nr / 4):
			s = TInt(unpack('>i', b[ofs:ofs+4])[0])
			out.append(s)
			ofs += 4

		return (_cls(out), ofs)

class TInt2Array(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		(tv, tot_len, nr) = unpack('>BHB', b[:4])
		assert(tv == 11)
		ofs = 4

		out = list()
		for i in xrange(nr):
			(s, sz) = TIntArray.frombytes(b[ofs:], '')
			out.append(s)
			ofs += sz

		return (_cls(out), ofs)

class TInt3Array(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		(tv, tot_len, nr) = unpack('>BHB', b[:4])
		assert(tv == 16)
		ofs = 4

		out = list()
		for i in xrange(nr):
			(s, sz) = TInt2Array.frombytes(b[ofs:], '')
			out.append(s)
			ofs += sz

		return (_cls(out), ofs)

class TStr(str):
	def fencode(self, s):
		ret = ''
		for c in map(ord, s):
			if c >= 1 and c <= 127:
				ret += chr(c)
			else:
				ret += chr(0xc0 | ((c >> 6) & 0x1f))
				ret += chr(0x80 | ((c & 0x3f)))
		return ret

	def get_bytes(self):
		e = self.fencode(self)
		return pack('>BH', 3, len(e)) + e

	@classmethod
	def fdecode(_cls, s):
		ret = ''
		a = 0
		for c in map(ord, s):
			if (c & 0xc0) == 0xc0:
				a = (c & 0x1f) << 6
			else:
				if c & 0x80:
					c &= 0x3f
				ret += chr(a | c)
				a = 0
		return ret
	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)
		tv, sz = unpack('>BH', b[:3])
		assert(tv == 3)
		return (_cls(_cls.fdecode(b[3:3 + sz])), sz + 3)

class TStrArray(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		tv, totlen, nr = unpack('>BHH', b[:5])
		assert(tv == 6)
		ofs = 5
		out = list()
		for i in xrange(nr):
			(s, sz) = TStr.frombytes(b[ofs:], '')
			out.append(s)
			ofs += sz

		return (_cls(out), ofs)

class TStr2Array(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		tv, totlen_hi, totlen, nr = unpack('>BBHH', b[:6])
		assert(tv == 9)
		ofs = 6
		out = list()
		for i in xrange(nr):
			(s, sz) = TStrArray.frombytes(b[ofs:], '')
			out.append(s)
			ofs += sz

		return (_cls(out), ofs)

class TBoolArray(tuple):
	def get_bytes(self):
		raise NotImplementedError

	@classmethod
	def frombytes(_cls, b, d):
		if not b:
			return (_cls(d), 0)

		(tv, nr) = unpack('>BH', b[:3])
		assert(tv == 10)
		ofs = 3
		out = list()
		for i in xrange(nr):
			s = TBool(unpack('>B', b[ofs])[0])
			out.append(s)
			ofs += 1

		return (_cls(out), ofs)

