import redis
import msgpack

class MyRedis(redis.StrictRedis):
    def __init__(self, host='localhost', port=6379, db=0):
        super().__init__(host=host, port=port, db=db)

    def set(self, name, value):
        value = msgpack.packb(value)
        return super().set(name, value)

    def get(self, name):
        res = super().get(name)
        if not res:
            return None
        return msgpack.unpackb(res, encoding='utf-8')

    def setex(self, name, time, value):
        value = msgpack.packb(value)
        return super().setex(name, time, value)

    def setnx(self, name, value, time):
        value = msgpack.packb(value)
        return super().setnx(name, value, time)

    def getset(self, name, value):
        value = msgpack.packb(value)
        return super().getset(name, value)

