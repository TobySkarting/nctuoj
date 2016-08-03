from req import ApiRequestHandler
from req import Service
import tornado

class Executes(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def post(self):
        pass

class Execute(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def put(self):
        pass

    @tornado.gen.coroutine
    def delete(self):
        pass
