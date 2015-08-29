from req import WebRequestHandler
from req import Service


class Web404Handler(WebRequestHandler):
    def get(self):
        self.write_error(404)
        return

    def post(self):
        return
