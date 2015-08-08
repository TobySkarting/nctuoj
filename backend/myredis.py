import redis
import msgpack
import json
import pickle

DEFAULT_EXPIRE_TIME = 3600

class MyRedis(redis.StrictRedis):
    def __init__(self, host='localhost', port=6379, db=0):
        super().__init__(host=host, port=port, db=db)

    def set(self, name, value, time=DEFAULT_EXPIRE_TIME):
        return self.setex(name, time, value)

    def get(self, name):
        res = super().get(name)
        if not res:
            return None
        return pickle.loads(res, encoding='utf-8')

    def setex(self, name, time, value):
        value = pickle.dumps(value)
        return super().setex(name, time, value)

    def setnx(self, name, value):
        value = pickle.dumps(value)
        return super().setnx(name, value)

    def getset(self, name, value):
        value = pickle.dumps(value)
        return super().getset(name, value)

