from req import WebRequestHandler
from req import Service
import tornado

class WebGroupHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass

    @tornado.gen.coroutine
    def post(self, id):
        pass
