from req import ApiRequestHandler
from req import Service
import tornado

class Users(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def post(self):
        pass

class User(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass

    @tornado.gen.coroutine
    def put(self, id):
        pass

    @tornado.gen.coroutine
    def delete(self, id):
        pass

