from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiTestdataHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass

    @tornado.gen.coroutine
    def post(self, id):
        pass

    @tornado.gen.coroutine
    def delete(self, id):
        pass
