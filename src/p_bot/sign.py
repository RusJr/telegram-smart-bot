import execjs
from pprint import pprint
from datetime import datetime


class PBotSign:

    _js_get_random = execjs.compile("""
        _get_random = function() {return Math["random"]();};
    """)

    _js_get_crc = execjs.compile("""   
        var _0x265f6c = function _0x265f6c() {
            var _0xdeafce;
            var _0x40598f = [];
            for (var _0x4558e0 = 0x0; _0x4558e0 < 0x100; _0x4558e0++) {
                _0xdeafce = _0x4558e0;
                for (var _0x23fc50 = 0x0; _0x23fc50 < 0x8; _0x23fc50++) {
                    _0xdeafce = _0xdeafce & 0x1 ? 0xedb88320 ^ _0xdeafce >>> 0x1 : _0xdeafce >>> 0x1;
                }
                _0x40598f[_0x4558e0] = _0xdeafce;
            }
            return _0x40598f;
        };
    
        _get_crc = function(_0x3d2ebf) {
            var _0x3f278b = _0x265f6c();
            var _0x23c6ec = 0x0 ^ -0x1;
            for (var _0xdd386 = 0x0; _0xdd386 < _0x3d2ebf["length"]; _0xdd386++) {
                _0x23c6ec = _0x23c6ec >>> 0x8 ^ _0x3f278b[(_0x23c6ec ^ _0x3d2ebf['charCodeAt'](_0xdd386)) & 0xff];
            }
            return (_0x23c6ec ^ -0x1) >>> 0x0;
        };
    """)

    def __init__(self):
        now = self.get_now()
        self.a = self._get_a()
        self.b = self._get_b(now)
        self.c = self._get_c(now)
        self.d = self._get_d()
        self.e = self._get_random()
        self.t = now
        self.x = self._get_x()

    def to_dict(self)-> dict:
        return {'a': self.a,
                'b': self.b,
                'c': self.c,
                'd': self.d,
                'e': self.e,
                't': self.t,
                'x': self.x}

    @staticmethod
    def _get_key1(): return 'WxvttruvF01cvHy8'

    @staticmethod
    def _get_K21(): return '8r5yD8pl8lLcz20G'

    @staticmethod
    def _get_a(): return 'public-api'

    @staticmethod
    def get_now():
        # js = execjs.compile("""
        #      get_now = function() {
        #         var _now = new Date().getTime();
        #         return _now;
        #     };
        # """)
        return int(datetime.now().timestamp() * 1000)

    @classmethod
    def _get_random(cls):
        return cls._js_get_random.call("_get_random")

    @classmethod
    def _get_crc(cls, string: str):
        return cls._js_get_crc.call("_get_crc", string)

    @classmethod
    def _get_b(cls, timestamp: int):
        input_str = str(timestamp) + 'b'
        return cls._get_crc(input_str)

    @classmethod
    def _get_c(cls, timestamp: int):
        """ getCRCSign """
        return cls._get_crc(cls._get_a() + str(timestamp) + cls._get_key1() + cls._get_K21() + "8dY72lsSOvXnJF4T")

    @classmethod
    def _get_d(cls):
        input_str = str(cls.get_now()) + 'd'
        return cls._get_crc(input_str)

    @classmethod
    def _get_x(cls):
        return cls._get_random() * 10


if __name__ == '__main__':
    sign_parameters = PBotSign().to_dict()
    pprint(sign_parameters)
