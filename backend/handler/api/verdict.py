from req import ApiRequestHandler
from req import Service
import tornado

class Verdicts(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def post(self):
        pass

class Verdict(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def put(self):
        pass

    @tornado.gen.coroutine
    def delete(self):
        pass
