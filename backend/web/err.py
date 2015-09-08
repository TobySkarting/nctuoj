from req import WebRequestHandler
from req import Service
import tornado


class Web404Handler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write_error(404)
        return

    def post(self):
        return
