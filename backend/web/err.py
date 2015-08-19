from req import RequestHandler
from req import Service


class Web404Handler(RequestHandler):
    def get(self):
        self.write_error(404)
        return

    def post(self):
        return
