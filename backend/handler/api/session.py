from req import ApiRequestHandler
from req import Service
import tornado

class Session(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        pass

    @tornado.gen.coroutine
    def delete(self):
        pass

